# 项目上下文（每次会话自动加载）

## 项目概述

韩语背单词微信小程序项目。包含产品设计文档、词汇数据、测验数据、音频素材及工具脚本。当前阶段：**开发中**（阶段一：项目初始化与基础架构）。

## 项目结构

```
├── CLAUDE.md                    # 本文件，AI 自动读取的项目上下文
├── README.md                    # 项目整体说明
├── 文档管理规范.md               # 文档分类、命名、更新责任规范
├── 文档索引.md                   # 各文件用途与更新日期（由 update_index.py 自动生成）
├── 单词分级标准.md               # 三级划分依据
├── project.config.json          # 微信开发者工具项目配置
├── tsconfig.json                # TypeScript 配置
├── package.json                 # npm 依赖（MobX 等）
│
├── miniprogram/                 # 小程序源码
│   ├── app.ts / app.json / app.wxss  # 入口文件
│   ├── sitemap.json
│   ├── pages/                   # 页面（6个）
│   │   ├── index/               # 单词首页（Tab）
│   │   ├── learn/               # 背单词 + 复习（mode 参数区分）
│   │   ├── result/              # 结算页
│   │   ├── stats/               # 统计页（Tab）
│   │   ├── mine/                # 我的（Tab）
│   │   └── book/                # 选词书
│   ├── components/              # 公共组件（3个）
│   │   ├── quiz-card/           # 四选一卡片
│   │   ├── recall-card/         # 主动回忆卡片
│   │   └── word-detail/         # 答案揭示详情
│   ├── services/                # 业务逻辑层（SRS、队列、存储）
│   ├── store/                   # MobX 状态管理
│   ├── utils/                   # 工具函数
│   └── static/                  # 本地静态资源（Lottie JSON 等）
│
├── cloudfunctions/             # 微信云函数（onLogin / syncProgress / dailyReset / updateProfile）
│
├── memory-bank/                 # 产品/设计/数据/脚本集中存放
│   ├── 技术栈.md                # 技术选型与架构方案
│   ├── 实施计划.md              # 分步开发指令（给 AI 开发者，含验证标准）
│   ├── progress.md              # 开发进度跟踪
│   ├── architecture.md          # 架构设计记录
│   ├── 产品文档/
│   │   ├── prd初稿.md           # 产品需求文档（功能架构、交互设计、数据结构）
│   │   ├── 背诵机制设计.md       # SRS 算法理论详述（已合入 PRD）
│   │   ├── TOPIK初级词书说明.md  # TOPIK 初级核心词书的定位、来源依据与校验要求
│   │   ├── TOPIK初级词源审计.md  # TOPIK 初级外部来源、覆盖差异与补词审计
│   │   ├── TOPIK12官方依据与编写记录.md # TOPIK 1/2级官方依据、公开词表来源与拆分记录
│   │   ├── TOPIK12源词表清洗核对报告.md # TOPIK 1/2级源词表清洗、去重与待复核报告
│   │   ├── TOPIK初级统一词书口径说明.md # TOPIK 初级统一成一本词书的产品口径
│   │   ├── 全局文案池.md         # 空状态/错误/鼓励/引导文案统一管理
│   │   └── 云开发数据规范.md     # 云函数协议、集合字段、离线队列
│   ├── 调研文档/
│   │   ├── 竞品调研报告.md       # 4 款竞品实际分析 + 核心结论
│   │   ├── 竞品调研报告.docx     # 同上 Word 版
│   │   ├── 竞品-不背单词/       # 竞品截图素材
│   │   ├── 竞品-多邻国/
│   │   ├── 竞品-疯狂背单词/
│   │   └── 竞品-韩语u学院/
│   ├── 设计文档/
│   │   ├── figma原型prompt.md   # 逐页 Figma AI 生成 prompt + 设计规范
│   │   ├── 前端页面设计方案.md   # 小程序前端视觉、交互、字号、颜色与页面逻辑规范
│   │   ├── 风格Demo.html        # 早期视觉风格 Demo（已归档）
│   │   ├── 宣传素材/            # 小红书等平台宣传图素材（含 2026-07-19 宣传图与文案）
│   │   └── prototype/           # 原型 HTML Demo
│   ├── 数据文件/
│   │   ├── beginner.json        # 初级词汇（日常生存韩语，1282词）
│   │   ├── topik_beginner.json  # TOPIK 初级（1-2级）候选词书（1594词，同主词库格式，待审计）
│   │   ├── topik_beginner_core.json # TOPIK 初级（1-2级）候选追溯词书（1594词，含来源与分组）
│   │   ├── topik_i_source_audit.json # TOPIK I 外部来源审计结果与缺词清单
│   │   ├── topik_i_source_pool.json # TOPIK I 外部公开源词池（非正式词书）
│   │   ├── topik_level1_source_pool.json # TOPIK 1级源词表（非正式词书）
│   │   ├── topik_level2_source_pool.json # TOPIK 2级源词表（非正式词书）
│   │   ├── topik_level1_cleaned_source_pool.json # TOPIK 1级清洗源词表（非正式词书）
│   │   ├── topik_level2_cleaned_source_pool.json # TOPIK 2级清洗源词表（非正式词书）
│   │   ├── topik_beginner_cleaned_source_pool.json # TOPIK 初级统一清洗源词表（1786词，非正式词书）
│   │   ├── topik_i_unassigned_source_words.json # TOPIK I 未定级源词（待人工判断）
│   │   ├── intermediate.json    # 中级词汇（社交/职场表达，901词）
│   │   ├── advanced.json        # 高级词汇（学术/抽象表达，759词）
│   │   ├── beginner_quiz.json   # 初级四选一干扰项数据
│   │   ├── topik_beginner_quiz.json # TOPIK 初级四选一干扰项数据
│   │   ├── intermediate_quiz.json # 中级四选一干扰项数据
│   │   ├── advanced_quiz.json   # 高级四选一干扰项数据
│   │   ├── 韩语单词知识库.docx   # 全部词汇 Word 版（阅读/打印用）
│   │   ├── TOPIK初级词汇.docx   # TOPIK 初级词汇 Word 版（阅读/打印用）
│   │   └── 音频_edge女声正式版/ # Edge TTS 女声正式版（2942个 mp3 + manifest）
│   └── 工具脚本/
│       ├── generate.py          # 初始词汇数据生成
│       ├── generate_distractors.py # 干扰选项批量生成
│       ├── build_topik12_source_pool.py # TOPIK 1/2级源词表构建
│       ├── clean_topik12_source_pool.py # TOPIK 1/2级源词表清洗核对
│       ├── generate_report.py   # 报告生成工具
│       ├── verify_dataset.py    # 数据全量校验（结构 / 去重 / 音频 / 干扰项）
│       ├── verify_pronunciation.py # 发音规则嫌疑扫描
│       ├── fix_pronunciation.py # 发音规则自动修订（支持 --dry-run）
│       ├── scan_content.py      # 内容合规关键词扫描
│       └── update_index.py      # 文档索引自动更新
│
└── 过程记录/
    ├── 对话记录.md               # 跨会话决策记录与待办
    └── 干扰选项审核表.md         # 1624 词干扰选项审核（已归档）
```

