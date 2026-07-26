#!/usr/bin/env python3
"""Generate TOPIK beginner JSON data from the final delivery Word document."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from docx import Document


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DOCX = ROOT / "memory-bank" / "数据文件" / "TOPIK初级词汇_最终交付版.docx"
SOURCE_DIR = ROOT / "memory-bank" / "数据文件"
TARGET_DIR = ROOT / "miniprogram" / "data"

LEVEL = "topik_beginner"
LEVEL_CN = "TOPIK初级"
DESCRIPTION = "TOPIK I（1~2级）初级核心词汇，独立词书，基于 TOPIK 初级词汇最终交付 Word 文档生成"

HEADERS = ["序号", "韩语", "发音", "词性", "中文释义", "干扰1", "干扰2", "干扰3", "批次"]
POS_CN_MAP = {
    "명사": "名词",
    "동사": "动词",
    "형용사": "形容词",
    "부사": "副词",
    "감탄사": "感叹词",
    "조사": "助词",
    "관형사": "冠形词",
    "대명사": "代词",
    "수사": "数词",
    "접속사": "连接词",
}
MEANING_ALIASES = {
    "首尔": "首都；首尔",
    "济州岛": "济州道；济州岛",
    "热的": "热（天气）的",
}


def cell_text(cell) -> str:
    return cell.text.replace("\xa0", " ").strip()


def split_pos(value: str) -> tuple[str, str]:
    parts = [part.strip() for part in value.split("/") if part.strip()]
    pos = parts[0] if parts else value.strip()
    pos_cn = parts[1] if len(parts) > 1 else POS_CN_MAP.get(pos, "")
    if not pos or not pos_cn:
        raise ValueError(f"无法解析词性: {value!r}")
    return pos, pos_cn


def load_rows() -> list[dict[str, str]]:
    if not SOURCE_DOCX.exists():
        raise FileNotFoundError(SOURCE_DOCX)

    doc = Document(str(SOURCE_DOCX))
    target_table = None
    for table in doc.tables:
        first_row = [cell_text(cell) for cell in table.rows[0].cells]
        if first_row[: len(HEADERS)] == HEADERS:
            target_table = table
            break

    if target_table is None:
        raise ValueError("未找到 TOPIK 最终交付表格")

    rows: list[dict[str, str]] = []
    for row in target_table.rows[1:]:
        cells = [cell_text(cell) for cell in row.cells]
        if not any(cells):
            continue
        if len(cells) < len(HEADERS):
            raise ValueError(f"列数不足: {cells}")
        rows.append(dict(zip(HEADERS, cells[: len(HEADERS)])))
    return rows


def validate_basic(rows: list[dict[str, str]]) -> None:
    if len(rows) != 1786:
        raise ValueError(f"TOPIK 初级词数应为 1786，实际为 {len(rows)}")

    expected_ids = list(range(1, len(rows) + 1))
    actual_ids = [int(row["序号"]) for row in rows]
    if actual_ids != expected_ids:
        raise ValueError("序号不是从 1 开始连续递增")

    required = ["韩语", "发音", "词性", "中文释义", "干扰1", "干扰2", "干扰3"]
    for row in rows:
        row_id = int(row["序号"])
        for key in required:
            if not row[key]:
                raise ValueError(f"第 {row_id} 行字段为空: {key}")
        distractors = [row["干扰1"], row["干扰2"], row["干扰3"]]
        if len(set(distractors)) != 3:
            raise ValueError(f"第 {row_id} 行干扰项重复: {distractors}")
        if row["中文释义"] in distractors:
            raise ValueError(f"第 {row_id} 行干扰项与正确释义相同: {row['中文释义']}")


def build_data(rows: list[dict[str, str]]) -> tuple[dict, dict, dict]:
    meaning_to_korean: dict[str, list[str]] = defaultdict(list)
    normalized_meaning_to_korean: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        meaning_to_korean[row["中文释义"]].append(row["韩语"])
        normalized_meaning_to_korean[normalize_meaning(row["中文释义"])].append(row["韩语"])

    words = []
    quiz_words = []
    unresolved: list[tuple[int, str]] = []
    alias_matches: list[tuple[int, str, str, list[str]]] = []
    ambiguous: list[tuple[int, str, list[str]]] = []
    normalized_matches: list[tuple[int, str, list[str]]] = []

    for row in rows:
        word_id = int(row["序号"])
        pos, pos_cn = split_pos(row["词性"])
        word = {
            "id": word_id,
            "korean": row["韩语"],
            "pronunciation": row["发音"],
            "pos": pos,
            "pos_cn": pos_cn,
            "meaning": row["中文释义"],
        }
        words.append(word)

        distractors = []
        for key in ("干扰1", "干扰2", "干扰3"):
            meaning = row[key]
            candidates = meaning_to_korean.get(meaning, [])
            alias = MEANING_ALIASES.get(meaning)
            if not candidates and alias:
                candidates = meaning_to_korean.get(alias, [])
                if candidates:
                    alias_matches.append((word_id, meaning, alias, candidates))
            if not candidates:
                candidates = normalized_meaning_to_korean.get(normalize_meaning(meaning), [])
                if candidates:
                    normalized_matches.append((word_id, meaning, candidates))
            if not candidates:
                unresolved.append((word_id, meaning))
                korean = ""
            else:
                if len(candidates) > 1:
                    ambiguous.append((word_id, meaning, candidates))
                korean = candidates[0]
            distractors.append({"meaning": meaning, "korean": korean})

        quiz_words.append({**word, "distractors": distractors})

    if unresolved:
        preview = unresolved[:10]
        raise ValueError(f"存在无法映射韩语的干扰项: {preview}")

    vocab = {
        "level": LEVEL,
        "level_cn": LEVEL_CN,
        "description": DESCRIPTION,
        "total": len(words),
        "words": words,
    }
    quiz = {
        "level": LEVEL,
        "level_cn": LEVEL_CN,
        "description": "TOPIK 初级词汇四选一测验数据",
        "total": len(quiz_words),
        "format_note": "distractors 为 3 个同词性干扰项，正确答案为 meaning 字段",
        "words": quiz_words,
    }
    audit = {
        "total": len(words),
        "unresolved_distractors": len(unresolved),
        "alias_distractor_matches": len(alias_matches),
        "normalized_distractor_matches": len(normalized_matches),
        "ambiguous_distractor_meanings": len(ambiguous),
        "alias_preview": [
            {
                "id": row_id,
                "meaning": meaning,
                "alias": alias,
                "korean_candidates": candidates,
            }
            for row_id, meaning, alias, candidates in alias_matches[:20]
        ],
        "normalized_preview": [
            {"id": row_id, "meaning": meaning, "korean_candidates": candidates}
            for row_id, meaning, candidates in normalized_matches[:20]
        ],
        "ambiguous_preview": [
            {"id": row_id, "meaning": meaning, "korean_candidates": candidates}
            for row_id, meaning, candidates in ambiguous[:20]
        ],
    }
    return vocab, quiz, audit


def normalize_meaning(value: str) -> str:
    text = value.strip()
    if text.endswith("的") and len(text) > 1:
        return text[:-1]
    return text


def validate_output(vocab: dict, quiz: dict) -> None:
    if vocab["total"] != 1786 or quiz["total"] != 1786:
        raise ValueError("输出 total 异常")
    if len(vocab["words"]) != vocab["total"]:
        raise ValueError("词库 words 数量与 total 不一致")
    if len(quiz["words"]) != quiz["total"]:
        raise ValueError("quiz words 数量与 total 不一致")

    expected_ids = list(range(1, vocab["total"] + 1))
    if [word["id"] for word in vocab["words"]] != expected_ids:
        raise ValueError("词库 ID 不连续")
    if [word["id"] for word in quiz["words"]] != expected_ids:
        raise ValueError("quiz ID 不连续")

    vocab_by_id = {word["id"]: word for word in vocab["words"]}
    for word in quiz["words"]:
        base = vocab_by_id[word["id"]]
        for key in ("korean", "pronunciation", "pos", "pos_cn", "meaning"):
            if word[key] != base[key]:
                raise ValueError(f"quiz 第 {word['id']} 行与词库字段不一致: {key}")
        if len(word["distractors"]) != 3:
            raise ValueError(f"quiz 第 {word['id']} 行干扰项不是 3 个")
        meanings = [item["meaning"] for item in word["distractors"]]
        if len(set(meanings)) != 3:
            raise ValueError(f"quiz 第 {word['id']} 行干扰项重复")
        if word["meaning"] in meanings:
            raise ValueError(f"quiz 第 {word['id']} 行干扰项等于正确释义")
        for item in word["distractors"]:
            if not item["meaning"] or not item["korean"]:
                raise ValueError(f"quiz 第 {word['id']} 行干扰项字段为空")


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_outputs(vocab: dict, quiz: dict) -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    outputs = {
        SOURCE_DIR / f"{LEVEL}.json": vocab,
        SOURCE_DIR / f"{LEVEL}_quiz.json": quiz,
        TARGET_DIR / f"{LEVEL}.json": vocab,
        TARGET_DIR / f"{LEVEL}_quiz.json": quiz,
    }
    for path, data in outputs.items():
        write_json(path, data)

    for name, data in ((LEVEL, vocab), (f"{LEVEL}_quiz", quiz)):
        text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        (TARGET_DIR / f"{name}_v2.js").write_text(f"module.exports = {text}", encoding="utf-8")


def main() -> None:
    rows = load_rows()
    validate_basic(rows)
    vocab, quiz, audit = build_data(rows)
    validate_output(vocab, quiz)
    write_outputs(vocab, quiz)

    print(f"generated={LEVEL}")
    print(f"total={vocab['total']}")
    print(f"unresolved_distractors={audit['unresolved_distractors']}")
    print(f"alias_distractor_matches={audit['alias_distractor_matches']}")
    print(f"normalized_distractor_matches={audit['normalized_distractor_matches']}")
    print(f"ambiguous_distractor_meanings={audit['ambiguous_distractor_meanings']}")
    if audit["alias_preview"]:
        print("alias_preview=" + json.dumps(audit["alias_preview"], ensure_ascii=True))
    if audit["normalized_preview"]:
        print("normalized_preview=" + json.dumps(audit["normalized_preview"], ensure_ascii=True))
    if audit["ambiguous_preview"]:
        print("ambiguous_preview=" + json.dumps(audit["ambiguous_preview"], ensure_ascii=True))


if __name__ == "__main__":
    main()
