# TOPIK 1级/2级词汇书官方依据与编写记录

> 创建日期：2026-07-26
> 最后更新：2026-07-26
> 状态：源词表已建立 / 正式词书待逐词补全
> 用途：记录 TOPIK 1级、2级词汇书的官方依据、公开词表来源、拆分逻辑和待补字段

---

## 一、边界更正

TOPIK 官方公开的是考试结构、等级分数、能力描述和大致词汇量要求，不公开一份唯一、固定、逐词可核验的官方词汇表。因此本项目不能把任何公开整理词表称为“官方原表”。

本次重新编写时，官方材料只作为等级边界依据；逐词候选来自公开 TOPIK 词表，并保留每个词的来源证据。正式词书必须逐词补齐中文释义、发音、词性、quiz 和音频映射后才能发布。

## 二、官方依据

| 来源 | 性质 | URL |
|------|------|-----|
| National Institute for International Education TOPIK overview | official: TOPIK owner/operator overview, test format and levels | https://www.niied.go.kr/web/NIIED/contents/niiedEng/eng_topikOverview |
| 中国教育考试网 TOPIK 考试介绍 | official China test-administration page: score bands and Chinese ability descriptors | https://topik-main.neea.cn/xhtml1/folder/1507/1511-1.htm |

官方/考试机构材料确认：TOPIK I 包含 1级和2级；TOPIK I PBT 为听力30题、阅读40题，总分200；1级通常为80-139分，2级为140-200分。中国教育考试网的中文说明还明确写到：1级约800个基本词汇，2级约1500-2000个词汇。

## 三、公开词表来源

| 来源 | 用途 | URL |
|------|------|-----|
| TOPIK in Depth Level 1 vocabulary | public level-specific TOPIK vocabulary list; used for 1级 split only | https://topikindepth.com/en/topik/1/ |
| TOPIK in Depth Level 2 vocabulary | public level-specific TOPIK vocabulary list; used for 2级 split only | https://topikindepth.com/en/topik/2/ |
| Tammy Korean TOPIK I Vocabulary List 1671 | public TOPIK I vocabulary list with English glosses | https://learning-korean.com/elementary/20210101-10466/ |
| KoreanTopik TOPIK 1 Vocabulary List 1850 | public TOPIK I vocabulary list, split across linked pages | https://www.koreantopik.com/2024/05/topik-1-vocabulary-list-1850-for.html |

## 四、本轮产物

- `topik_level1_source_pool.json`：719 词，作为 TOPIK 1级源词表。
- `topik_level2_source_pool.json`：1067 词，作为 TOPIK 2级增量源词表。
- 合计：1786 词，落在 TOPIK 2级约1500-2000词的官方能力区间内。
- 1级源词表中已有项目释义/发音覆盖：491 词；待新词补全：228 词。
- 2级源词表中已有项目释义/发音覆盖：481 词；待新词补全：586 词。
- 外部公开来源去重候选池：2183 词。

## 五、下一步

1. 先处理 `metadata_status = needs_new_entry_review` 的词。
2. 每个新词补齐：中文释义、韩语词性、中文词性、Revised Romanization 发音、3个干扰项。
3. 对来源释义冲突、明显非TOPIK I、专有地名/品牌/过细文化词做人工保留/排除判断。
4. 生成正式 `topik_level1.json`、`topik_level2.json`、quiz、Word、小程序数据和音频映射。
5. 完成前不得把源词表包装成最终词书。