总词汇量：2942 词（初级 1282 / 中级 901 / 高级 759）

## 数据格式

每个 JSON 文件结构：

```json
{
  "level": "beginner",
  "level_cn": "初级",
  "description": "级别描述",
  "total": 1018,
  "words": [
    {
      "id": 1,
      "korean": "사람",
      "pronunciation": "sa-ram",
      "pos": "명사",
      "pos_cn": "名词",
      "meaning": "人"
    }
  ]
}
```

## 分级标准

| 级别 | 定位 | 判断依据 |
|------|------|----------|
| 初级 beginner | 日常生存韩语 | TOPIK I（1~2级）核心词；每天接触的词 |
| 中级 intermediate | 社交与日常表达 | TOPIK II（3~4级）；新闻标题、工作沟通用词 |
| 高级 advanced | 学术/职场/抽象表达 | TOPIK II（5~6级）；论文、报告、深度讨论用词 |

## 音频映射与批次规则

音频以 `level + id` 作为唯一绑定键，禁止依赖文件顺序匹配。

| 项目 | 规则 | 示例 |
|------|------|------|
| 单词唯一键 | `{level}:{id}` | `beginner:1019` |
| 本地文件名 | `{level}_{id:04d}.mp3` | `beginner_1019.mp3` |
| 本地相对路径 | `音频_edge女声正式版/{level}/{level}_{id:04d}.mp3` | `音频_edge女声正式版/beginner/beginner_1019.mp3` |
| 云存储路径 | `audio/{level}/{id}.mp3` | `audio/beginner/1019.mp3` |
| 小程序播放路径 | 按 `level + id` 拼接 | `audio/${level}/${id}.mp3` |

当前音频清单：

- `memory-bank/数据文件/音频_edge女声正式版/audio_manifest.json`：全量 2942 条，包含 `level`、`id`、`korean`、`meaning`、`filename`、`audio`、`cloud_path`、`batch`、`exists`。
- `memory-bank/数据文件/音频_edge女声正式版/audio_batch2_manifest.json`：第二批新增词音频清单，共 1318 条。
- `memory-bank/数据文件/音频_edge女声正式版/audio_batch2_summary.json`：第二批音频汇总。

