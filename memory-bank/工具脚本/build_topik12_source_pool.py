#!/usr/bin/env python3
"""
Build TOPIK 1/2 source pools from official level criteria and public TOPIK word lists.

This script does not claim to produce an official fixed TOPIK vocabulary list.
Official sources define exam format, score bands, ability descriptors and rough
vocabulary sizes; they do not publish one authoritative per-word list. The output
therefore keeps public source evidence for every candidate word.
"""

from __future__ import annotations

import json
import re
import socket
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urljoin
from urllib.request import ProxyHandler, Request, build_opener

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "memory-bank" / "数据文件"
DOC_DIR = ROOT / "memory-bank" / "产品文档"

HANGUL = "\uAC00-\uD7A3"


@dataclass(frozen=True)
class Source:
    key: str
    name: str
    url: str
    source_type: str


OFFICIAL_SOURCES = [
    Source(
        "niied_topik_overview",
        "National Institute for International Education TOPIK overview",
        "https://www.niied.go.kr/web/NIIED/contents/niiedEng/eng_topikOverview",
        "official: TOPIK owner/operator overview, test format and levels",
    ),
    Source(
        "neea_topik_intro",
        "中国教育考试网 TOPIK 考试介绍",
        "https://topik-main.neea.cn/xhtml1/folder/1507/1511-1.htm",
        "official China test-administration page: score bands and Chinese ability descriptors",
    ),
]

PUBLIC_WORD_SOURCES = [
    Source(
        "topikindepth_level1",
        "TOPIK in Depth Level 1 vocabulary",
        "https://topikindepth.com/en/topik/1/",
        "public level-specific TOPIK vocabulary list; used for 1级 split only",
    ),
    Source(
        "topikindepth_level2",
        "TOPIK in Depth Level 2 vocabulary",
        "https://topikindepth.com/en/topik/2/",
        "public level-specific TOPIK vocabulary list; used for 2级 split only",
    ),
    Source(
        "tammy_1671",
        "Tammy Korean TOPIK I Vocabulary List 1671",
        "https://learning-korean.com/elementary/20210101-10466/",
        "public TOPIK I vocabulary list with English glosses",
    ),
    Source(
        "koreantopik_1850",
        "KoreanTopik TOPIK 1 Vocabulary List 1850",
        "https://www.koreantopik.com/2024/05/topik-1-vocabulary-list-1850-for.html",
        "public TOPIK I vocabulary list, split across linked pages",
    ),
]


def proxy_opener():
    proxies: dict[str, str] = {}
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.4)
        try:
            sock.connect(("127.0.0.1", 7897))
            proxies = {
                "http": "http://127.0.0.1:7897",
                "https": "http://127.0.0.1:7897",
            }
        except OSError:
            proxies = {}
    return build_opener(ProxyHandler(proxies))


OPENER = proxy_opener()


def fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with OPENER.open(req, timeout=60) as resp:
        return resp.read().decode("utf-8", "replace")


def clean_word(word: str) -> str:
    word = re.sub(r"\s*\([^)]*\)\s*", "", word).strip()
    return word.replace("\u200b", "").strip()


def is_korean_word(word: str) -> bool:
    return bool(re.fullmatch(rf"[{HANGUL}]+", word)) and 1 <= len(word) <= 12


def add_word(pool: dict[str, dict[str, Any]], word: str, source_key: str, **meta: Any) -> None:
    word = clean_word(word)
    if not is_korean_word(word):
        return
    item = pool.setdefault(word, {"korean": word, "sources": []})
    if source_key not in item["sources"]:
        item["sources"].append(source_key)
    if meta:
        item.setdefault("source_meta", {})[source_key] = meta


def parse_topikindepth(url: str, source_key: str) -> dict[str, dict[str, Any]]:
    soup = BeautifulSoup(fetch(url), "html.parser")
    pool: dict[str, dict[str, Any]] = {}
    for a in soup.find_all("a"):
        text = a.get_text(" ", strip=True)
        m = re.match(rf"^([{HANGUL}]+)\s+", text)
        if m:
            add_word(pool, m.group(1), source_key)
    return pool


def parse_tammy(url: str) -> dict[str, dict[str, Any]]:
    soup = BeautifulSoup(fetch(url), "html.parser")
    table = soup.find("table")
    pool: dict[str, dict[str, Any]] = {}
    if not table:
        return pool
    for row in table.find_all("tr")[1:]:
        cells = [cell.get_text(" ", strip=True) for cell in row.find_all(["td", "th"])]
        if len(cells) >= 3:
            add_word(pool, cells[1], "tammy_1671", source_no=cells[0], meaning_en=cells[2])
    return pool


