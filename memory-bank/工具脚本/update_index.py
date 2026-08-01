"""
文档索引自动更新脚本
运行此脚本可自动生成/更新 文档索引.md，反映所有文档的最新状态。
"""

import json
import os
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_mod_date(filepath):
    """获取文件修改日期"""
    t = os.path.getmtime(filepath)
    return datetime.fromtimestamp(t).strftime('%Y-%m-%d')

def get_dir_mod_date(dirpath):
    """获取目录中最新文件的修改日期"""
    latest = 0
    for root, dirs, files in os.walk(dirpath):
        for f in files:
            fp = os.path.join(root, f)
            t = os.path.getmtime(fp)
            if t > latest:
                latest = t
    if latest == 0:
        return get_mod_date(dirpath)
    return datetime.fromtimestamp(latest).strftime('%Y-%m-%d')

def get_word_count(json_path):
    """读取 JSON 文件中的单词数"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('total', len(data.get('words', [])))

def main():
    categories = {
        '项目基建': [
            {'file': 'AGENTS.md', 'purpose': 'Codex 自动读取的项目上下文'},
            {'file': 'CLAUDE.md', 'purpose': 'AI 自动读取的项目上下文'},
            {'file': 'README.md', 'purpose': '项目整体说明'},
            {'file': '文档管理规范.md', 'purpose': '文档分类、命名、更新责任规范'},
            {'file': '单词分级标准.md', 'purpose': '初/中/高级单词的划分依据和规则'},
            {'file': 'memory-bank/技术栈.md', 'purpose': '技术选型与架构方案'},
            {'file': 'memory-bank/实施计划.md', 'purpose': '分步开发指令（给 AI 开发者，含验证标准）'},
        ],
        '产品文档': [
            {'file': 'memory-bank/产品文档/prd初稿.md', 'purpose': '产品需求文档（功能架构、交互设计、数据结构）'},
            {'file': 'memory-bank/产品文档/prd阅读版.md', 'purpose': '阅读友好版 PRD（背景、核心功能、需求详述表格）'},
            {'file': 'memory-bank/产品文档/背诵机制设计.md', 'purpose': 'SRS 算法理论详述（已合入 PRD）'},
            {'file': 'memory-bank/产品文档/TOPIK中高级词汇来源审计.md', 'purpose': 'TOPIK 3-6级来源、分级、排除项与局限审计'},
            {'file': 'memory-bank/产品文档/TOPIK中高级词汇元数据审计.md', 'purpose': 'TOPIK 中高级释义、词性、发音与干扰项审计'},
        ],
        '调研文档': [
            {'file': 'memory-bank/调研文档/', 'purpose': '竞品调研统一目录（报告 + 截图素材）', 'is_dir': True},
        ],
        '设计文档': [
            {'file': 'memory-bank/设计文档/figma原型prompt.md', 'purpose': '逐页 Figma AI 生成 prompt + 设计规范'},
            {'file': 'memory-bank/设计文档/前端页面设计方案.md', 'purpose': '小程序前端视觉、交互、字号、颜色与页面逻辑规范'},
            {'file': 'memory-bank/设计文档/风格Demo.html', 'purpose': '早期视觉风格 Demo（已归档）'},
            {'file': 'memory-bank/设计文档/prototype/', 'purpose': '原型 HTML Demo', 'is_dir': True},
            {'file': 'memory-bank/设计文档/宣传素材/', 'purpose': '小红书等平台宣传图与发布文案素材', 'is_dir': True},
        ],
        '数据文件': [
            {'file': 'memory-bank/数据文件/', 'purpose': '词汇 JSON + quiz + docx + 音频素材', 'is_dir': True},
        ],
        '工具脚本': [
            {'file': 'memory-bank/工具脚本/generate.py', 'purpose': '初始词汇数据生成'},
            {'file': 'memory-bank/工具脚本/generate_distractors.py', 'purpose': '干扰选项批量生成'},
            {'file': 'memory-bank/工具脚本/generate_topik_beginner_json.py', 'purpose': 'TOPIK 初级 Word 转 JSON 与 Quiz'},
            {'file': 'memory-bank/工具脚本/extract_nikl_learning_vocab.ps1', 'purpose': '提取并校验国立国语院官方分级词表'},
            {'file': 'memory-bank/工具脚本/build_topik_ii_source_pools.py', 'purpose': '构建 TOPIK 中高级来源池与分级审计'},
            {'file': 'memory-bank/工具脚本/fetch_topik_ii_krdict_metadata.py', 'purpose': '抓取韩国语基础词典官方元数据'},
            {'file': 'memory-bank/工具脚本/generate_topik_ii_wordbooks.py', 'purpose': '生成 TOPIK 中高级 JSON、Quiz、Word 与审计'},
            {'file': 'memory-bank/工具脚本/sync_miniprogram_data.py', 'purpose': '同步六本词书到小程序运行数据'},
            {'file': 'memory-bank/工具脚本/generate_report.py', 'purpose': '报告生成工具'},
            {'file': 'memory-bank/工具脚本/update_index.py', 'purpose': '文档索引自动更新（本脚本）'},
        ],
        '过程记录': [
            {'file': '过程记录/对话记录.md', 'purpose': '跨会话决策记录与待办'},
            {'file': '过程记录/干扰选项审核表.md', 'purpose': '1624 词干扰选项审核（已归档）'},
        ],
    }

    # 统计词汇数
    level_specs = [
        ('通用', '初级', 'beginner'),
        ('通用', '中级', 'intermediate'),
        ('通用', '高级', 'advanced'),
        ('TOPIK', '初级', 'topik_beginner'),
        ('TOPIK', '中级（3-4级）', 'topik_intermediate'),
        ('TOPIK', '高级（5-6级）', 'topik_advanced'),
    ]
    word_counts = {}
    word_sets = {}
    for _, _, level in level_specs:
        path = os.path.join(PROJECT_ROOT, 'memory-bank', '数据文件', f'{level}.json')
        if os.path.exists(path):
            count = get_word_count(path)
            word_counts[level] = count
            with open(path, 'r', encoding='utf-8') as f:
                word_sets[level] = {word['korean'] for word in json.load(f).get('words', [])}
    general_total = sum(word_counts.get(level, 0) for level in ('beginner', 'intermediate', 'advanced'))
    topik_total = sum(word_counts.get(level, 0) for level in ('topik_beginner', 'topik_intermediate', 'topik_advanced'))
    entry_total = general_total + topik_total
    general_words = set().union(*(word_sets.get(level, set()) for level in ('beginner', 'intermediate', 'advanced')))
    topik_words = set().union(*(word_sets.get(level, set()) for level in ('topik_beginner', 'topik_intermediate', 'topik_advanced')))
    unique_total = len(general_words | topik_words)
    cross_system_overlap = len(general_words & topik_words)
    # 生成索引内容
    today = datetime.now().strftime('%Y-%m-%d')

    lines = [
        '# 文档索引',
        '',
        f'> 本文件由 `memory-bank/工具脚本/update_index.py` 自动生成，请勿手动编辑。',
        f'> 最后更新：{today}',
        '',
        '## 词汇统计',
        '',
        '| 体系 | 级别 | level | 词数 |',
        '|------|------|-------|-----:|',
        *[
            f'| {system} | {level_cn} | `{level}` | {word_counts.get(level, "?")} |'
            for system, level_cn, level in level_specs
        ],
        f'| **通用小计** |  |  | **{general_total}** |',
        f'| **TOPIK小计** |  |  | **{topik_total}** |',
        f'| **文件条目合计** |  |  | **{entry_total}** |',
        '',
        f'> 六本词书按韩语词形去重后共 {unique_total} 词；通用与 TOPIK 体系重合 {cross_system_overlap} 词。',
        '',
    ]

    for cat_name, docs in categories.items():
        lines.append(f'## {cat_name}')
        lines.append('')
        lines.append('| 文件 | 用途 | 最后修改 |')
        lines.append('|------|------|----------|')

        for doc in docs:
            filepath = os.path.join(PROJECT_ROOT, doc['file'].rstrip('/'))
            if os.path.exists(filepath):
                if doc.get('is_dir'):
                    mod_date = get_dir_mod_date(filepath)
                else:
                    mod_date = get_mod_date(filepath)
                lines.append(f'| {doc["file"]} | {doc["purpose"]} | {mod_date} |')
            else:
                lines.append(f'| {doc["file"]} | {doc["purpose"]} | (未创建) |')

        lines.append('')

    # 写入文件
    index_path = os.path.join(PROJECT_ROOT, '文档索引.md')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f'文档索引已更新: {index_path}')
    print(f'通用词汇量: {general_total}')
    print(f'TOPIK词汇量: {topik_total}')
    print(f'六词书去重词形: {unique_total}')

if __name__ == '__main__':
    main()
