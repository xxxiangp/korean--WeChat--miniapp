# TOPIK 1级/2级源词表清洗核对报告

> 创建日期：2026-07-26
> 最后更新：2026-07-26
> 状态：源词表已清洗 / 正式词书待逐词补全
> 用途：记录 TOPIK 1级、2级源词表的去重、分级、来源支持和待复核清单

---

## 一、清洗结论

- TOPIK 1级清洗源词：719 词。
- TOPIK 2级清洗源词：1067 词。
- 1/2级交叉重复：0 词。
- 级别内部重复：0 词。
- TOPIK I 外部来源池中未定级词：397 词，需人工判断是否补入1级或2级。
- 1级待新编字段：228 词。
- 2级待新编字段：586 词。
- 程序结构错误：0 条。

## 二、1级统计

```json
{
  "source_confidence": {
    "high": 693,
    "medium": 26
  },
  "clean_decision": {
    "keep_high_confidence": 693,
    "keep_medium_confidence": 26
  },
  "metadata_coverage": {
    "covered_by_project_vocab": 491,
    "needs_new_entry_review": 228
  },
  "source_support_count": {
    "3": 693,
    "2": 26
  }
}
```

## 三、2级统计

```json
{
  "source_confidence": {
    "high": 544,
    "medium": 511,
    "needs_manual_review": 12
  },
  "clean_decision": {
    "keep_high_confidence": 544,
    "keep_medium_confidence": 511,
    "keep_for_manual_review_single_source": 12
  },
  "metadata_coverage": {
    "covered_by_project_vocab": 481,
    "needs_new_entry_review": 586
  },
  "source_support_count": {
    "3": 544,
    "2": 511,
    "1": 12
  }
}
```

## 四、2级单来源待复核词

这些词只出现在 level2 分级来源中，不能直接删除，但正式词书前需要人工确认。

| ID | 韩语 | 来源 | 复核标记 |
|----|------|------|----------|
| 464 | 선물하다 | topikindepth_level2 | single_level_source_only, needs_chinese_pos_pronunciation_quiz |
| 466 | 선생 | topikindepth_level2 | single_level_source_only, needs_chinese_pos_pronunciation_quiz |
| 506 | 쇠고기 | topikindepth_level2 | single_level_source_only, needs_chinese_pos_pronunciation_quiz |
| 542 | 식사하다 | topikindepth_level2 | single_level_source_only, needs_chinese_pos_pronunciation_quiz |
| 585 | 안녕하다 | topikindepth_level2 | single_level_source_only, needs_chinese_pos_pronunciation_quiz |
| 588 | 않다 | topikindepth_level2 | single_level_source_only, needs_chinese_pos_pronunciation_quiz |
| 599 | 약속하다 | topikindepth_level2 | single_level_source_only |
| 628 | 여행하다 | topikindepth_level2 | single_level_source_only |
| 677 | 요리하다 | topikindepth_level2 | single_level_source_only |
| 678 | 요즈음 | topikindepth_level2 | single_level_source_only, needs_chinese_pos_pronunciation_quiz |
| 801 | 전화하다 | topikindepth_level2 | single_level_source_only |
| 974 | 티브이 | topikindepth_level2 | single_level_source_only, needs_chinese_pos_pronunciation_quiz |

## 五、未定级来源词样例（前120条）

这些词出现在 TOPIK I 公开大词表中，但没有进入本轮 level1/level2 分级来源。它们不是最终删除项，只是待定级池。