def parse_koreantopik(index_url: str) -> dict[str, dict[str, Any]]:
    soup = BeautifulSoup(fetch(index_url), "html.parser")
    page_urls: list[str] = []
    for a in soup.find_all("a", href=True):
        if a.get_text(" ", strip=True).startswith("From "):
            page_urls.append(urljoin(index_url, a["href"]))
    page_urls = list(dict.fromkeys(page_urls))

    pool: dict[str, dict[str, Any]] = {}
    for page in page_urls:
        page_soup = BeautifulSoup(fetch(page), "html.parser")
        table = page_soup.find("table")
        if not table:
            continue
        for row in table.find_all("tr")[1:]:
            cells = row.find_all(["td", "th"])
            if not cells:
                continue
            first = cells[0].get_text(" ", strip=True)
            m = re.match(rf"^(\d{{1,4}})\s+([{HANGUL}]+)\b", first)
            if m:
                add_word(pool, m.group(2), "koreantopik_1850", source_no=m.group(1), page=page)
    return pool


def load_project_vocab() -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {}
    for level in ["beginner", "intermediate", "advanced"]:
        path = DATA_DIR / f"{level}.json"
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for word in data.get("words", []):
            out.setdefault(word["korean"], []).append(
                {
                    "level": level,
                    "id": word["id"],
                    "meaning": word.get("meaning", ""),
                    "pos_cn": word.get("pos_cn", ""),
                    "pronunciation": word.get("pronunciation", ""),
                }
            )
    return out


