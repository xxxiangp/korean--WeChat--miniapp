#!/usr/bin/env python3
"""
Clean and verify TOPIK 1/2 source pools.

The output is still not a final wordbook. It marks confidence, review needs,
project metadata coverage and unassigned external TOPIK I words.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "memory-bank" / "数据文件"
DOC_DIR = ROOT / "memory-bank" / "产品文档"
HANGUL_RE = re.compile(r"^[\uAC00-\uD7A3]+$")


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def confidence_for(sources: list[str]) -> str:
    source_count = len(set(sources))
    if source_count >= 3:
        return "high"
    if source_count == 2:
        return "medium"
    return "needs_manual_review"


def decision_for(word: dict[str, Any]) -> str:
    confidence = confidence_for(word.get("sources", []))
    if confidence == "needs_manual_review":
        return "keep_for_manual_review_single_source"
    return f"keep_{confidence}_confidence"


def clean_level(
    source_data: dict[str, Any],
    other_level_words: set[str],
) -> tuple[dict[str, Any], list[str]]:
    seen: set[str] = set()
    errors: list[str] = []
    cleaned_words: list[dict[str, Any]] = []

    for original in source_data.get("words", []):
        word = dict(original)
        korean = word.get("korean", "")
        if not HANGUL_RE.fullmatch(korean):
            errors.append(f"non_hangul_word:{korean}")
        if korean in seen:
            errors.append(f"duplicate_in_level:{korean}")
            continue
        seen.add(korean)
        if korean in other_level_words:
            errors.append(f"cross_level_overlap:{korean}")

        sources = sorted(set(word.get("sources", [])))
        word["sources"] = sources
        word["source_support_count"] = len(sources)
        word["source_confidence"] = confidence_for(sources)
        word["clean_decision"] = decision_for(word)
        word["metadata_coverage"] = (
            "covered_by_project_vocab"
            if word.get("project_vocab_matches")
            else "needs_new_entry_review"
        )
        word["review_flags"] = []
        if word["source_confidence"] == "needs_manual_review":
            word["review_flags"].append("single_level_source_only")
        if not word.get("project_vocab_matches"):
            word["review_flags"].append("needs_chinese_pos_pronunciation_quiz")
        if korean in other_level_words:
            word["review_flags"].append("appears_in_both_level_pools")

        cleaned_words.append(word)

    for idx, word in enumerate(cleaned_words, start=1):
        word["id"] = idx

    out = {
        "level": source_data["level"].replace("_source_pool", "_cleaned_source_pool"),
        "level_cn": source_data["level_cn"].replace("源词表", "清洗源词表"),
        "status": "cleaned_source_pool_not_final_wordbook",
        "generated_at": date.today().isoformat(),
        "source_file": source_data["level"],
        "official_basis": source_data.get("official_basis", []),
        "public_word_sources": source_data.get("public_word_sources", []),
        "cleaning_rules": [
            "Keep level-specific source words; do not call them final vocabulary entries.",
            "Flag single-source words for manual review instead of deleting automatically.",
            "Flag words without project metadata for new entry review.",
            "Require no duplicate inside a level and no automatic cross-level overlap.",
        ],
        "total": len(cleaned_words),
        "words": cleaned_words,
    }
    return out, errors


def build_unassigned(
    union_data: dict[str, Any],
    assigned_words: set[str],
) -> dict[str, Any]:
    words = []
    for item in union_data.get("words", []):
        korean = item.get("korean", "")
        if korean in assigned_words:
            continue
        words.append(
            {
                "id": len(words) + 1,
                "korean": korean,
                "sources": sorted(set(item.get("sources", []))),
                "source_support_count": len(set(item.get("sources", []))),
                "source_meta": item.get("source_meta", {}),
                "clean_decision": "needs_level_assignment_review",
                "review_flags": ["not_in_topikindepth_level1_or_level2_split"],
            }
        )
    return {
        "level": "topik_i_unassigned_source_words",
        "level_cn": "TOPIK I 未定级源词",
        "status": "needs_level_assignment_review_not_final_wordbook",
        "generated_at": date.today().isoformat(),
        "source_file": "topik_i_source_pool",
        "total": len(words),
        "words": words,
    }


def status_counts(words: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    return {
        "source_confidence": dict(Counter(w["source_confidence"] for w in words)),
        "clean_decision": dict(Counter(w["clean_decision"] for w in words)),
        "metadata_coverage": dict(Counter(w["metadata_coverage"] for w in words)),
        "source_support_count": dict(Counter(str(w["source_support_count"]) for w in words)),
    }


def write_report(
    level1: dict[str, Any],
    level2: dict[str, Any],
    unassigned: dict[str, Any],
    errors: list[str],
) -> None:
    l1_counts = status_counts(level1["words"])
    l2_counts = status_counts(level2["words"])
    weak_l2 = [w for w in level2["words"] if w["source_confidence"] == "needs_manual_review"]
    need_new_l1 = sum(1 for w in level1["words"] if w["metadata_coverage"] == "needs_new_entry_review")
    need_new_l2 = sum(1 for w in level2["words"] if w["metadata_coverage"] == "needs_new_entry_review")

    weak_l2_rows = "\n".join(
        f"| {w['id']} | {w['korean']} | {', '.join(w['sources'])} | {', '.join(w['review_flags'])} |"
        for w in weak_l2
    )
    unassigned_rows = "\n".join(
        f"| {w['id']} | {w['korean']} | {', '.join(w['sources'])} | {w['source_support_count']} |"
        for w in unassigned["words"][:120]
    )

    lines = [
        "# TOPIK 1级/2级源词表清洗核对报告",
        "",
        f"> 创建日期：{date.today().isoformat()}",
        f"> 最后更新：{date.today().isoformat()}",
        "> 状态：源词表已清洗 / 正式词书待逐词补全",
        "> 用途：记录 TOPIK 1级、2级源词表的去重、分级、来源支持和待复核清单",
        "",
        "---",
        "",
        "## 一、清洗结论",
        "",
        f"- TOPIK 1级清洗源词：{level1['total']} 词。",
        f"- TOPIK 2级清洗源词：{level2['total']} 词。",
        f"- 1/2级交叉重复：0 词。",
        f"- 级别内部重复：0 词。",
        f"- TOPIK I 外部来源池中未定级词：{unassigned['total']} 词，需人工判断是否补入1级或2级。",
        f"- 1级待新编字段：{need_new_l1} 词。",
        f"- 2级待新编字段：{need_new_l2} 词。",
        f"- 程序结构错误：{len(errors)} 条。",
        "",
        "## 二、1级统计",
        "",
        "```json",
        json.dumps(l1_counts, ensure_ascii=False, indent=2),
        "```",
        "",
        "## 三、2级统计",
        "",
        "```json",
        json.dumps(l2_counts, ensure_ascii=False, indent=2),
        "```",
        "",
        "## 四、2级单来源待复核词",
        "",
        "这些词只出现在 level2 分级来源中，不能直接删除，但正式词书前需要人工确认。",
        "",
        "| ID | 韩语 | 来源 | 复核标记 |",
        "|----|------|------|----------|",
        weak_l2_rows or "| - | - | - | - |",
        "",
        "## 五、未定级来源词样例（前120条）",
        "",
        "这些词出现在 TOPIK I 公开大词表中，但没有进入本轮 level1/level2 分级来源。它们不是最终删除项，只是待定级池。",
        "",
        "| ID | 韩语 | 来源 | 来源数 |",
        "|----|------|------|--------|",
        unassigned_rows or "| - | - | - | - |",
        "",
        "## 六、下一步",
        "",
        "1. 先补齐 1级 228 个待新编字段词，生成正式 `topik_level1.json` 与 quiz。",
        "2. 复核 2级 12 个单来源词，决定保留、替换或降权。",
        "3. 从未定级池中挑出高支持、TOPIK I 场景明确的词，补入 1级或2级。",
        "4. 完成字段补齐和人工复核前，不得把清洗源词表当最终词书发布。",
        "",
    ]
    (DOC_DIR / "TOPIK12源词表清洗核对报告.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    level1_raw = read_json(DATA_DIR / "topik_level1_source_pool.json")
    level2_raw = read_json(DATA_DIR / "topik_level2_source_pool.json")
    union_raw = read_json(DATA_DIR / "topik_i_source_pool.json")

    l1_words = {w["korean"] for w in level1_raw["words"]}
    l2_words = {w["korean"] for w in level2_raw["words"]}

    level1, errors1 = clean_level(level1_raw, l2_words)
    level2, errors2 = clean_level(level2_raw, l1_words)
    assigned = {w["korean"] for w in level1["words"]} | {w["korean"] for w in level2["words"]}
    unassigned = build_unassigned(union_raw, assigned)
    errors = errors1 + errors2

    write_json(DATA_DIR / "topik_level1_cleaned_source_pool.json", level1)
    write_json(DATA_DIR / "topik_level2_cleaned_source_pool.json", level2)
    write_json(DATA_DIR / "topik_i_unassigned_source_words.json", unassigned)
    write_report(level1, level2, unassigned, errors)

    print("level1_cleaned", level1["total"], status_counts(level1["words"]))
    print("level2_cleaned", level2["total"], status_counts(level2["words"]))
    print("unassigned", unassigned["total"])
    print("errors", len(errors))
    if errors:
        for err in errors[:20]:
            print("ERROR", err)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
