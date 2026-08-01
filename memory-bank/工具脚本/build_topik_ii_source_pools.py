#!/usr/bin/env python3
"""Build auditable TOPIK 3-6 source pools before final wordbook generation."""

from __future__ import annotations

import html
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "memory-bank" / "数据文件"
DOC_DIR = ROOT / "memory-bank" / "产品文档"
NIKL_SNAPSHOT = DATA_DIR / "topik_ii_nikl_source_snapshot.json"
TODAY = date.today().isoformat()

PURE_HANGUL_RE = re.compile(r"^[가-힣]+$")
EXPECTED_COUNTS = {3: 887, 4: 1898, 5: 1171, 6: 957}
SENSE_ALIGNMENT_EXCLUSIONS = {
    "기": {
        "reason": "public_gloss_not_supported_by_official_exact_headword_senses",
        "review_note": (
            "TOPIK in Depth glosses 기 as a Chinese-character radical/basic component, "
            "but the NIKL curriculum supports 氣/期/旗 senses and the Standard Korean "
            "Dictionary exact-headword audit found no such radical sense."
        ),
    },
    "에": {
        "reason": "public_and_official_evidence_refer_to_different_level_senses",
        "review_note": (
            "The public source lists the elementary locative/time particle, while the "
            "only selected NIKL 2003 C-stage evidence is the homographic interjection. "
            "The particle must not be promoted into the advanced wordbook."
        ),
    },
    "토": {
        "reason": "public_gloss_not_supported_by_official_exact_headword_senses",
        "review_note": (
            "Both public lists gloss 토 as soil, but the Standard Korean Dictionary "
            "exact-headword audit found no standalone soil sense; the NIKL 2017 "
            "Level 3 evidence is the abbreviation for Saturday."
        ),
    },
    "지": {
        "reason": "public_and_official_evidence_refer_to_different_grammar_senses",
        "review_note": (
            "The only public evidence glosses a connective ending meaning because/since, "
            "while the selected NIKL 2003 B-stage evidence and Korean Basic Dictionary "
            "support the dependent noun meaning time elapsed since an event. The omitted "
            "hyphen must not turn the ending into a standalone vocabulary item."
        ),
    },
}


@dataclass(frozen=True)
class Source:
    key: str
    name: str
    url: str
    source_type: str


OFFICIAL_BOUNDARY_SOURCES = [
    Source(
        "niied_topik_overview",
        "NIIED TOPIK overview",
        "https://www.niied.go.kr/web/NIIED/contents/niiedEng/eng_topikOverview",
        "official: TOPIK owner/operator; confirms TOPIK II and Level 3-6 score bands",
    ),
    Source(
        "neea_topik_intro",
        "中国教育考试网TOPIK考试介绍",
        "https://topik-main.neea.cn/xhtml1/folder/1507/1511-1.htm",
        "official China test-administration information",
    ),
]

NIKL_SOURCE = Source(
    "nikl_learning_vocab_5965",
    "韩国国立国语院《韩国语学习用词汇目录》",
    "https://www.korean.go.kr/front/etcData/etcDataView.do?mn_id=46&etc_seq=71",
    "official Korean learner vocabulary list: A 982 / B 2111 / C 2872; not a TOPIK fixed list",
)

NIKL_CURRICULUM_SOURCE = Source(
    "nikl_standard_curriculum_2017",
    "韩国国立国语院《2017国际通用韩国语标准教育课程》词汇等级目录",
    "https://www.korean.go.kr/front_eng/down/down_01V.do?report_seq=932",
    "official Korean standard curriculum vocabulary list with explicit Level 1-6 labels; not a TOPIK fixed list",
)

TOPIK_IN_DEPTH_SOURCES = {
    level: Source(
        f"topikindepth_level{level}",
        f"TOPIK in Depth Level {level} vocabulary",
        f"https://topikindepth.com/zh/topik/{level}/",
        "public level-specific TOPIK vocabulary list with romanization and Chinese glosses",
    )
    for level in range(3, 7)
}

