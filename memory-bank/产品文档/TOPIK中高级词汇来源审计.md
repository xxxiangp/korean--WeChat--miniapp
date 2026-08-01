# TOPIK中高级词汇来源审计

> 创建日期：2026-08-02
> 最后更新：2026-08-02
> 状态：源词池已建立 / 分级与排除审计通过
> 用途：记录TOPIK 3-6级词汇的官方边界、逐词来源、清洗规则、覆盖情况和局限

---

## 一、结论边界

TOPIK官方公开考试结构、等级和分数区间，但不发布一份唯一固定的3-6级逐词考纲。因此本项目不能把任何第三方逐词表称为“TOPIK官方词表”。

本次采用分层证据：NIIED/中国教育考试网确认TOPIK II等级边界；国立国语院2017标准课程词表提供官方1-6级逐词分级；国立国语院2003年5965词提供历史学习阶段；TOPIK in Depth 3-6级与KoreanTopik TOPIK II 3900词表提供两套独立的考试相关候选证据。

## 二、来源

| 来源 | 性质 | 用途 |
|------|------|------|
| [NIIED TOPIK overview](https://www.niied.go.kr/web/NIIED/contents/niiedEng/eng_topikOverview) | official: TOPIK owner/operator; confirms TOPIK II and Level 3-6 score bands | 等级与考试边界 |
| [中国教育考试网TOPIK考试介绍](https://topik-main.neea.cn/xhtml1/folder/1507/1511-1.htm) | official China test-administration information | 等级与考试边界 |
| [韩国国立国语院《2017国际通用韩国语标准教育课程》词汇等级目录](https://www.korean.go.kr/front_eng/down/down_01V.do?report_seq=932) | official Korean standard curriculum vocabulary list with explicit Level 1-6 labels; not a TOPIK fixed list | 主要官方1-6级逐词分级与词性支持 |
| [韩国国立国语院《韩国语学习用词汇目录》](https://www.korean.go.kr/front/etcData/etcDataView.do?mn_id=46&etc_seq=71) | official Korean learner vocabulary list: A 982 / B 2111 / C 2872; not a TOPIK fixed list | 候选词官方学习阶段与词性支持 |
| [TOPIK in Depth Level 3 vocabulary](https://topikindepth.com/zh/topik/3/) | public level-specific TOPIK vocabulary list with romanization and Chinese glosses | 3级逐词候选 |
| [TOPIK in Depth Level 4 vocabulary](https://topikindepth.com/zh/topik/4/) | public level-specific TOPIK vocabulary list with romanization and Chinese glosses | 4级逐词候选 |
| [TOPIK in Depth Level 5 vocabulary](https://topikindepth.com/zh/topik/5/) | public level-specific TOPIK vocabulary list with romanization and Chinese glosses | 5级逐词候选 |
| [TOPIK in Depth Level 6 vocabulary](https://topikindepth.com/zh/topik/6/) | public level-specific TOPIK vocabulary list with romanization and Chinese glosses | 6级逐词候选 |
| [KoreanTopik TOPIK 2 Vocabulary List 3900](https://www.koreantopik.com/2024/09/complete-topik-2-vocabulary-list-3900.html) | public TOPIK II vocabulary list with English glosses; advertised as 3900, page integrity audited separately | 独立TOPIK II候选佐证与英文释义 |

国立国语院2003词表附件抓取日期：2026-08-01；SHA-256：`DF05D31942DB919668A91234539ED63A200C77F4058A9A135B64C3ED08219475`。原表5965条：A 982、B 2111、C 2872；去除同形异义编号后为5543个韩语词形。

国立国语院2017标准课程附件抓取日期：2026-08-01；SHA-256：`2CDE28AB90E04728513E65EF5DF4BAAA400A4055FE2ABD1856889CB983C4C3AC`。原表10635条：1级735、2级1100、3级1655、4级2200、5级2365、6级2580；去除同形异义编号后为10113个韩语词形。

KoreanTopik页面宣称3900词，但本次逐页解析得到3873行、3872个不同编号、3706个纯韩文去重词形；缺失编号28个，重复编号1个。因此它只作为公开佐证，不按宣传数量视为完整原表。

局限：两份国立国语院名单都是韩国语学习者通用课程/词汇分级，不等于TOPIK逐词考纲；两套TOPIK逐词来源都是公开整理站点，不是考试官方。交叉使用能提高可信度，但不能消除逐词复核责任。

## 三、清洗规则

1. 只保留纯韩文词条；以连字符开头的语法形式、空格短语、数字或符号项不进入背词词书。
2. 同形异义词合并学习，按2017官方课程中最早等级归属，避免同一个韩语词形跨词书重复。
3. 与TOPIK初级重复的词不再进入中高级词书；2017官方1/2级或2003旧表A阶段词也不提升到中高级。
4. 候选词必须同时具备公开TOPIK II证据与官方学习等级证据：2017课程3/4级归中级、5/6级归高级；2017未收录时才回退到2003旧表B/C阶段。只有公开站点支持的词保留在审计排除池。
5. 公开释义与官方等级证据明显指向不同同形义项时，须用《标准国语大辞典》复核；无法对齐或发生跨级错配的词进入审计排除池。
6. 现有项目词库只用于复用已校对的释义、词性和发音，不作为TOPIK来源证据。

## 四、源词池统计

```json
{
  "topikindepth_parsed": {
    "3": 887,
    "4": 1896,
    "5": 1114,
    "6": 957
  },
  "koreantopik_integrity": {
    "advertised_total": 3900,
    "raw_rows": 3873,
    "unique_source_numbers": 3872,
    "accepted_unique_pure_hangul": 3706,
    "missing_source_number_count": 28,
    "duplicate_source_numbers": {
      "2600": 2
    }
  },
  "topik_intermediate": {
    "total": 3715,
    "topikindepth_sublevels": {
      "3": 872,
      "4": 1808,
      "5": 998,
      "6": 37
    },
    "public_source_support_count": {
      "2": 3464,
      "1": 251
    },
    "level_assignment_basis": {
      "nikl_2017_minimum_level_3": 1456,
      "nikl_2017_minimum_level_4": 1971,
      "nikl_2003_grade_B_without_2017_match": 288
    },
    "source_confidence": {
      "high_official_level_plus_two_public_sources": 3427,
      "medium_legacy_official_stage_plus_public_source": 251,
      "medium_legacy_official_stage_plus_two_public_sources": 37
    },
    "metadata_status": {
      "needs_new_entry_metadata_with_chinese_source": 2996,
      "covered_by_project_vocab": 719
    },
    "nikl_grades": {
      "B": 1203,
      "C": 1622,
      "A": 2
    },
    "nikl_2017_levels": {
      "3급": 1456,
      "5급": 88,
      "4급": 1996,
      "6급": 35
    },
    "review_flags": {
      "needs_new_project_metadata": 2996,
      "public_sublevel_differs_from_official_assignment": 1035,
      "multiple_nikl_2017_levels_keep_minimum_for_merged_homograph": 142,
      "assignment_uses_legacy_nikl_2003_stage": 288,
      "single_public_topik_source": 251
    }
  },
  "topik_advanced": {
    "total": 1008,
    "topikindepth_sublevels": {
      "6": 900,
      "4": 52,
      "5": 55,
      "3": 1
    },
    "public_source_support_count": {
      "1": 933,
      "2": 75
    },
    "level_assignment_basis": {
      "nikl_2017_minimum_level_5": 238,
      "nikl_2017_minimum_level_6": 106,
      "nikl_2003_grade_C_without_2017_match": 664
    },
    "source_confidence": {
      "high_official_level_plus_public_source": 341,
      "high_official_level_plus_two_public_sources": 3,
      "medium_legacy_official_stage_plus_public_source": 592,
      "medium_legacy_official_stage_plus_two_public_sources": 72
    },
    "metadata_status": {
      "needs_new_entry_metadata_with_chinese_source": 868,
      "covered_by_project_vocab": 140
    },
    "nikl_grades": {
      "C": 974,
      "B": 36,
      "A": 1
    },
    "nikl_2017_levels": {
      "5급": 238,
      "6급": 109
    },
    "review_flags": {
      "single_public_topik_source": 933,
      "needs_new_project_metadata": 868,
      "public_sublevel_differs_from_official_assignment": 53,
      "multiple_nikl_2017_levels_keep_minimum_for_merged_homograph": 3,
      "assignment_uses_legacy_nikl_2003_stage": 664
    }
  },
  "source_exclusions": {
    "non_pure_hangul_or_grammar_form": 122
  },
  "book_exclusions": {
    "nikl_2017_minimum_level_is_1_or_2": 75,
    "already_owned_by_topik_beginner_wordbook": 70,
    "public_topik_source_only_without_nikl_level_support": 48,
    "public_gloss_not_supported_by_official_exact_headword_senses": 2,
    "nikl_2003_minimum_stage_is_A": 3,
    "public_and_official_evidence_refer_to_different_level_senses": 1,
    "public_and_official_evidence_refer_to_different_grammar_senses": 1
  }
}
```

## 五、中级使用2003旧表回退分级的待复核词（前40条）

| ID | 韩语 | 公开子级 | 释义来源 | 分级依据 | 标记 |
|----|------|----------|----------|----------|------|
| 3428 | 가까워지다 | 4 | 变得接近，关系变亲近 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3429 | 가까이 | 3 | 靠近，距离近 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, needs_new_project_metadata |
| 3430 | 가난하다 | 4 | 贫穷的，缺乏财富的 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3431 | 가능하다 | 4 | 可能，能够 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3432 | 가로 | 3 | 宽度，横向长度 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, needs_new_project_metadata |
| 3433 | 가슴속 | 4 | 内心，心里 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3434 | 가이드 | 4 | 导游，指导者，指南 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source |
| 3435 | 각자 | 3 | 各自，每个人 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, needs_new_project_metadata |
| 3436 | 감상하다 | 4 | 欣赏（艺术作品等） | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3437 | 강원도 | 4 | 韩国东北部的一个道（行政区划） | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3438 | 강조하다 | 4 | 强调，突出表示 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source |
| 3439 | 개발하다 | 4 | 开发，开拓，创造新事物 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3440 | 개인적 | 5 | 个人的，私人的 | nikl_2003_grade_B_without_2017_match | public_sublevel_differs_from_official_assignment, assignment_uses_legacy_nikl_2003_stage, needs_new_project_metadata |
| 3441 | 걱정되다 | 4 | 担心，感到忧虑 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3442 | 건너오다 | 4 | 从对面过来，穿过到这边 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3443 | 검정색 | 4 | 黑色 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3444 | 결국 | 3 | 最终，结果 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage |
| 3445 | 결심하다 | 4 | 下决心，决定做某事 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3446 | 결정되다 | 4 | 被决定，确定 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3447 | 결정하다 | 4 | 决定，作出判断 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source |
| 3448 | 경기도 | 4 | 环绕首尔的地区名称 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3449 | 경상도 | 4 | 韩国庆尚道地区的名称 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3450 | 경제적 | 5 | 经济的，关于经济的 | nikl_2003_grade_B_without_2017_match | public_sublevel_differs_from_official_assignment, assignment_uses_legacy_nikl_2003_stage, needs_new_project_metadata |
| 3451 | 경험하다 | 4 | 经历，体验 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3452 | 계산하다 | 4 | 计算，结算 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source |
| 3453 | 계속되다 | 4 | 继续，持续 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3454 | 계속하다 | 4 | 继续，持续 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3455 | 계획하다 | 4 | 计划，制定计划 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3456 | 고교 | 4 | 高中 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3457 | 고려하다 | 4 | 考虑，斟酌 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3458 | 고모부 | 4 | 父亲那边姑妈的丈夫 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3459 | 고민하다 | 4 | 烦恼，苦恼 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source |
| 3460 | 고생하다 | 4 | 吃苦，辛苦，遭受困难或痛苦 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3461 | 고속도로 | 4 | 无路灯的高速公路，高速汽车道 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source |
| 3462 | 골프장 | 4 | 高尔夫球场 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3463 | 공항버스 | 4 | 机场巴士 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3464 | 과학적 | 5 | 科学的的 | nikl_2003_grade_B_without_2017_match | public_sublevel_differs_from_official_assignment, assignment_uses_legacy_nikl_2003_stage, needs_new_project_metadata |
| 3465 | 관련되다 | 4 | 有关，相关 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3466 | 관련하다 | 4 | 与……相关，涉及 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 3467 | 관찰하다 | 4 | 观察，仔细看 | nikl_2003_grade_B_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |

## 六、高级使用2003旧表回退分级的待复核词（前40条）

| ID | 韩语 | 公开子级 | 释义来源 | 分级依据 | 标记 |
|----|------|----------|----------|----------|------|
| 345 | 가능해지다 | 6 | 变得可能 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 346 | 가려지다 | 6 | 被遮盖，被隐藏 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 347 | 가입하다 | 6 | 加入，参加 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 348 | 가정교사 | 6 | 家庭教师 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 349 | 각기 | 6 | 各自，分别 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 350 | 간접적 | 5 | 间接的，不直接的 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, needs_new_project_metadata |
| 351 | 간혹 | 5 | 偶尔，有时 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, needs_new_project_metadata |
| 352 | 감동적 | 5 | 感人的，令人感动的 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, needs_new_project_metadata |
| 353 | 감소되다 | 6 | 减少，变少 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 354 | 감소하다 | 6 | 减少，降低 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source |
| 355 | 감정적 | 6 | 感情的的，情绪相关的 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 356 | 강남 | 6 | 河流以南的地区，特别指首尔的江南区 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 357 | 강력하다 | 6 | 强大，有力 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 358 | 강변 | 6 | 强词夺理，辩解 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 359 | 강북 | 6 | 江北，指江河以北的地区 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 360 | 강요하다 | 6 | 强迫，强制要求 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 361 | 강의하다 | 6 | 讲授，授课 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 362 | 강화하다 | 6 | 加强，强化 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 363 | 같이하다 | 6 | 一起做，共同进行 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 364 | 개발되다 | 6 | 被开发，被利用 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 365 | 개방되다 | 6 | 被开放，变得可自由使用 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 366 | 개방하다 | 6 | 开放，解放 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 367 | 개선되다 | 6 | 被改善，得到改进 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 368 | 개선하다 | 6 | 改善，改进 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source |
| 369 | 객관적 | 5 | 客观的，不受主观影响的 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage |
| 370 | 거대하다 | 6 | 非常巨大，庞大的 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 371 | 거부하다 | 6 | 拒绝，否认，不同意 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source |
| 372 | 거절하다 | 6 | 拒绝，回绝 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source |
| 373 | 건 | 6 | 表示问题或事项的名词 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 374 | 건넌방 | 6 | 对面的房间，尤其是客厅对面的房间 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 375 | 건설되다 | 6 | 被建造，建设 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 376 | 건설하다 | 6 | 建设，建造 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 377 | 건전하다 | 6 | 健康的，健全，有活力 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 378 | 건조하다 | 6 | 干燥，变干 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source |
| 379 | 걷기 | 6 | 步行，走路 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 380 | 겨자 | 6 | 芥末（辛辣的调味品） | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 381 | 결과적 | 6 | 结果的，作为结果的 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 382 | 결석하다 | 6 | 缺席，指未参加学校、会议等 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 383 | 경고하다 | 6 | 警告，提醒注意 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |
| 384 | 경영하다 | 6 | 经营，管理 | nikl_2003_grade_C_without_2017_match | assignment_uses_legacy_nikl_2003_stage, single_public_topik_source, needs_new_project_metadata |

## 七、未采用材料

项目旧文件 `韩语-小程序/TOPIK词汇.pdf` 含大量变形、短语、词性错误和过度展开释义，仅保留为历史参考，不参与本轮候选纳入和字段定稿。

## 八、下一步

1. 对待新编词补齐并审计中文释义、韩国国语罗马字发音和词性。
2. 逐条处理单公开来源、官方阶段不一致和同形多词性记录。
3. 生成中级/高级Word、JSON和quiz后执行结构、重复、释义冲突、发音和干扰项校验。
4. 在全部校验完成前，源词池不得命名或宣传为最终词书。
