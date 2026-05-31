"""
为所有韩语词汇生成 3 个干扰选项（同词性、不混淆）

输出：
1. beginner_quiz.json / intermediate_quiz.json / advanced_quiz.json → 小程序接入用
2. 干扰选项审核表.md → 人工校对用

干扰项选取规则：
- 同词性优先（从全库同词性词中抽取）
- 不选自身、不选含义完全相同的词
- 不选含义有包含关系的词（如 "走" 不选 "走路"）
- 同级别优先，不足时跨级别补充
- 固定随机种子保证可复现
"""

import json
import random
import os

random.seed(42)

BASE_DIR = '/Users/kakami/Desktop/韩语知识库'

# 加载全部词汇
all_words = []
levels_data = {}

for level in ['beginner', 'intermediate', 'advanced']:
    with open(os.path.join(BASE_DIR, f'{level}.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)
        levels_data[level] = data
        for w in data['words']:
            w['_level'] = level
            all_words.append(w)

print(f"总词汇量: {len(all_words)}")

# 按词性建立索引（全库）
pos_groups = {}
for w in all_words:
    pos = w['pos']
    if pos not in pos_groups:
        pos_groups[pos] = []
    pos_groups[pos].append(w)

print("词性分布:")
for pos, words in sorted(pos_groups.items(), key=lambda x: -len(x[1])):
    print(f"  {pos}: {len(words)}")


def meanings_conflict(m1, m2):
    """检查两个释义是否冲突（相同、包含、过于相似）"""
    m1_clean = m1.replace('（', '').replace('）', '').replace('(', '').replace(')', '')
    m2_clean = m2.replace('（', '').replace('）', '').replace('(', '').replace(')', '')

    # 完全相同
    if m1_clean == m2_clean:
        return True

    # 分号分割后有交集
    parts1 = set(p.strip() for p in m1_clean.replace('；', ';').split(';'))
    parts2 = set(p.strip() for p in m2_clean.replace('；', ';').split(';'))
    if parts1 & parts2:
        return True

    # 一个包含另一个（去掉括号内容后）
    core1 = m1_clean.split('；')[0].split(';')[0].strip()
    core2 = m2_clean.split('；')[0].split(';')[0].strip()
    if len(core1) > 1 and len(core2) > 1:
        if core1 in core2 or core2 in core1:
            return True

    return False


def get_distractors(target_word, pos_pool, n=3):
    """为目标词从同词性池中选取 n 个不冲突的干扰项"""
    candidates = [
        w for w in pos_pool
        if w['korean'] != target_word['korean']
        and not meanings_conflict(target_word['meaning'], w['meaning'])
    ]

    # 同级别优先
    same_level = [c for c in candidates if c['_level'] == target_word['_level']]
    other_level = [c for c in candidates if c['_level'] != target_word['_level']]

    random.shuffle(same_level)
    random.shuffle(other_level)

    selected = []
    for c in same_level + other_level:
        # 确保选出的干扰项之间也不冲突
        conflict = False
        for s in selected:
            if meanings_conflict(c['meaning'], s['meaning']):
                conflict = True
                break
        if not conflict:
            selected.append(c)
        if len(selected) >= n:
            break

    return selected


# 处理词性池过小的情况（如 관형사 只有 32 个）
# 如果同词性不足 4 个词，则从相近词性补充
POS_FALLBACK = {
    '접속사': '부사',
    '수사': '명사',
    '감탄사': '부사',
}


def get_pool_for_word(word):
    """获取该词可用的干扰项池"""
    pos = word['pos']
    pool = pos_groups.get(pos, [])
    if len(pool) < 4:
        fallback_pos = POS_FALLBACK.get(pos, '명사')
        pool = pool + pos_groups.get(fallback_pos, [])
    return pool


# ===== 生成干扰项 =====
results = {level: [] for level in ['beginner', 'intermediate', 'advanced']}
failed = []

for word in all_words:
    pool = get_pool_for_word(word)
    distractors = get_distractors(word, pool)

    if len(distractors) < 3:
        # 极端情况：从全库名词补充
        extra_pool = pos_groups.get('명사', [])
        extra = get_distractors(word, extra_pool, n=3 - len(distractors))
        distractors.extend(extra)

    if len(distractors) < 3:
        failed.append(word)
        # 用占位符
        while len(distractors) < 3:
            distractors.append({'meaning': '【需人工补充】', 'korean': '?'})

    entry = {
        'id': word['id'],
        'korean': word['korean'],
        'pronunciation': word['pronunciation'],
        'pos': word['pos'],
        'pos_cn': word['pos_cn'],
        'meaning': word['meaning'],
        'distractors': [
            {'meaning': d['meaning'], 'korean': d['korean']}
            for d in distractors[:3]
        ]
    }
    results[word['_level']].append(entry)

# ===== 输出 JSON 文件（小程序接入用）=====
for level in ['beginner', 'intermediate', 'advanced']:
    level_cn = {'beginner': '初级', 'intermediate': '中级', 'advanced': '高级'}[level]
    output = {
        'level': level,
        'level_cn': level_cn,
        'description': f'{level_cn}词汇四选一测试数据',
        'total': len(results[level]),
        'format_note': 'distractors 为 3 个同词性干扰项，正确答案为 meaning 字段',
        'words': results[level]
    }
    output_path = os.path.join(BASE_DIR, f'{level}_quiz.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"✅ {output_path} ({len(results[level])} 词)")

# ===== 输出审核文档 =====
md_lines = [
    '# 干扰选项审核表',
    '',
    '> 生成日期：2026-05-30',
    '> 生成规则：同词性随机抽取，排除含义冲突项',
    '> 审核方式：检查每行的 3 个干扰项是否合理，不合理的标记修改',
    '',
    '---',
    '',
]

for level in ['beginner', 'intermediate', 'advanced']:
    level_cn = {'beginner': '初级', 'intermediate': '中级', 'advanced': '高级'}[level]
    md_lines.append(f'## {level_cn}（{len(results[level])} 词）')
    md_lines.append('')
    md_lines.append('| ID | 韩文 | 正确答案 | 干扰1 | 干扰2 | 干扰3 |')
    md_lines.append('|----|------|----------|-------|-------|-------|')

    for entry in results[level]:
        d = entry['distractors']
        md_lines.append(
            f"| {entry['id']} | {entry['korean']} | {entry['meaning']} | "
            f"{d[0]['meaning']} | {d[1]['meaning']} | {d[2]['meaning']} |"
        )

    md_lines.append('')
    md_lines.append('---')
    md_lines.append('')

if failed:
    md_lines.append(f'## ⚠️ 需人工补充（{len(failed)} 词）')
    md_lines.append('')
    for w in failed:
        md_lines.append(f"- {w['korean']}（{w['meaning']}）— 同词性候选不足")

review_path = os.path.join(BASE_DIR, '干扰选项审核表.md')
with open(review_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(md_lines))
print(f"✅ {review_path}")

if failed:
    print(f"⚠️ {len(failed)} 个词需要人工补充干扰项")
else:
    print("✅ 所有词均已成功生成 3 个干扰项")
