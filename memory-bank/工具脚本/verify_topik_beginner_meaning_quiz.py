#!/usr/bin/env python3
"""
Verify TOPIK beginner source words against existing project meanings and quiz data.

This verifies what is currently verifiable:
- Korean spelling shape, duplicate status and source support in the unified source pool.
- For words already covered by project vocabulary, the matching project entry exists.
- For covered words with existing quiz data, distractors do not duplicate the correct
  meaning or Korean spelling.

Words marked needs_new_entry_review do not yet have final Chinese meaning, POS,
pronunciation or quiz data, so they are explicitly reported as not yet verifiable.
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


def load_project_vocab() -> dict[tuple[str, int], dict[str, Any]]:
    out: dict[tuple[str, int], dict[str, Any]] = {}
    for level in ["beginner", "intermediate", "advanced"]:
        data = read_json(DATA_DIR / f"{level}.json")
        for word in data.get("words", []):
            out[(level, word["id"])] = word
    return out


def load_project_quiz() -> dict[tuple[str, int], dict[str, Any]]:
    out: dict[tuple[str, int], dict[str, Any]] = {}
    for level in ["beginner", "intermediate", "advanced"]:
        path = DATA_DIR / f"{level}_quiz.json"
        if not path.exists():
            continue
        data = read_json(path)
        for word in data.get("words", []):
            out[(level, word["id"])] = word
    return out


def first_project_match(word: dict[str, Any]) -> dict[str, Any] | None:
    matches = word.get("project_vocab_matches") or []
    if not matches:
        return None
    return matches[0]


def verify() -> dict[str, Any]:
    source = read_json(DATA_DIR / "topik_beginner_cleaned_source_pool.json")
    project_vocab = load_project_vocab()
    project_quiz = load_project_quiz()

    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    covered_records: list[dict[str, Any]] = []
    pending_records: list[dict[str, Any]] = []

    words = source.get("words", [])
    seen: set[str] = set()
    duplicate_words: list[str] = []

    for word in words:
        korean = word.get("korean", "")
        record_base = {
            "id": word.get("id"),
            "korean": korean,
            "source_sublevel": word.get("source_sublevel"),
            "sources": word.get("sources", []),
            "source_confidence": word.get("source_confidence"),
            "metadata_coverage": word.get("metadata_coverage"),
        }

        if not HANGUL_RE.fullmatch(korean):
            errors.append({**record_base, "type": "invalid_korean_spelling_shape"})
        if korean in seen:
            duplicate_words.append(korean)
            errors.append({**record_base, "type": "duplicate_korean"})
        seen.add(korean)
        if not word.get("sources"):
            errors.append({**record_base, "type": "missing_external_source"})

        match = first_project_match(word)
        if word.get("metadata_coverage") == "needs_new_entry_review":
            pending_records.append(
                {
                    **record_base,
                    "required_work": [
                        "Chinese meaning",
                        "Korean POS",
                        "Chinese POS",
                        "Revised Romanization pronunciation",
                        "3 quiz distractors",
                    ],
                    "verification_status": "not_yet_verifiable_no_final_entry",
                }
            )
            continue

        if not match:
            errors.append({**record_base, "type": "covered_but_missing_project_match"})
            continue

        key = (match["level"], match["id"])
        vocab_entry = project_vocab.get(key)
        quiz_entry = project_quiz.get(key)
        if not vocab_entry:
            errors.append({**record_base, "type": "project_vocab_match_not_found", "match": match})
            continue
        if vocab_entry.get("korean") != korean:
            errors.append(
                {
                    **record_base,
                    "type": "project_vocab_korean_mismatch",
                    "match": match,
                    "project_korean": vocab_entry.get("korean"),
                }
            )

        meaning = vocab_entry.get("meaning", "")
        if not meaning:
            errors.append({**record_base, "type": "empty_correct_meaning", "match": match})
        for required in ["pronunciation", "pos", "pos_cn"]:
            if not vocab_entry.get(required):
                errors.append({**record_base, "type": f"empty_{required}", "match": match})

        quiz_status = "verified"
        distractors = []
        if not quiz_entry:
            quiz_status = "missing_quiz"
            errors.append({**record_base, "type": "missing_project_quiz", "match": match})
        else:
            if quiz_entry.get("korean") != korean:
                errors.append(
                    {
                        **record_base,
                        "type": "quiz_korean_mismatch",
                        "match": match,
                        "quiz_korean": quiz_entry.get("korean"),
                    }
                )
            if quiz_entry.get("meaning") != meaning:
                errors.append(
                    {
                        **record_base,
                        "type": "quiz_correct_meaning_mismatch",
                        "match": match,
                        "quiz_meaning": quiz_entry.get("meaning"),
                        "project_meaning": meaning,
                    }
                )
            distractors = quiz_entry.get("distractors", [])
            if len(distractors) != 3:
                errors.append(
                    {
                        **record_base,
                        "type": "distractor_count_not_3",
                        "match": match,
                        "count": len(distractors),
                    }
                )
            seen_distractor_meanings: set[str] = set()
            for index, distractor in enumerate(distractors, start=1):
                d_meaning = distractor.get("meaning", "")
                d_korean = distractor.get("korean", "")
                if not d_meaning or not d_korean:
                    errors.append(
                        {
                            **record_base,
                            "type": "empty_distractor_field",
                            "match": match,
                            "distractor_index": index,
                        }
                    )
                if d_meaning == meaning:
                    errors.append(
                        {
                            **record_base,
                            "type": "distractor_meaning_equals_correct",
                            "match": match,
                            "distractor_index": index,
                            "meaning": meaning,
                        }
                    )
                if d_korean == korean:
                    errors.append(
                        {
                            **record_base,
                            "type": "distractor_korean_equals_correct",
                            "match": match,
                            "distractor_index": index,
                            "korean": korean,
                        }
                    )
                if d_meaning in seen_distractor_meanings:
                    warnings.append(
                        {
                            **record_base,
                            "type": "duplicate_distractor_meaning",
                            "match": match,
                            "distractor_index": index,
                            "meaning": d_meaning,
                        }
                    )
                seen_distractor_meanings.add(d_meaning)

        covered_records.append(
            {
                **record_base,
                "project_match": match,
                "correct_meaning": meaning,
                "pos_cn": vocab_entry.get("pos_cn", ""),
                "pronunciation": vocab_entry.get("pronunciation", ""),
                "quiz_status": quiz_status,
                "distractor_count": len(distractors),
                "verification_status": "programmatically_verified_against_project_vocab_and_quiz",
            }
        )

    summary = {
        "audit_date": date.today().isoformat(),
        "source_file": "memory-bank/数据文件/topik_beginner_cleaned_source_pool.json",
        "status": "partial_verification_complete_final_wordbook_not_generated",
        "total_words": len(words),
        "unique_korean_words": len(seen),
        "duplicate_korean_count": len(duplicate_words),
        "metadata_coverage": dict(Counter(w.get("metadata_coverage") for w in words)),
        "source_confidence": dict(Counter(w.get("source_confidence") for w in words)),
        "covered_words_verified_count": len(covered_records),
        "pending_new_entry_count": len(pending_records),
        "errors_count": len(errors),
        "warnings_count": len(warnings),
    }

    return {
        "summary": summary,
        "errors": errors,
        "warnings": warnings,
        "covered_records": covered_records,
        "pending_new_entry_records": pending_records,
    }


def write_report(result: dict[str, Any]) -> None:
    summary = result["summary"]
    pending_sample = result["pending_new_entry_records"][:80]
    error_rows = result["errors"][:80]

    pending_rows = "\n".join(
        f"| {r['id']} | {r['korean']} | {r['source_confidence']} | {', '.join(r['sources'])} |"
        for r in pending_sample
    )
    error_table = "\n".join(
        f"| {e.get('id', '')} | {e.get('korean', '')} | {e.get('type', '')} |"
        for e in error_rows
    )

    lines = [
        "# TOPIK 初级释义与测验选项核对报告",
        "",
        f"> 创建日期：{summary['audit_date']}",
        f"> 最后更新：{summary['audit_date']}",
        "> 状态：已核对现有覆盖词 / 新词待编写后再核对",
        "> 用途：核对 TOPIK 初级统一源词表中韩语拼写、项目释义、quiz 正确项与干扰项冲突",
        "",
        "---",
        "",
        "## 一、结论",
        "",
        f"- TOPIK 初级统一源词表：{summary['total_words']} 词。",
        f"- 韩语去重后：{summary['unique_korean_words']} 词。",
        f"- 重复韩语词：{summary['duplicate_korean_count']}。",
        f"- 已有项目词库覆盖并完成程序核对：{summary['covered_words_verified_count']} 词。",
        f"- 尚未生成正式释义/发音/quiz，不能完成语义核对：{summary['pending_new_entry_count']} 词。",
        f"- 程序错误：{summary['errors_count']} 条。",
        f"- 警告：{summary['warnings_count']} 条。",
        "",
        "本轮能确认的是：已有项目词库覆盖的词，其韩语拼写与项目词条一致；正确释义来自项目词库；quiz 正确项与项目释义一致；3个干扰项不会与正确释义或正确韩语词相同。尚未新编的词不能假装已经完成释义和干扰项核对。",
        "",
        "## 二、统计",
        "",
        "```json",
        json.dumps(summary, ensure_ascii=False, indent=2),
        "```",
        "",
        "## 三、待新编词样例（前80条）",
        "",
        "| ID | 韩语 | 来源置信度 | 来源 |",
        "|----|------|------------|------|",
        pending_rows or "| - | - | - | - |",
        "",
        "## 四、错误样例（前80条）",
        "",
        "| ID | 韩语 | 错误类型 |",
        "|----|------|----------|",
        error_table or "| - | - | 无 |",
        "",
        "## 五、下一步",
        "",
        "1. 先为 814 个待新编词生成正式中文释义、词性、发音和 quiz。",
        "2. 每批新增后重新运行 `verify_topik_beginner_meaning_quiz.py`。",
        "3. 若出现 `distractor_meaning_equals_correct` 或 `distractor_korean_equals_correct`，该批不得进入正式词书。",
        "",
    ]
    (DOC_DIR / "TOPIK初级释义与测验选项核对报告.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    result = verify()
    write_json(DATA_DIR / "topik_beginner_meaning_quiz_audit.json", result)
    write_report(result)
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    if result["summary"]["errors_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
