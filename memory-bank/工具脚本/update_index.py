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
            {'file': 'memory-bank/产品文档/TOPIK初级词书说明.md', 'purpose': 'TOPIK 初级核心词书的定位、来源依据与校验要求'},
            {'file': 'memory-bank/产品文档/TOPIK初级词源审计.md', 'purpose': 'TOPIK 初级外部来源、覆盖差异与补词审计'},
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
            {'file': 'memory-bank/工具脚本/generate_report.py', 'purpose': '报告生成工具'},
            {'file': 'memory-bank/工具脚本/update_index.py', 'purpose': '文档索引自动更新（本脚本）'},
        ],
        '过程记录': [
            {'file': '过程记录/对话记录.md', 'purpose': '跨会话决策记录与待办'},
            {'file': '过程记录/干扰选项审核表.md', 'purpose': '1624 词干扰选项审核（已归档）'},
        ],
    }

    # 统计词汇数
    word_counts = {}
    special_word_counts = {}
    total = 0
    for level in ['beginner', 'intermediate', 'advanced']:
        path = os.path.join(PROJECT_ROOT, 'memory-bank', '数据文件', f'{level}.json')
        if os.path.exists(path):
            count = get_word_count(path)
            word_counts[level] = count
            total += count
    for level in ['topik_beginner']:
        path = os.path.join(PROJECT_ROOT, 'memory-bank', '数据文件', f'{level}.json')
        if os.path.exists(path):
            special_word_counts[level] = get_word_count(path)

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
        '| 级别 | 词数 |',
        '|------|------|',
        f'| 初级 (beginner) | {word_counts.get("beginner", "?")} |',
        f'| 中级 (intermediate) | {word_counts.get("intermediate", "?")} |',
        f'| 高级 (advanced) | {word_counts.get("advanced", "?")} |',
        f'| **总计** | **{total}** |',
        '',
        '### 专项词书',
        '',
        '| 词书 | 词数 |',
        '|------|------|',
        f'| TOPIK初级（1-2级）(topik_beginner) | {special_word_counts.get("topik_beginner", "?")} |',
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
    print(f'总词汇量: {total}')

if __name__ == '__main__':
    main()