def merge_source_meta(*pools: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for pool in pools:
        for word, item in pool.items():
            target = merged.setdefault(word, {"korean": word, "sources": []})
            for source in item.get("sources", []):
                if source not in target["sources"]:
                    target["sources"].append(source)
            if "source_meta" in item:
                target.setdefault("source_meta", {}).update(item["source_meta"])
    return merged


def build_level_records(
    level_key: str,
    source_pool: dict[str, dict[str, Any]],
    all_sources: dict[str, dict[str, Any]],
    project_vocab: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for idx, korean in enumerate(sorted(source_pool), start=1):
        support = all_sources.get(korean, {"sources": []})
        project_matches = project_vocab.get(korean, [])
        record = {
            "id": idx,
            "korean": korean,
            "topik_level": level_key,
            "sources": sorted(support.get("sources", [])),
            "source_meta": support.get("source_meta", {}),
            "project_vocab_matches": project_matches,
            "metadata_status": "covered_by_project_vocab" if project_matches else "needs_new_entry_review",
        }
        records.append(record)
    return {
        "level": f"topik_{level_key}_source_pool",
        "level_cn": f"TOPIK {level_key[-1]}级源词表",
        "status": "source_pool_not_final_wordbook",
        "generated_at": date.today().isoformat(),
        "official_basis": [source.__dict__ for source in OFFICIAL_SOURCES],
        "public_word_sources": [source.__dict__ for source in PUBLIC_WORD_SOURCES],
        "total": len(records),
        "words": records,
    }


def write_doc(level1: dict[str, Any], level2: dict[str, Any], all_sources: dict[str, dict[str, Any]]) -> None:
    total = level1["total"] + level2["total"]
    covered1 = sum(1 for w in level1["words"] if w["metadata_status"] == "covered_by_project_vocab")
    covered2 = sum(1 for w in level2["words"] if w["metadata_status"] == "covered_by_project_vocab")

    lines = [
        "# TOPIK 1级/2级词汇书官方依据与编写记录",
        "",
        f"> 创建日期：{date.today().isoformat()}",
        f"> 最后更新：{date.today().isoformat()}",
        "> 状态：源词表已建立 / 正式词书待逐词补全",
        "> 用途：记录 TOPIK 1级、2级词汇书的官方依据、公开词表来源、拆分逻辑和待补字段",
        "",
        "---",
        "",
        "## 一、边界更正",
        "",
        "TOPIK 官方公开的是考试结构、等级分数、能力描述和大致词汇量要求，不公开一份唯一、固定、逐词可核验的官方词汇表。因此本项目不能把任何公开整理词表称为“官方原表”。",
        "",
        "本次重新编写时，官方材料只作为等级边界依据；逐词候选来自公开 TOPIK 词表，并保留每个词的来源证据。正式词书必须逐词补齐中文释义、发音、词性、quiz 和音频映射后才能发布。",
        "",
        "## 二、官方依据",
        "",
        "| 来源 | 性质 | URL |",
        "|------|------|-----|",
    ]
    for source in OFFICIAL_SOURCES:
        lines.append(f"| {source.name} | {source.source_type} | {source.url} |")

    lines += [
        "",
        "官方/考试机构材料确认：TOPIK I 包含 1级和2级；TOPIK I PBT 为听力30题、阅读40题，总分200；1级通常为80-139分，2级为140-200分。中国教育考试网的中文说明还明确写到：1级约800个基本词汇，2级约1500-2000个词汇。",
        "",
        "## 三、公开词表来源",
        "",
        "| 来源 | 用途 | URL |",
        "|------|------|-----|",
    ]
    for source in PUBLIC_WORD_SOURCES:
        lines.append(f"| {source.name} | {source.source_type} | {source.url} |")

    lines += [
        "",
        "## 四、本轮产物",
        "",
        f"- `topik_level1_source_pool.json`：{level1['total']} 词，作为 TOPIK 1级源词表。",
        f"- `topik_level2_source_pool.json`：{level2['total']} 词，作为 TOPIK 2级增量源词表。",
        f"- 合计：{total} 词，落在 TOPIK 2级约1500-2000词的官方能力区间内。",
        f"- 1级源词表中已有项目释义/发音覆盖：{covered1} 词；待新词补全：{level1['total'] - covered1} 词。",
        f"- 2级源词表中已有项目释义/发音覆盖：{covered2} 词；待新词补全：{level2['total'] - covered2} 词。",
        f"- 外部公开来源去重候选池：{len(all_sources)} 词。",
        "",
        "## 五、下一步",
        "",
        "1. 先处理 `metadata_status = needs_new_entry_review` 的词。",
        "2. 每个新词补齐：中文释义、韩语词性、中文词性、Revised Romanization 发音、3个干扰项。",
        "3. 对来源释义冲突、明显非TOPIK I、专有地名/品牌/过细文化词做人工保留/排除判断。",
        "4. 生成正式 `topik_level1.json`、`topik_level2.json`、quiz、Word、小程序数据和音频映射。",
        "5. 完成前不得把源词表包装成最终词书。",
        "",
    ]
    (DOC_DIR / "TOPIK12官方依据与编写记录.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DOC_DIR.mkdir(parents=True, exist_ok=True)

    topik1 = parse_topikindepth("https://topikindepth.com/en/topik/1/", "topikindepth_level1")
    topik2 = parse_topikindepth("https://topikindepth.com/en/topik/2/", "topikindepth_level2")
    tammy = parse_tammy("https://learning-korean.com/elementary/20210101-10466/")
    koreantopik = parse_koreantopik("https://www.koreantopik.com/2024/05/topik-1-vocabulary-list-1850-for.html")

    all_sources = merge_source_meta(topik1, topik2, tammy, koreantopik)
    project_vocab = load_project_vocab()

    level1 = build_level_records("level1", topik1, all_sources, project_vocab)
    level2 = build_level_records("level2", topik2, all_sources, project_vocab)
    source_pool = {
        "level": "topik_i_source_pool",
        "level_cn": "TOPIK I（1-2级）外部源词池",
        "status": "source_pool_not_final_wordbook",
        "generated_at": date.today().isoformat(),
        "source_counts": {
            "topikindepth_level1": len(topik1),
            "topikindepth_level2": len(topik2),
            "tammy_1671": len(tammy),
            "koreantopik_1850": len(koreantopik),
            "union": len(all_sources),
        },
        "official_basis": [source.__dict__ for source in OFFICIAL_SOURCES],
        "public_word_sources": [source.__dict__ for source in PUBLIC_WORD_SOURCES],
        "words": [all_sources[word] for word in sorted(all_sources)],
    }

    (DATA_DIR / "topik_level1_source_pool.json").write_text(
        json.dumps(level1, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (DATA_DIR / "topik_level2_source_pool.json").write_text(
        json.dumps(level2, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (DATA_DIR / "topik_i_source_pool.json").write_text(
        json.dumps(source_pool, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_doc(level1, level2, all_sources)

    print("TOPIK level1 source words:", level1["total"])
    print("TOPIK level2 source words:", level2["total"])
    print("Public source union:", len(all_sources))
    print(
        "Project covered:",
        sum(1 for word in level1["words"] + level2["words"] if word["metadata_status"] == "covered_by_project_vocab"),
    )
    print(
        "Needs new entry review:",
        sum(1 for word in level1["words"] + level2["words"] if word["metadata_status"] == "needs_new_entry_review"),
    )


if __name__ == "__main__":
    main()
