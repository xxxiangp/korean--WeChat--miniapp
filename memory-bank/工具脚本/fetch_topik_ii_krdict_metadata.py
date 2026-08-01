#!/usr/bin/env python3
"""Fetch auditable TOPIK II metadata from the official Korean Basic Dictionary."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup, NavigableString, Tag


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "memory-bank" / "数据文件"
OUTPUT_PATH = DATA_DIR / "topik_ii_krdict_metadata.json"
SOURCE_POOLS = (
    DATA_DIR / "topik_intermediate_source_pool.json",
    DATA_DIR / "topik_advanced_source_pool.json",
)

SOURCE_PAGE = "https://krdict.korean.go.kr/chn/mainAction"
SEARCH_FORM_URL = "https://krdict.korean.go.kr/chn/dicSearchDetail/searchDetailWords"
SEARCH_URL = "https://krdict.korean.go.kr/chn/dicSearchDetail/searchDetailWordsResult"
DETAIL_URL = "https://krdict.korean.go.kr/chn/dicSearch/SearchView?ParaWordNo={target_code}"
USER_AGENT = "Mozilla/5.0"
PAGE_SIZE = 100
PARSER_VERSION = 2
TODAY = date.today().isoformat()

THREAD_STATE = threading.local()


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def load_targets() -> tuple[set[str], dict[str, set[str]], str]:
    targets: set[str] = set()
    for path in SOURCE_POOLS:
        data = read_json(path)
        targets.update(word["korean"] for word in data["words"])

    by_prefix: dict[str, set[str]] = {}
    for korean in targets:
        by_prefix.setdefault(korean[0], set()).add(korean)
    digest = hashlib.sha256("\n".join(sorted(targets)).encode("utf-8")).hexdigest()
    return targets, by_prefix, digest


def new_session() -> tuple[requests.Session, str]:
    session = requests.Session()
    response = session.get(
        SEARCH_FORM_URL, headers={"User-Agent": USER_AGENT}, timeout=90
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    token_node = soup.select_one("form[name=searchDetailWordsForm] input[name=_csrf]")
    if not token_node or not token_node.get("value"):
        raise ValueError("Korean Basic Dictionary CSRF token missing")
    return session, str(token_node["value"])


def thread_session() -> tuple[requests.Session, str]:
    if not hasattr(THREAD_STATE, "session"):
        THREAD_STATE.session, THREAD_STATE.csrf = new_session()
    return THREAD_STATE.session, THREAD_STATE.csrf


def reset_thread_session() -> tuple[requests.Session, str]:
    if hasattr(THREAD_STATE, "session"):
        THREAD_STATE.session.close()
    THREAD_STATE.session, THREAD_STATE.csrf = new_session()
    return THREAD_STATE.session, THREAD_STATE.csrf


def request_params(prefix: str, page: int, csrf: str) -> list[tuple[str, str]]:
    return [
        ("nation", "chn"),
        ("nationCode", "11"),
        ("searchFlag", "Y"),
        ("sort", "1"),
        ("currentPage", str(page)),
        ("ParaWordNo", ""),
        ("syllablePosition", ""),
        ("actCategoryList", ""),
        ("gubun", "W"),
        ("all_wordNativeCode", "ALL"),
        ("all_sp_code", "ALL"),
        ("all_imcnt", "ALL"),
        ("all_multimedia", "ALL"),
        ("searchSyllableStart", ""),
        ("searchSyllableEnd", ""),
        ("searchOp", "AND"),
        ("searchTarget", "word"),
        ("searchOrglanguage", "all"),
        ("wordCondition", "wordStart"),
        ("query", prefix),
        ("blockCount", str(PAGE_SIZE)),
        ("_csrf", csrf),
    ]


def fetch_page(prefix: str, page: int) -> BeautifulSoup:
    last_error = ""
    for attempt in range(6):
        try:
            session, csrf = thread_session()
            response = session.get(
                SEARCH_URL,
                params=request_params(prefix, page, csrf),
                headers={"User-Agent": USER_AGENT},
                timeout=120,
            )
            response.raise_for_status()
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.title.get_text(" ", strip=True) if soup.title else ""
            if "500" not in title:
                return soup
            last_error = f"server error page: {title}"
        except (requests.RequestException, ValueError) as exc:
            last_error = str(exc)
        time.sleep(min(30, 2 ** attempt))
        reset_thread_session()
    raise RuntimeError(f"KRDICT fetch failed prefix={prefix} page={page}: {last_error}")


def normalized_headword(raw: str) -> str:
    return re.sub(r"\s+\d+$", "", raw).strip()


def direct_text(tag: Tag) -> str:
    return "".join(
        str(child) for child in tag.contents if isinstance(child, NavigableString)
    ).strip()


def extract_pronunciations(container: Tag) -> list[str]:
    pronunciations: list[str] = []
    for node in container.select("span.search_sub"):
        value = direct_text(node)
        for pronunciation in re.findall(r"\[([^\]]+)\]", value):
            cleaned = re.sub(r"[\sː:]", "", pronunciation)
            if cleaned and cleaned not in pronunciations:
                pronunciations.append(cleaned)
    return pronunciations


def parse_result(dl: Tag, targets: set[str]) -> tuple[str, dict[str, Any]] | None:
    head_node = dl.select_one("dt .word_type1_17")
    if not head_node:
        return None
    displayed_headword = head_node.get_text(" ", strip=True)
    korean = normalized_headword(displayed_headword)
    if korean not in targets:
        return None

    dt = dl.find("dt")
    if not dt:
        return None
    code_match = re.search(r"checkSubmit\('(\d+)'", str(dt))
    target_code = int(code_match.group(1)) if code_match else 0

    pos_ko = ""
    pos_cn = ""
    pos_node = dt.select_one(".word_att_type1")
    if pos_node:
        pos_match = re.search(r"「([^」]+)」", pos_node.get_text(" ", strip=True))
        pos_ko = pos_match.group(1).strip() if pos_match else ""
        pos_cn_node = pos_node.select_one(".manyLang11")
        pos_cn = pos_cn_node.get_text(" ", strip=True) if pos_cn_node else ""

    chinese_values = [
        dd.get_text(" ", strip=True)
        for dd in dl.find_all("dd", recursive=False)
        if "manyLang11" in (dd.get("class") or [])
    ]
    translated_headword = chinese_values[0] if chinese_values else ""
    translated_definitions = [value for value in chinese_values[1:] if value]

    record = {
        "target_code": target_code,
        "displayed_headword": displayed_headword,
        "pronunciations_hangul": extract_pronunciations(dt),
        "pos_ko": pos_ko,
        "pos_cn": pos_cn,
        "translated_headword_zh": translated_headword,
        "translated_definitions_zh": translated_definitions,
        "detail_url": DETAIL_URL.format(target_code=target_code) if target_code else "",
    }
    return korean, record


def fetch_prefix(prefix: str, targets: set[str]) -> tuple[str, dict[str, list[dict[str, Any]]], int]:
    found: dict[str, list[dict[str, Any]]] = {}
    page = 1
    while True:
        soup = fetch_page(prefix, page)
        result_nodes = soup.select("div.search_result > dl")
        for dl in result_nodes:
            parsed = parse_result(dl, targets)
            if not parsed:
                continue
            korean, record = parsed
            records = found.setdefault(korean, [])
            if record not in records:
                records.append(record)

        if len(result_nodes) < PAGE_SIZE:
            break
        page += 1
        if page > 100:
            raise ValueError(f"Unexpected KRDICT page count for prefix {prefix}")
        time.sleep(0.15)
    return prefix, found, page


def atomic_write(data: dict[str, Any]) -> None:
    temporary = OUTPUT_PATH.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(OUTPUT_PATH)


def snapshot_payload(
    targets: set[str],
    target_sha256: str,
    completed_prefixes: set[str],
    prefix_page_counts: dict[str, int],
    entries: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    return {
        "parser_version": PARSER_VERSION,
        "status": (
            "official_dictionary_metadata_snapshot_complete"
            if len(completed_prefixes) == len({word[0] for word in targets})
            else "official_dictionary_metadata_snapshot_in_progress"
        ),
        "retrieved_at": TODAY,
        "source": {
            "name": "韩国国立国语院《韩国语基础词典》中文版",
            "organization": "국립국어원",
            "source_page": SOURCE_PAGE,
            "query_endpoint": SEARCH_URL,
            "source_note": "官方学习词典网页高级检索；按词头首音节分页，仅保存本项目候选词结果",
        },
        "target_total": len(targets),
        "target_sha256": target_sha256,
        "completed_prefixes": sorted(completed_prefixes),
        "prefix_page_counts": dict(sorted(prefix_page_counts.items())),
        "found_word_total": len(entries),
        "missing_words": sorted(targets - set(entries)),
        "entries": dict(sorted(entries.items())),
    }


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if not 1 <= args.workers <= 6:
        raise ValueError("workers must be between 1 and 6")

    targets, by_prefix, target_sha256 = load_targets()
    completed_prefixes: set[str] = set()
    prefix_page_counts: dict[str, int] = {}
    entries: dict[str, list[dict[str, Any]]] = {}

    if OUTPUT_PATH.exists():
        existing = read_json(OUTPUT_PATH)
        existing_targets = set(existing.get("entries", {})) | set(
            existing.get("missing_words", [])
        )
        if (
            existing.get("parser_version") == PARSER_VERSION
            and targets.issubset(existing_targets)
        ):
            if existing.get("target_sha256") != target_sha256:
                print("source pool only removed targets; pruning the KRDICT snapshot")
            completed_prefixes.update(existing.get("completed_prefixes", []))
            completed_prefixes.intersection_update(by_prefix)
            prefix_page_counts.update(
                {
                    prefix: count
                    for prefix, count in existing.get("prefix_page_counts", {}).items()
                    if prefix in by_prefix
                }
            )
            entries.update(
                {
                    korean: records
                    for korean, records in existing.get("entries", {}).items()
                    if korean in targets
                }
            )
        elif existing.get("target_sha256") != target_sha256:
            print("source pool added or replaced targets; rebuilding the KRDICT snapshot")
        else:
            print(
                "parser version changed; rebuilding the KRDICT snapshot "
                f"with parser v{PARSER_VERSION}"
            )

    pending = [prefix for prefix in sorted(by_prefix) if prefix not in completed_prefixes]
    print(
        f"targets={len(targets)} prefixes={len(by_prefix)} "
        f"completed={len(completed_prefixes)} pending={len(pending)}"
    )

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(fetch_prefix, prefix, by_prefix[prefix]): prefix
            for prefix in pending
        }
        for completed_count, future in enumerate(as_completed(futures), start=1):
            prefix, found, page_count = future.result()
            for korean, records in found.items():
                entries[korean] = records
            completed_prefixes.add(prefix)
            prefix_page_counts[prefix] = page_count

            if completed_count % 10 == 0 or completed_count == len(pending):
                atomic_write(
                    snapshot_payload(
                        targets,
                        target_sha256,
                        completed_prefixes,
                        prefix_page_counts,
                        entries,
                    )
                )
                print(
                    f"progress={len(completed_prefixes)}/{len(by_prefix)} "
                    f"found={len(entries)}"
                )

    final_payload = snapshot_payload(
        targets, target_sha256, completed_prefixes, prefix_page_counts, entries
    )
    atomic_write(final_payload)
    print(f"status={final_payload['status']}")
    print(f"found={final_payload['found_word_total']}")
    print(f"missing={len(final_payload['missing_words'])}")
    print(f"output={OUTPUT_PATH}")


if __name__ == "__main__":
    main()
