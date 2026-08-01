#!/usr/bin/env python3
"""
同步词库源数据到微信小程序运行数据。

数据源：
  memory-bank/数据文件/{beginner,intermediate,advanced,topik_beginner,
  topik_intermediate,topik_advanced}.json
  memory-bank/数据文件/{beginner,intermediate,advanced,topik_beginner,
  topik_intermediate,topik_advanced}_quiz.json

输出：
  miniprogram/data/*.json
  miniprogram/data/*_v2.js

保留 _v2.js 后缀是为了规避微信开发者工具对旧 JS 模块的缓存干扰。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "memory-bank" / "数据文件"
TARGET_DIR = ROOT / "miniprogram" / "data"
LEVELS = (
    "beginner",
    "intermediate",
    "advanced",
    "topik_beginner",
    "topik_intermediate",
    "topik_advanced",
)


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def dump_json(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def validate_dataset(name: str, data: dict[str, Any]) -> None:
    words = data.get("words")
    total = data.get("total")
    if not isinstance(words, list):
        raise ValueError(f"{name}: words 必须是数组")
    if total != len(words):
        raise ValueError(f"{name}: total={total} 与 words.length={len(words)} 不一致")

    ids = [word.get("id") for word in words if isinstance(word, dict)]
    expected_ids = list(range(1, len(words) + 1))
    if ids != expected_ids:
        raise ValueError(f"{name}: id 必须从 1 开始连续递增")


def write_targets(name: str, data: dict[str, Any]) -> None:
    json_text = dump_json(data)
    (TARGET_DIR / f"{name}.json").write_text(json_text, encoding="utf-8")
    (TARGET_DIR / f"{name}_v2.js").write_text(
        f"module.exports = {json_text}", encoding="utf-8"
    )


def sync_one(name: str) -> tuple[int, int]:
    source_path = SOURCE_DIR / f"{name}.json"
    data = read_json(source_path)
    validate_dataset(name, data)
    write_targets(name, data)

    target_json = read_json(TARGET_DIR / f"{name}.json")
    target_js_text = (TARGET_DIR / f"{name}_v2.js").read_text(encoding="utf-8")
    if not target_js_text.startswith("module.exports = "):
        raise ValueError(f"{name}_v2.js: CommonJS 导出格式异常")
    validate_dataset(f"miniprogram/data/{name}.json", target_json)
    return data["total"], len(data["words"])


def main() -> None:
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    print("同步 miniprogram/data ...")
    for level in LEVELS:
        total, count = sync_one(level)
        quiz_total, quiz_count = sync_one(f"{level}_quiz")
        if total != quiz_total or count != quiz_count:
            raise ValueError(
                f"{level}: 词库({total}) 与 quiz({quiz_total}) 数量不一致"
            )
        print(f"- {level}: {total} 词，quiz {quiz_total} 条")

    print("完成：JSON 与 *_v2.js 已同步。")


if __name__ == "__main__":
    main()