音频批次与扩词批次（batch1-11）不是同一个概念。音频批次用于区分小程序初始上线词库和上线后新增词：

| 音频批次 | 范围 | 数量 |
|----------|------|------|
| audio batch1 | beginner 1-1018 / intermediate 1-336 / advanced 1-270 | 1624 |
| audio batch2 | beginner 1019-1282 / intermediate 337-901 / advanced 271-759 | 1318 |

后续新增词规则：

1. 只在对应级别末尾追加新词，使用下一个连续 `id`。
2. 已发布/已接入音频的旧词不要改 `id`；如必须删除或重排，必须同步更新 manifest、云存储映射和小程序数据迁移方案。
3. 新增词后运行音频同步脚本，只生成缺失的 `level + id` 音频，不覆盖已有音频。
4. 每次新增音频需更新对应批次 manifest，并检查全量 `audio_manifest.json` 中 `exists=false` 为 0。

## 发音标注规范

采用韩国《国语罗马字标记法》(Revised Romanization)，基于实际发音标注：
- 音节间用连字符 `-` 分隔
- 必须反映实际发音规则（经音化、鼻音化、连音等）：
  - 경음화：闭塞音(ㄱㄷㅂ)后的松音变紧音（ㄱ→ㄲ, ㄷ→ㄸ, ㅂ→ㅃ, ㅅ→ㅆ, ㅈ→ㅉ）
  - 비음화：ㄱ→ㅇ, ㄷ→ㄴ, ㅂ→ㅁ（在鼻音前）
  - 연음：终声连到后续元音音节

## 已确认的约定

1. **同形异义词处理**：合并为一个条目，释义用分号隔开（如 눈→"眼睛；雪"）
2. **词性标注**：使用韩语词性名（명사/동사/형용사/부사/감탄사/조사/관형사/대명사/수사）
3. **ID 编号**：每个级别内从 1 开始连续编号
4. **文档索引**：修改任何文件后运行 `python3 memory-bank/工具脚本/update_index.py` 更新索引
5. **Word 文档**：需要同步更新（使用 python-docx 生成，3个表格对应3个级别）
6. **扩词原则**：必须符合分级标准 + 韩国人日常高频使用，不能与其他级别重复
7. **文档规范**：所有 .md 文档需包含标准头信息（创建日期/更新日期/状态/用途），详见 `文档管理规范.md`
8. **GitHub 同步提醒**：遇到重要更新（词库/quiz/音频 manifest/小程序源码/PRD/设计文档/索引/过程记录/宣传素材/作品集 Demo 等）后，AI 需主动判断是否应提交并上传 GitHub。若已经完成可交付成果但用户未提到 `commit` / `push`，AI 应在最终回复中明确提醒“这次建议提交并上传 GitHub”，必要时主动询问是否现在执行；不要默默结束。
9. **词库来源真实性红线**：新增 TOPIK、考试、教材或任何“客观来源”词书时，AI 不能只从现有词库按感觉筛选后宣称符合考点。必须先列明外部来源、来源性质、抓取/对照日期、覆盖范围和不足；至少完成“正确释义来自哪里、候选词是否被来源支持、遗漏词如何发现、排除词为什么排除”的审计记录。未完成外部交叉验证前，只能标记为“候选版/待审计”，不得命名为最终版、不得写入宣传口径、不得主动 push 到 GitHub。
10. **不糊弄用户规则**：当用户要求“不能出错、客观、科学、确实符合考点”时，AI 必须把不确定性说清楚，把做过的验证和没做的验证分开说明；发现前一步判断过度或依据不足时，必须立即纠正文件状态和说明，不得用漂亮表述掩盖事实。

## 注意事项

- 不要创建不必要的新文件，优先编辑现有文件
- 修改 JSON 后注意保持格式正确、ID 连续
- 发音标注务必检查经音化等音变规则
- 新增/删除文件后必须同步更新本文件的项目结构段 + 运行索引脚本
- PRD 变更后在 `对话记录.md` 记录决策
- 新增词和音频时必须遵守 `level + id` 绑定规则，更新 `audio_manifest.json` 和对应批次清单
- 扩词 / 删词 / 改词必须按 [词库变更规范.md](memory-bank/产品文档/词库变更规范.md) 执行，区分上线前与上线后规则（上线后 id 焊死，删词走软删除）
- **AI 执行红线**：收到任何泡泡发的指令前，必须先对照 [AI执行红线.md](memory-bank/AI执行红线.md) 检查；命中红线（改 id / 删词 / 视觉决策 / 破坏性 git / 改云函数 / 改 PRD 等）必须**先停下来用 §5.1 模板提问，等泡泡明确确认后再动手**，不要直接执行
- 重要更新完成后主动提醒是否提交并上传 GitHub；可交付成果不要只停留在本地而不提示
