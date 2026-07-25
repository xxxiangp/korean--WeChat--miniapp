# TOPIK 初级词书说明

> 创建日期：2026-07-25
> 最后更新：2026-07-25
> 状态：候选版 / 待外部来源交叉审计
> 用途：说明 TOPIK 初级词书的定位、来源依据、筛选规则、数据格式与校验要求

---

## 一、词书定位

`TOPIK 初级核心` 当前是面向 TOPIK I（1-2 级）备考用户的**候选词书**。

> 重要更正：当前 1594 词是从项目现有 `beginner/intermediate/advanced` 词库中派生出的候选集合，其中 94 词为外部公开 TOPIK I 来源审计后从项目主词库补入；已完成内部字段、释义、干扰项一致性校验，但尚未完成全部外部缺词的新词录入和人工复核。未完成审计前，不得称为最终版 TOPIK 考点词表，不得用于宣传口径或 GitHub 发布口径。

本词书当前候选版本收录 1594 个基础与进阶初级词，适合：

- TOPIK I 入门复习
- TOPIK I 1/2 级备考
- 韩语零基础到初级阶段的核心词汇回顾
- 后续扩展为 `TOPIK I 完整复习词书`

## 二、来源依据

本词书当前只完成“官方考试范围 + 项目已校验词库”的内部候选构建。下一步必须补做公开 TOPIK I 词表交叉审计。

### 2.1 TOPIK I 范围

TOPIK I 覆盖 1-2 级，重点考查初级学习者在日常生活中理解和使用韩语的能力，常见主题包括：

- 自我介绍、家庭、朋友
- 时间、日期、天气
- 饮食、购物、交通
- 学校、工作、兴趣
- 基础动作、状态、感受

TOPIK 1 级能力描述通常对应约 800 个基础词汇；TOPIK 2 级会继续扩展到约 1500-2000 个词汇。当前候选版先达到 1500+ 词规模，再通过外部公开词表继续补缺。

### 2.2 项目词库依据

项目现有 `beginner.json` 已按“日常生存韩语 / TOPIK I 核心词 / 高频生活词”整理，共 1282 词。

本词书当前版本的构成：

| 分组 | 数量 | 来源 | 说明 |
|------|------|------|------|
| 1급核心 | 800 | `beginner.json` id 1-800 | 覆盖 TOPIK I 1 级约 800 基础词范围 |
| 2급进阶 | 482 | `beginner.json` id 801-1282 | 扩展日常生活、公共场景、家务、兴趣、连接表达等 TOPIK I 2 级主题 |
| 2급补充 | 218 | `intermediate.json` 精选 | 从中级词库中筛选符合 TOPIK I 2 级边界的日常、公共服务、学习生活、基础情绪与表达词 |
| 外部来源补充 | 94 | 项目主词库已有词 | 外部公开 TOPIK I 来源审计后补入，复用既有释义、发音、quiz 与音频映射 |

筛选补充词时明确排除：

- 政治、法律、投资、宏观经济等偏 TOPIK II 主题
- 专业学科、学术研究、复杂社会议题
- 追星、社媒、新造流行语等专题词
- 过细的医疗、文学、历史、职场层级词

每个词条复用现有已校验字段：韩文、罗马字发音、韩语词性、中文词性、中文释义。保留 `source_level` 和 `source_id`，便于追溯到原始词库。

## 三、数据文件

本词书保留两类 JSON：

1. 正式运行版：与 `beginner.json`、`intermediate.json`、`advanced.json` 保持同一字段结构，便于小程序直接加载。
2. 来源追溯版：保留 `source_level`、`source_id`、`topik_band`、`selection_note`，用于审查 1/2 级来源和后续维护。

正式运行版路径：

```text
memory-bank/数据文件/topik_beginner.json
memory-bank/数据文件/topik_beginner_quiz.json
miniprogram/data/topik_beginner.json
miniprogram/data/topik_beginner_v2.js
miniprogram/data/topik_beginner_quiz.json
miniprogram/data/topik_beginner_quiz_v2.js
```

正式运行版结构：

```json
{
  "level": "topik_beginner",
  "level_cn": "TOPIK初级（1-2级）",
  "description": "面向 TOPIK I（1-2级）备考的初级核心词汇...",
  "total": 1594,
  "words": [
    {
      "id": 1,
      "korean": "나",
      "pronunciation": "na",
      "pos": "대명사",
      "pos_cn": "代词",
      "meaning": "我（非敬语）"
    }
  ]
}
```

配套阅读/打印版：

```text
memory-bank/数据文件/TOPIK初级词汇.docx
```

来源追溯版路径：

```text
memory-bank/数据文件/topik_beginner_core.json
```

来源追溯版结构：

```json
{
  "level": "topik_i_beginner",
  "level_cn": "TOPIK初级（1-2级）",
  "description": "面向 TOPIK I（1-2级）备考的初级词书。",
  "source_policy": {
    "basis": [],
    "selection_rule": "...",
    "not_official_notice": "..."
  },
  "groups": [
    {
      "name": "1급核心",
      "count": 800
    }
  ],
  "total": 1594,
  "words": [
    {
      "id": 1,
      "source_level": "beginner",
      "source_id": 1,
      "topik_band": "1급核心",
      "selection_note": "beginner 1-800：基础高频词，覆盖 TOPIK I 1级约 800 词范围",
      "korean": "나",
      "pronunciation": "na",
      "pos": "대명사",
      "pos_cn": "代词",
      "meaning": "我（非敬语）"
    }
  ]
}
```

## 四、重要边界

1. 本词书不是 TOPIK 官方发布的固定词表。
2. 本词书是基于 TOPIK I 能力范围、1/2 级词汇量标准和项目已校验词库整理的备考核心词书。
3. 本次不修改 `beginner.json`、`intermediate.json`、`advanced.json` 的任何词条或 ID。
4. 当前已生成同规格正式 JSON、quiz、Word 文档，并同步到 `miniprogram/data`。
5. 当前未生成新音频，也未把 TOPIK 词书入口接入页面；后续接入时建议做“专题词书引用层”，不要复制一套独立学习记录。

## 五、后续扩展建议

| 阶段 | 词书 | 数量 | 说明 |
|------|------|------|------|
| v1 | TOPIK 初级核心 | 800 | 已完成，覆盖 1 级基础核心词 |
| v2 | TOPIK 初级（1-2级）候选 | 1500 | 已降级为候选版，依据不足，不能作为最终版 |
| v2.1 | TOPIK 初级（1-2级）候选 | 1594 | 当前版本，补入 94 个外部来源支持且项目主词库已有的词 |
| v3 | TOPIK I 完整复习 | 1800-2200 | 后续结合外部来源缺口、真题主题和人工复核继续精修与补充 |

---

## 六、校验要求

每次修改本词书后至少检查：

- `total` 等于 `words.length`
- `id` 从 1 连续递增
- `source_level/source_id` 能在源词库中找到
- `korean` 不重复
- 必填字段不为空
- `pos` 属于项目约定词性集合
- `topik_beginner_quiz.json` 与 `topik_beginner.json` 数量一致
- quiz 每个词条包含 3 个干扰项，且干扰项不等于正确释义

若后续接入前端，还需新增专题词书加载逻辑和对应回归用例。