KOREANTOPIK_SOURCE = Source(
    "koreantopik_topik2_3900",
    "KoreanTopik TOPIK 2 Vocabulary List 3900",
    "https://www.koreantopik.com/2024/09/complete-topik-2-vocabulary-list-3900.html",
    "public TOPIK II vocabulary list with English glosses; advertised as 3900, page integrity audited separately",
)
KOREANTOPIK_FEED_URL = (
    "https://www.koreantopik.com/feeds/posts/default/-/"
    "TOPIK%202%20Vocab?alt=json&max-results=100"
)


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fetch_level(level: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    source = TOPIK_IN_DEPTH_SOURCES[level]
    response = requests.get(source.url, headers={"User-Agent": "Mozilla/5.0"}, timeout=90)
    response.raise_for_status()
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    rows: list[dict[str, Any]] = []
    exclusions: list[dict[str, Any]] = []
    seen: set[str] = set()
    links = soup.select("a.word-row-link[data-token]")
    if len(links) != EXPECTED_COUNTS[level]:
        raise ValueError(
            f"TOPIK in Depth Level {level} count changed: "
            f"expected={EXPECTED_COUNTS[level]} actual={len(links)}"
        )

    for position, link in enumerate(links, start=1):
        korean = html.unescape(link.get("data-token", "")).strip()
        reading_node = link.select_one(".reading-col")
        meaning_node = link.select_one(".meaning-col")
        romanization = reading_node.get_text(" ", strip=True) if reading_node else ""
        meaning_zh = ""
        if meaning_node:
            meaning_zh = html.unescape(meaning_node.get("data-meaning-zh", "")).strip()

        base = {
            "korean": korean,
            "topik_sublevel": level,
            "source_position": position,
            "source_key": source.key,
            "source_url": source.url,
        }
        if not PURE_HANGUL_RE.fullmatch(korean):
            exclusions.append({**base, "reason": "non_pure_hangul_or_grammar_form"})
            continue
        if korean in seen:
            exclusions.append({**base, "reason": "duplicate_inside_source_level"})
            continue
        if not romanization or not meaning_zh:
            exclusions.append({**base, "reason": "missing_source_romanization_or_chinese_gloss"})
            continue

        seen.add(korean)
        rows.append(
            {
                **base,
                "romanization_source": romanization,
                "meaning_zh_source": meaning_zh,
                "entry_url": source.url.rstrip("/")
                + "/entries/words/"
                + requests.utils.quote(korean),
            }
        )
    return rows, exclusions


def malformed_html_table_rows(page_html: str) -> list[list[str]]:
    """Parse Blogger's Word-exported table whose td/tr closing tags are omitted."""
    table_match = re.search(r"<table[\s\S]*?</table>", page_html, re.IGNORECASE)
    if not table_match:
        raise ValueError("KoreanTopik page table missing")

    rows: list[list[str]] = []
    for chunk in re.split(r"<tr[^>]*>", table_match.group(0), flags=re.IGNORECASE)[1:]:
        cells: list[str] = []
        raw_cells = re.findall(
            r"<td[^>]*>([\s\S]*?)(?=<td\b|<tr\b|</tr|</tbody|</table|$)",
            chunk,
            re.IGNORECASE,
        )
        for raw_cell in raw_cells:
            value = html.unescape(re.sub(r"<[^>]+>", " ", raw_cell))
            cells.append(re.sub(r"\s+", " ", value).strip())
        if cells:
            rows.append(cells)
    return rows


def fetch_koreantopik() -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    feed_request_count = 0
    start_index = 1
    total_results = 1
    while start_index <= total_results:
        feed_url = f"{KOREANTOPIK_FEED_URL}&start-index={start_index}"
        response = requests.get(
            feed_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=120
        )
        response.raise_for_status()
        payload = response.json()
        feed = payload["feed"]
        page_entries = feed.get("entry", [])
        if not page_entries:
            raise ValueError(
                f"KoreanTopik feed stopped before total: start={start_index} total={total_results}"
            )
        entries.extend(page_entries)
        feed_request_count += 1
        total_results = int(feed["openSearch$totalResults"]["$t"])
        start_index += len(page_entries)

    content_by_url: dict[str, str] = {}
    for entry in entries:
        alternate_links = [
            link["href"]
            for link in entry.get("link", [])
            if link.get("rel") == "alternate"
        ]
        if alternate_links:
            content_by_url[alternate_links[0]] = entry.get("content", {}).get("$t", "")

    index_html = content_by_url.get(KOREANTOPIK_SOURCE.url, "")
    if not index_html:
        raise ValueError("KoreanTopik index post missing from public Blogger feed")
    soup = BeautifulSoup(index_html, "html.parser")
    page_urls = list(
        dict.fromkeys(
            link["href"]
            for link in soup.find_all("a", href=True)
            if link.get_text(" ", strip=True).startswith("From ")
        )
    )
    if len(page_urls) != 39:
        raise ValueError(f"KoreanTopik page count changed: expected=39 actual={len(page_urls)}")

    index: dict[str, list[dict[str, Any]]] = defaultdict(list)
    exclusions: list[dict[str, Any]] = []
    source_numbers: list[int] = []
    raw_rows = 0
    for page_number, page_url in enumerate(page_urls, start=1):
        page_html = content_by_url.get(page_url, "")
        if not page_html:
            raise ValueError(f"KoreanTopik page missing from public Blogger feed: {page_url}")
        for cells in malformed_html_table_rows(page_html):
            if len(cells) < 3 or not cells[0].isdigit():
                continue
            raw_rows += 1
            source_no = int(cells[0])
            source_numbers.append(source_no)
            korean = re.sub(r"\s*\([^)]*\)\s*", "", cells[1]).strip()
            record = {
                "korean": korean,
                "source_no": source_no,
                "meaning_en_source": cells[2].strip(" ()"),
                "page_number": page_number,
                "page_url": page_url,
            }
            if not PURE_HANGUL_RE.fullmatch(korean):
                exclusions.append({**record, "reason": "non_pure_hangul_or_grammar_form"})
                continue
            index[korean].append(record)

    number_counts = Counter(source_numbers)
    expected_numbers = set(range(1, 3901))
    actual_numbers = set(source_numbers)
    audit = {
        "advertised_total": 3900,
        "page_count": len(page_urls),
        "feed_entry_count": len(entries),
        "feed_request_count": feed_request_count,
        "raw_rows": raw_rows,
        "unique_source_numbers": len(actual_numbers),
        "missing_source_numbers": sorted(expected_numbers - actual_numbers),
        "duplicate_source_numbers": {
            str(number): count for number, count in number_counts.items() if count > 1
        },
        "accepted_unique_pure_hangul": len(index),
        "excluded_rows": exclusions,
    }
    return index, audit


def load_project_vocab() -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for level in ("beginner", "intermediate", "advanced"):
        data = read_json(DATA_DIR / f"{level}.json")
        for word in data["words"]:
            index[word["korean"]].append(
                {
                    "level": level,
                    "id": word["id"],
                    "pronunciation": word.get("pronunciation", ""),
                    "pos": word.get("pos", ""),
                    "pos_cn": word.get("pos_cn", ""),
                    "meaning": word.get("meaning", ""),
                }
            )
    return index


def load_nikl_index(snapshot: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in snapshot["words"]:
        index[item["korean"]].append(
            {
                "entry": item["entry"],
                "homonym_no": item.get("homonym_no"),
                "rank": item["rank"],
                "pos_code": item["pos_code"],
                "origin": item.get("origin", ""),
                "grade": item["grade"],
            }
        )
    return index


def load_curriculum_index(snapshot: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in snapshot["standard_curriculum_words"]:
        index[item["korean"]].append(
            {
                "entry": item["entry"],
                "homonym_no": item.get("homonym_no"),
                "overall_no": item["overall_no"],
                "level_no": item["level_no"],
                "grade": item["grade"],
                "pos": item["pos"].strip(),
                "guide": item.get("guide", "").strip(),
                "prior_stage": item.get("prior_stage", "").strip(),
            }
        )
    return index


def lower_topik_words() -> set[str]:
    data = read_json(DATA_DIR / "topik_beginner.json")
    return {word["korean"] for word in data["words"]}


def curriculum_level(grade: str) -> int:
    match = re.fullmatch(r"([1-6])급", grade)
    if not match:
        raise ValueError(f"Unexpected curriculum grade: {grade}")
    return int(match.group(1))


def confidence_for(assignment_basis: str, public_support_count: int) -> str:
    if assignment_basis.startswith("nikl_2017"):
        return (
            "high_official_level_plus_two_public_sources"
            if public_support_count >= 2
            else "high_official_level_plus_public_source"
        )
    return (
        "medium_legacy_official_stage_plus_two_public_sources"
        if public_support_count >= 2
        else "medium_legacy_official_stage_plus_public_source"
    )


def build_books(
    level_rows: dict[int, list[dict[str, Any]]],
    koreantopik_index: dict[str, list[dict[str, Any]]],
    curriculum_index: dict[str, list[dict[str, Any]]],
    nikl_index: dict[str, list[dict[str, Any]]],
    project_index: dict[str, list[dict[str, Any]]],
    lower_words: set[str],
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    candidates: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"topikindepth_matches": [], "koreantopik_matches": []}
    )
    for level in range(3, 7):
        for row in level_rows[level]:
            candidates[row["korean"]]["topikindepth_matches"].append(row)
    for korean, matches in koreantopik_index.items():
        candidates[korean]["koreantopik_matches"].extend(matches)

    assigned: dict[str, list[dict[str, Any]]] = {
        "topik_intermediate": [],
        "topik_advanced": [],
    }
    exclusions: list[dict[str, Any]] = []
    for korean in sorted(candidates):
        evidence = candidates[korean]
        tid_matches = sorted(
            evidence["topikindepth_matches"],
            key=lambda item: (item["topik_sublevel"], item["source_position"]),
        )
        kt_matches = sorted(
            evidence["koreantopik_matches"], key=lambda item: item["source_no"]
        )
        public_source_keys = []
        if tid_matches:
            public_source_keys.append("topikindepth_level_3_to_6")
        if kt_matches:
            public_source_keys.append(KOREANTOPIK_SOURCE.key)

        exclusion_base = {
            "korean": korean,
            "topikindepth_sublevels": sorted(
                {item["topik_sublevel"] for item in tid_matches}
            ),
            "koreantopik_source_numbers": sorted(
                {item["source_no"] for item in kt_matches}
            ),
            "public_sources": public_source_keys,
        }
        if korean in lower_words:
            exclusions.append(
                {**exclusion_base, "reason": "already_owned_by_topik_beginner_wordbook"}
            )
            continue
        if korean in SENSE_ALIGNMENT_EXCLUSIONS:
            exclusions.append(
                {**exclusion_base, **SENSE_ALIGNMENT_EXCLUSIONS[korean]}
            )
            continue

        curriculum_matches = curriculum_index.get(korean, [])
        nikl_matches = nikl_index.get(korean, [])
        curriculum_grades = sorted(
            {match["grade"] for match in curriculum_matches}, key=curriculum_level
        )
        old_grades = sorted({match["grade"] for match in nikl_matches})

        book = ""
        assignment_basis = ""
        if curriculum_grades:
            minimum_level = min(curriculum_level(grade) for grade in curriculum_grades)
            if minimum_level <= 2:
                exclusions.append(
                    {
                        **exclusion_base,
                        "curriculum_grades": curriculum_grades,
                        "reason": "nikl_2017_minimum_level_is_1_or_2",
                    }
                )
                continue
            book = "topik_intermediate" if minimum_level <= 4 else "topik_advanced"
            assignment_basis = f"nikl_2017_minimum_level_{minimum_level}"
        elif "A" in old_grades:
            exclusions.append(
                {
                    **exclusion_base,
                    "nikl_2003_grades": old_grades,
                    "reason": "nikl_2003_minimum_stage_is_A",
                }
            )
            continue
        elif "B" in old_grades:
            book = "topik_intermediate"
            assignment_basis = "nikl_2003_grade_B_without_2017_match"
        elif "C" in old_grades:
            book = "topik_advanced"
            assignment_basis = "nikl_2003_grade_C_without_2017_match"
        else:
            exclusions.append(
                {
                    **exclusion_base,
                    "reason": "public_topik_source_only_without_nikl_level_support",
                }
            )
            continue

        project_matches = project_index.get(korean, [])
        primary_tid = tid_matches[0] if tid_matches else {}
        primary_kt = kt_matches[0] if kt_matches else {}
        public_support_count = len(public_source_keys)
        target_tid_levels = {3, 4} if book == "topik_intermediate" else {5, 6}
        review_flags: list[str] = []
        if len(curriculum_grades) > 1:
            review_flags.append("multiple_nikl_2017_levels_keep_minimum_for_merged_homograph")
        if tid_matches and not (
            {item["topik_sublevel"] for item in tid_matches} & target_tid_levels
        ):
            review_flags.append("public_sublevel_differs_from_official_assignment")
        if not assignment_basis.startswith("nikl_2017"):
            review_flags.append("assignment_uses_legacy_nikl_2003_stage")
        if public_support_count == 1:
            review_flags.append("single_public_topik_source")
        if not primary_tid:
            review_flags.append("needs_chinese_gloss_and_romanization_from_official_dictionary")
        if not project_matches:
            review_flags.append("needs_new_project_metadata")

        record = {
            "id": 0,
            "korean": korean,
            "topik_sublevel": primary_tid.get("topik_sublevel"),
            "topikindepth_sublevels": sorted(
                {item["topik_sublevel"] for item in tid_matches}
            ),
            "source_position": primary_tid.get(
                "source_position", primary_kt.get("source_no")
            ),
            "source_key": primary_tid.get("source_key", KOREANTOPIK_SOURCE.key),
            "source_url": primary_tid.get("source_url", KOREANTOPIK_SOURCE.url),
            "romanization_source": primary_tid.get("romanization_source", ""),
            "meaning_zh_source": primary_tid.get("meaning_zh_source", ""),
            "meaning_en_source": primary_kt.get("meaning_en_source", ""),
            "entry_url": primary_tid.get("entry_url", ""),
            "topikindepth_matches": tid_matches,
            "koreantopik_matches": kt_matches,
            "public_source_support_count": public_support_count,
            "level_assignment_basis": assignment_basis,
            "sources": [
                *(item["source_key"] for item in tid_matches),
                *([KOREANTOPIK_SOURCE.key] if kt_matches else []),
                *(f"nikl_standard_curriculum_level_{grade}" for grade in curriculum_grades),
                *(f"nikl_learning_vocab_grade_{grade}" for grade in old_grades),
            ],
            "nikl_curriculum_matches": curriculum_matches,
            "nikl_matches": nikl_matches,
            "project_vocab_matches": project_matches,
            "source_confidence": confidence_for(assignment_basis, public_support_count),
            "metadata_status": (
                "covered_by_project_vocab"
                if project_matches
                else (
                    "needs_new_entry_metadata_with_chinese_source"
                    if primary_tid
                    else "needs_official_dictionary_metadata"
                )
            ),
            "review_flags": review_flags,
        }
        assigned[book].append(record)

    def finish(book: str, levels: tuple[int, int], level_cn: str) -> dict[str, Any]:
        words = sorted(
            assigned[book],
            key=lambda item: (
                0 if item["level_assignment_basis"].startswith("nikl_2017") else 1,
                item["level_assignment_basis"],
                item["korean"],
            ),
        )
        for index, word in enumerate(words, start=1):
            word["id"] = index
        return {
            "level": f"{book}_source_pool",
            "level_cn": f"{level_cn}源词池",
            "status": "evidence_classified_source_pool_not_final_wordbook",
            "generated_at": TODAY,
            "sublevels": list(levels),
            "assignment_rule": (
                "public TOPIK II evidence plus NIKL 2017 minimum homograph level; "
                "fallback to NIKL 2003 B/C only when absent from 2017"
            ),
            "official_boundary_sources": [
                source.__dict__ for source in OFFICIAL_BOUNDARY_SOURCES
            ],
            "official_learning_vocab_source": NIKL_SOURCE.__dict__,
            "official_standard_curriculum_source": NIKL_CURRICULUM_SOURCE.__dict__,
            "public_level_sources": [
                TOPIK_IN_DEPTH_SOURCES[level].__dict__ for level in range(3, 7)
            ],
            "public_topik_ii_source": KOREANTOPIK_SOURCE.__dict__,
            "total": len(words),
            "words": words,
        }

    return (
        finish("topik_intermediate", (3, 4), "TOPIK中级（3-4级）"),
        finish("topik_advanced", (5, 6), "TOPIK高级（5-6级）"),
        exclusions,
    )


def book_stats(book: dict[str, Any]) -> dict[str, Any]:
    words = book["words"]
    return {
        "total": len(words),
        "topikindepth_sublevels": dict(
            Counter(
                str(level)
                for word in words
                for level in word["topikindepth_sublevels"]
            )
        ),
        "public_source_support_count": dict(
            Counter(str(word["public_source_support_count"]) for word in words)
        ),
        "level_assignment_basis": dict(
            Counter(word["level_assignment_basis"] for word in words)
        ),
        "source_confidence": dict(Counter(word["source_confidence"] for word in words)),
        "metadata_status": dict(Counter(word["metadata_status"] for word in words)),
        "nikl_grades": dict(
            Counter(
                grade
                for word in words
                for grade in {match["grade"] for match in word["nikl_matches"]}
            )
        ),
        "nikl_2017_levels": dict(
            Counter(
                grade
                for word in words
                for grade in {match["grade"] for match in word["nikl_curriculum_matches"]}
            )
        ),
        "review_flags": dict(Counter(flag for word in words for flag in word["review_flags"])),
    }


def write_report(
    snapshot: dict[str, Any],
    level_rows: dict[int, list[dict[str, Any]]],
    koreantopik_audit: dict[str, Any],
    source_exclusions: list[dict[str, Any]],
    intermediate: dict[str, Any],
    advanced: dict[str, Any],
    book_exclusions: list[dict[str, Any]],
) -> None:
    inter_stats = book_stats(intermediate)
    adv_stats = book_stats(advanced)
    legacy_inter = [
        word
        for word in intermediate["words"]
        if word["level_assignment_basis"].startswith("nikl_2003")
    ]
    legacy_adv = [
        word
        for word in advanced["words"]
        if word["level_assignment_basis"].startswith("nikl_2003")
    ]

    def preview_rows(words: list[dict[str, Any]], limit: int = 40) -> list[str]:
        return [
            f"| {word['id']} | {word['korean']} | {word['topik_sublevel']} | "
            f"{word['meaning_zh_source'] or word['meaning_en_source']} | "
            f"{word['level_assignment_basis']} | {', '.join(word['review_flags'])} |"
            for word in words[:limit]
        ]

    lines = [
        "# TOPIK中高级词汇来源审计",
        "",
        f"> 创建日期：{TODAY}",
        f"> 最后更新：{TODAY}",
        "> 状态：源词池已建立 / 分级与排除审计通过",
        "> 用途：记录TOPIK 3-6级词汇的官方边界、逐词来源、清洗规则、覆盖情况和局限",
        "",
        "---",
        "",
        "## 一、结论边界",
        "",
        "TOPIK官方公开考试结构、等级和分数区间，但不发布一份唯一固定的3-6级逐词考纲。因此本项目不能把任何第三方逐词表称为“TOPIK官方词表”。",
        "",
        "本次采用分层证据：NIIED/中国教育考试网确认TOPIK II等级边界；国立国语院2017标准课程词表提供官方1-6级逐词分级；国立国语院2003年5965词提供历史学习阶段；TOPIK in Depth 3-6级与KoreanTopik TOPIK II 3900词表提供两套独立的考试相关候选证据。",
        "",
        "## 二、来源",
        "",
        "| 来源 | 性质 | 用途 |",
        "|------|------|------|",
    ]
    for source in OFFICIAL_BOUNDARY_SOURCES:
        lines.append(f"| [{source.name}]({source.url}) | {source.source_type} | 等级与考试边界 |")
    lines.append(
        f"| [{NIKL_CURRICULUM_SOURCE.name}]({NIKL_CURRICULUM_SOURCE.url}) | "
        f"{NIKL_CURRICULUM_SOURCE.source_type} | 主要官方1-6级逐词分级与词性支持 |"
    )
    lines.append(
        f"| [{NIKL_SOURCE.name}]({NIKL_SOURCE.url}) | {NIKL_SOURCE.source_type} | "
        "候选词官方学习阶段与词性支持 |"
    )
    for level in range(3, 7):
        source = TOPIK_IN_DEPTH_SOURCES[level]
        lines.append(f"| [{source.name}]({source.url}) | {source.source_type} | {level}级逐词候选 |")
    lines.append(
        f"| [{KOREANTOPIK_SOURCE.name}]({KOREANTOPIK_SOURCE.url}) | "
        f"{KOREANTOPIK_SOURCE.source_type} | 独立TOPIK II候选佐证与英文释义 |"
    )

    lines += [
        "",
        "国立国语院2003词表附件抓取日期：2026-08-01；SHA-256："
        f"`{snapshot['source']['file_sha256']}`。原表5965条：A 982、B 2111、C 2872；去除同形异义编号后为"
        f"{snapshot['unique_korean_after_homonym_suffix_removal']}个韩语词形。",
        "",
        "国立国语院2017标准课程附件抓取日期：2026-08-01；SHA-256："
        f"`{snapshot['standard_curriculum_source']['file_sha256']}`。原表10635条：1级735、2级1100、3级1655、4级2200、5级2365、6级2580；去除同形异义编号后为"
        f"{snapshot['standard_curriculum_unique_korean_after_homonym_suffix_removal']}个韩语词形。",
        "",
        "KoreanTopik页面宣称3900词，但本次逐页解析得到"
        f"{koreantopik_audit['raw_rows']}行、{koreantopik_audit['unique_source_numbers']}个不同编号、"
        f"{koreantopik_audit['accepted_unique_pure_hangul']}个纯韩文去重词形；缺失编号"
        f"{len(koreantopik_audit['missing_source_numbers'])}个，重复编号"
        f"{len(koreantopik_audit['duplicate_source_numbers'])}个。因此它只作为公开佐证，不按宣传数量视为完整原表。",
        "",
        "局限：两份国立国语院名单都是韩国语学习者通用课程/词汇分级，不等于TOPIK逐词考纲；两套TOPIK逐词来源都是公开整理站点，不是考试官方。交叉使用能提高可信度，但不能消除逐词复核责任。",
        "",
        "## 三、清洗规则",
        "",
        "1. 只保留纯韩文词条；以连字符开头的语法形式、空格短语、数字或符号项不进入背词词书。",
        "2. 同形异义词合并学习，按2017官方课程中最早等级归属，避免同一个韩语词形跨词书重复。",
        "3. 与TOPIK初级重复的词不再进入中高级词书；2017官方1/2级或2003旧表A阶段词也不提升到中高级。",
        "4. 候选词必须同时具备公开TOPIK II证据与官方学习等级证据：2017课程3/4级归中级、5/6级归高级；2017未收录时才回退到2003旧表B/C阶段。只有公开站点支持的词保留在审计排除池。",
        "5. 公开释义与官方等级证据明显指向不同同形义项时，须用《标准国语大辞典》复核；无法对齐或发生跨级错配的词进入审计排除池。",
        "6. 现有项目词库只用于复用已校对的释义、词性和发音，不作为TOPIK来源证据。",
        "",
        "## 四、源词池统计",
        "",
        "```json",
        json.dumps(
            {
                "topikindepth_parsed": {str(level): len(level_rows[level]) for level in range(3, 7)},
                "koreantopik_integrity": {
                    "advertised_total": koreantopik_audit["advertised_total"],
                    "raw_rows": koreantopik_audit["raw_rows"],
                    "unique_source_numbers": koreantopik_audit["unique_source_numbers"],
                    "accepted_unique_pure_hangul": koreantopik_audit["accepted_unique_pure_hangul"],
                    "missing_source_number_count": len(koreantopik_audit["missing_source_numbers"]),
                    "duplicate_source_numbers": koreantopik_audit["duplicate_source_numbers"],
                },
                "topik_intermediate": inter_stats,
                "topik_advanced": adv_stats,
                "source_exclusions": dict(Counter(item["reason"] for item in source_exclusions)),
                "book_exclusions": dict(Counter(item["reason"] for item in book_exclusions)),
            },
            ensure_ascii=False,
            indent=2,
        ),
        "```",
        "",
        "## 五、中级使用2003旧表回退分级的待复核词（前40条）",
        "",
        "| ID | 韩语 | 公开子级 | 释义来源 | 分级依据 | 标记 |",
        "|----|------|----------|----------|----------|------|",
        *(preview_rows(legacy_inter) or ["| - | - | - | - | - | - |"]),
        "",
        "## 六、高级使用2003旧表回退分级的待复核词（前40条）",
        "",
        "| ID | 韩语 | 公开子级 | 释义来源 | 分级依据 | 标记 |",
        "|----|------|----------|----------|----------|------|",
        *(preview_rows(legacy_adv) or ["| - | - | - | - | - | - |"]),
        "",
        "## 七、未采用材料",
        "",
        "项目旧文件 `韩语-小程序/TOPIK词汇.pdf` 含大量变形、短语、词性错误和过度展开释义，仅保留为历史参考，不参与本轮候选纳入和字段定稿。",
        "",
        "## 八、下一步",
        "",
        "1. 对待新编词补齐并审计中文释义、韩国国语罗马字发音和词性。",
        "2. 逐条处理单公开来源、官方阶段不一致和同形多词性记录。",
        "3. 生成中级/高级Word、JSON和quiz后执行结构、重复、释义冲突、发音和干扰项校验。",
        "4. 在全部校验完成前，源词池不得命名或宣传为最终词书。",
        "",
    ]
    (DOC_DIR / "TOPIK中高级词汇来源审计.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if not NIKL_SNAPSHOT.exists():
        raise FileNotFoundError(
            f"缺少国立国语院来源快照：{NIKL_SNAPSHOT}。"
            "请先运行 extract_nikl_learning_vocab.ps1。"
        )

    snapshot = read_json(NIKL_SNAPSHOT)
    nikl_index = load_nikl_index(snapshot)
    curriculum_index = load_curriculum_index(snapshot)
    project_index = load_project_vocab()
    lower_words = lower_topik_words()

    level_rows: dict[int, list[dict[str, Any]]] = {}
    source_exclusions: list[dict[str, Any]] = []
    for level in range(3, 7):
        rows, exclusions = fetch_level(level)
        level_rows[level] = rows
        source_exclusions.extend(exclusions)

    koreantopik_index, koreantopik_audit = fetch_koreantopik()
    source_exclusions.extend(koreantopik_audit["excluded_rows"])
    intermediate, advanced, book_exclusions = build_books(
        level_rows,
        koreantopik_index,
        curriculum_index,
        nikl_index,
        project_index,
        lower_words,
    )

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DOC_DIR.mkdir(parents=True, exist_ok=True)
    write_json(DATA_DIR / "topik_intermediate_source_pool.json", intermediate)
    write_json(DATA_DIR / "topik_advanced_source_pool.json", advanced)

    audit = {
        "status": "source_audit_not_final_wordbook",
        "generated_at": TODAY,
        "official_boundary_sources": [source.__dict__ for source in OFFICIAL_BOUNDARY_SOURCES],
        "official_learning_vocab_source": {
            **NIKL_SOURCE.__dict__,
            "retrieved_at": snapshot["retrieved_at"],
            "file_sha256": snapshot["source"]["file_sha256"],
            "raw_total": snapshot["raw_total"],
            "grade_counts": snapshot["grade_counts"],
        },
        "official_standard_curriculum_source": {
            **NIKL_CURRICULUM_SOURCE.__dict__,
            "retrieved_at": snapshot["retrieved_at"],
            "file_sha256": snapshot["standard_curriculum_source"]["file_sha256"],
            "raw_total": snapshot["standard_curriculum_raw_total"],
            "grade_counts": snapshot["standard_curriculum_grade_counts"],
        },
        "public_level_sources": [TOPIK_IN_DEPTH_SOURCES[level].__dict__ for level in range(3, 7)],
        "public_topik_ii_source": KOREANTOPIK_SOURCE.__dict__,
        "koreantopik_integrity_audit": koreantopik_audit,
        "source_counts": {
            str(level): {
                "advertised": EXPECTED_COUNTS[level],
                "accepted_pure_hangul": len(level_rows[level]),
            }
            for level in range(3, 7)
        },
        "book_stats": {
            "topik_intermediate": book_stats(intermediate),
            "topik_advanced": book_stats(advanced),
        },
        "source_exclusions": source_exclusions,
        "book_exclusions": book_exclusions,
    }
    write_json(DATA_DIR / "topik_ii_source_audit.json", audit)
    write_report(
        snapshot,
        level_rows,
        koreantopik_audit,
        source_exclusions,
        intermediate,
        advanced,
        book_exclusions,
    )

    print("topik_intermediate", json.dumps(book_stats(intermediate), ensure_ascii=False))
    print("topik_advanced", json.dumps(book_stats(advanced), ensure_ascii=False))
    print("source_exclusions", dict(Counter(item["reason"] for item in source_exclusions)))
    print("book_exclusions", dict(Counter(item["reason"] for item in book_exclusions)))


if __name__ == "__main__":
    main()