| ID | 韩语 | 来源 | 来源数 |
|----|------|------|--------|
| 1 | 가구 | koreantopik_1850, tammy_1671 | 2 |
| 2 | 가지 | koreantopik_1850, tammy_1671 | 2 |
| 3 | 각 | tammy_1671 | 1 |
| 4 | 간 | tammy_1671 | 1 |
| 5 | 감동 | tammy_1671 | 1 |
| 6 | 감동하다 | tammy_1671 | 1 |
| 7 | 감사드립니다 | tammy_1671 | 1 |
| 8 | 감사합니다 | tammy_1671 | 1 |
| 9 | 감자탕 | tammy_1671 | 1 |
| 10 | 강좌 | tammy_1671 | 1 |
| 11 | 개나리 | tammy_1671 | 1 |
| 12 | 개인 | tammy_1671 | 1 |
| 13 | 건배 | tammy_1671 | 1 |
| 14 | 검사 | koreantopik_1850 | 1 |
| 15 | 겨울방학 | tammy_1671 | 1 |
| 16 | 결정하다 | tammy_1671 | 1 |
| 17 | 경기 | koreantopik_1850, tammy_1671 | 2 |
| 18 | 경기장 | tammy_1671 | 1 |
| 19 | 계산하다 | tammy_1671 | 1 |
| 20 | 고마웠습니다 | tammy_1671 | 1 |
| 21 | 고맙습니다 | tammy_1671 | 1 |
| 22 | 고모부 | tammy_1671 | 1 |
| 23 | 고장 | koreantopik_1850, tammy_1671 | 2 |
| 24 | 고추 | tammy_1671 | 1 |
| 25 | 골목 | tammy_1671 | 1 |
| 26 | 골프 | tammy_1671 | 1 |
| 27 | 곱다 | tammy_1671 | 1 |
| 28 | 공간 | tammy_1671 | 1 |
| 29 | 공기 | tammy_1671 | 1 |
| 30 | 공연 | tammy_1671 | 1 |
| 31 | 과 | tammy_1671 | 1 |
| 32 | 과거 | koreantopik_1850, tammy_1671 | 2 |
| 33 | 과학 | tammy_1671 | 1 |
| 34 | 관광하다 | tammy_1671 | 1 |
| 35 | 광주 | koreantopik_1850 | 1 |
| 36 | 괜찮습니다 | tammy_1671 | 1 |
| 37 | 교체 | tammy_1671 | 1 |
| 38 | 구경하다 | tammy_1671 | 1 |
| 39 | 구하다 | tammy_1671 | 1 |
| 40 | 국립 | tammy_1671 | 1 |
| 41 | 국어 | tammy_1671 | 1 |
| 42 | 그들 | tammy_1671 | 1 |
| 43 | 그램 | tammy_1671 | 1 |
| 44 | 그렇게 | tammy_1671 | 1 |
| 45 | 그렇구나 | tammy_1671 | 1 |
| 46 | 그렇습니다 | tammy_1671 | 1 |
| 47 | 그중 | tammy_1671 | 1 |
| 48 | 금연 | tammy_1671 | 1 |
| 49 | 금주 | tammy_1671 | 1 |
| 50 | 기사 | tammy_1671 | 1 |
| 51 | 기억하다 | tammy_1671 | 1 |
| 52 | 기타 | koreantopik_1850, tammy_1671 | 2 |
| 53 | 긴장되다 | tammy_1671 | 1 |
| 54 | 길다 | koreantopik_1850, tammy_1671 | 2 |
| 55 | 김 | koreantopik_1850, tammy_1671 | 2 |
| 56 | 김포공항 | tammy_1671 | 1 |
| 57 | 깊이 | koreantopik_1850 | 1 |
| 58 | 깨지다 | tammy_1671 | 1 |
| 59 | 꼭 | koreantopik_1850, tammy_1671 | 2 |
| 60 | 나빠지다 | tammy_1671 | 1 |
| 61 | 남미 | tammy_1671 | 1 |
| 62 | 남북 | tammy_1671 | 1 |
| 63 | 남산 | koreantopik_1850 | 1 |
| 64 | 내가 | tammy_1671 | 1 |
| 65 | 노력하다 | tammy_1671 | 1 |
| 66 | 누가 | tammy_1671 | 1 |
| 67 | 눈사람 | tammy_1671 | 1 |
| 68 | 눈싸움 | tammy_1671 | 1 |
| 69 | 뉴욕 | tammy_1671 | 1 |
| 70 | 늦잠 | tammy_1671 | 1 |
| 71 | 님 | tammy_1671 | 1 |
| 72 | 다음달 | tammy_1671 | 1 |
| 73 | 다음주 | tammy_1671 | 1 |
| 74 | 다음해 | tammy_1671 | 1 |
| 75 | 단점 | tammy_1671 | 1 |
| 76 | 닫히다 | tammy_1671 | 1 |
| 77 | 달다 | koreantopik_1850, tammy_1671 | 2 |
| 78 | 달리다 | koreantopik_1850, tammy_1671 | 2 |
| 79 | 담그다 | tammy_1671 | 1 |
| 80 | 당근 | tammy_1671 | 1 |
| 81 | 당신 | tammy_1671 | 1 |
| 82 | 대 | koreantopik_1850, tammy_1671 | 2 |
| 83 | 대구 | koreantopik_1850 | 1 |
| 84 | 대전 | koreantopik_1850 | 1 |
| 85 | 대학원생 | tammy_1671 | 1 |
| 86 | 대한민국 | tammy_1671 | 1 |
| 87 | 더운물 | tammy_1671 | 1 |
| 88 | 덮다 | tammy_1671 | 1 |
| 89 | 데리다 | tammy_1671 | 1 |
| 90 | 도로 | koreantopik_1850, tammy_1671 | 2 |
| 91 | 도쿄 | tammy_1671 | 1 |
| 92 | 독서실 | tammy_1671 | 1 |
| 93 | 독서하다 | tammy_1671 | 1 |
| 94 | 돌 | koreantopik_1850 | 1 |
| 95 | 동대문 | koreantopik_1850 | 1 |
| 96 | 동대문시장 | tammy_1671 | 1 |
| 97 | 동아리 | tammy_1671 | 1 |
| 98 | 동양 | tammy_1671 | 1 |
| 99 | 된장국 | tammy_1671 | 1 |
| 100 | 두부찌개 | tammy_1671 | 1 |
| 101 | 드시다 | tammy_1671 | 1 |
| 102 | 듣기 | tammy_1671 | 1 |
| 103 | 들 | tammy_1671 | 1 |
| 104 | 들리다 | koreantopik_1850 | 1 |
| 105 | 등산복 | tammy_1671 | 1 |
| 106 | 등산화 | tammy_1671 | 1 |
| 107 | 디브이디 | tammy_1671 | 1 |
| 108 | 따라가다 | tammy_1671 | 1 |
| 109 | 따라오다 | tammy_1671 | 1 |
| 110 | 따르다 | tammy_1671 | 1 |
| 111 | 뜨다 | koreantopik_1850, tammy_1671 | 2 |
| 112 | 로션 | tammy_1671 | 1 |
| 113 | 마늘 | tammy_1671 | 1 |
| 114 | 만 | koreantopik_1850, tammy_1671 | 2 |
| 115 | 말다 | koreantopik_1850 | 1 |
| 116 | 말하기 | tammy_1671 | 1 |
| 117 | 맞습니다 | tammy_1671 | 1 |
| 118 | 맞아요 | tammy_1671 | 1 |
| 119 | 맞은편 | tammy_1671 | 1 |
| 120 | 먹다 | koreantopik_1850, tammy_1671 | 2 |

## 六、下一步

1. 先补齐 1级 228 个待新编字段词，生成正式 `topik_level1.json` 与 quiz。
2. 复核 2级 12 个单来源词，决定保留、替换或降权。
3. 从未定级池中挑出高支持、TOPIK I 场景明确的词，补入 1级或2级。
4. 完成字段补齐和人工复核前，不得把清洗源词表当最终词书发布。
