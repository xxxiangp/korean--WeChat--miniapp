# TOPIK 初级释义与测验选项核对报告

> 创建日期：2026-07-26
> 最后更新：2026-07-26
> 状态：已核对现有覆盖词 / 新词待编写后再核对
> 用途：核对 TOPIK 初级统一源词表中韩语拼写、项目释义、quiz 正确项与干扰项冲突

---

## 一、结论

- TOPIK 初级统一源词表：1786 词。
- 韩语去重后：1786 词。
- 重复韩语词：0。
- 已有项目词库覆盖并完成程序核对：972 词。
- 尚未生成正式释义/发音/quiz，不能完成语义核对：814 词。
- 程序错误：0 条。
- 警告：0 条。

本轮能确认的是：已有项目词库覆盖的词，其韩语拼写与项目词条一致；正确释义来自项目词库；quiz 正确项与项目释义一致；3个干扰项不会与正确释义或正确韩语词相同。尚未新编的词不能假装已经完成释义和干扰项核对。

## 二、统计

```json
{
  "audit_date": "2026-07-26",
  "source_file": "memory-bank/数据文件/topik_beginner_cleaned_source_pool.json",
  "status": "partial_verification_complete_final_wordbook_not_generated",
  "total_words": 1786,
  "unique_korean_words": 1786,
  "duplicate_korean_count": 0,
  "metadata_coverage": {
    "covered_by_project_vocab": 972,
    "needs_new_entry_review": 814
  },
  "source_confidence": {
    "high": 1237,
    "medium": 537,
    "needs_manual_review": 12
  },
  "covered_words_verified_count": 972,
  "pending_new_entry_count": 814,
  "errors_count": 0,
  "warnings_count": 0
}
```

## 三、待新编词样例（前80条）

| ID | 韩语 | 来源置信度 | 来源 |
|----|------|------------|------|
| 14 | 가족 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 15 | 가지다 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 19 | 감사 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 21 | 값 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 26 | 개월 | medium | koreantopik_1850, topikindepth_level1 |
| 36 | 걸어오다 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 37 | 검은색 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 38 | 것 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 45 | 경치 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 47 | 계시다 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 48 | 계절 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 52 | 고등학생 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 53 | 고맙다 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 55 | 고프다 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 56 | 고향 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 58 | 곳 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 59 | 공 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 60 | 공부 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 64 | 공휴일 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 73 | 구경 | medium | koreantopik_1850, topikindepth_level1 |
| 76 | 구월 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 80 | 그 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 81 | 그거 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 83 | 그곳 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 84 | 그날 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 86 | 그때 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 93 | 그럼 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 94 | 그렇다 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 95 | 그렇지만 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 98 | 그리다 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 100 | 그분 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 101 | 그쪽 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 112 | 깎다 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 119 | 끝내다 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 122 | 나다 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 128 | 나중 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 129 | 날 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 130 | 날다 | medium | koreantopik_1850, topikindepth_level1 |
| 132 | 날짜 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 133 | 남녀 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 134 | 남동생 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 135 | 남자 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 136 | 남쪽 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 138 | 남학생 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 142 | 내다 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 155 | 넷째 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 159 | 노트 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 167 | 눈물 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 171 | 다녀오다 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 172 | 다니다 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 174 | 다른 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 176 | 다섯째 | medium | koreantopik_1850, topikindepth_level1 |
| 180 | 단어 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 186 | 담배 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 189 | 대학 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 191 | 대학생 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 196 | 도시 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 198 | 도착 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 202 | 돕다 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 203 | 동물 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 205 | 동안 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 206 | 동쪽 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 209 | 되다 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 210 | 두 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 212 | 둘째 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 214 | 드리다 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 223 | 때 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 224 | 떠나다 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 227 | 똑같다 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 228 | 똑바로 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 230 | 라디오 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 234 | 마음 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 241 | 말씀 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 242 | 맑다 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 247 | 매일 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 252 | 메뉴 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 253 | 며칠 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 256 | 모든 | medium | koreantopik_1850, topikindepth_level1 |
| 260 | 목욕 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |
| 261 | 몸 | high | koreantopik_1850, tammy_1671, topikindepth_level1 |

## 四、错误样例（前80条）

| ID | 韩语 | 错误类型 |
|----|------|----------|
| - | - | 无 |

## 五、下一步

1. 先为 814 个待新编词生成正式中文释义、词性、发音和 quiz。
2. 每批新增后重新运行 `verify_topik_beginner_meaning_quiz.py`。
3. 若出现 `distractor_meaning_equals_correct` 或 `distractor_korean_equals_correct`，该批不得进入正式词书。
