"""生成竞品调研报告 Word 文档"""

from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import datetime

doc = Document()

# ===== 样式设置 =====
style = doc.styles['Normal']
style.font.name = 'Microsoft YaHei'
style.font.size = Pt(10.5)
style.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')

# 页面边距
for section in doc.sections:
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)


def set_cell_shading(cell, color):
    """设置单元格背景色"""
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), color)
    shading.set(qn('w:val'), 'clear')
    cell._tc.get_or_add_tcPr().append(shading)


def add_table(doc, headers, rows, col_widths=None):
    """添加格式化表格"""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # 表头
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(10)
        set_cell_shading(cell, 'E8F0F8')

    # 数据行
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = str(val)
            cell.paragraphs[0].runs[0].font.size = Pt(10)

    # 列宽
    if col_widths:
        for i, w in enumerate(col_widths):
            for row in table.rows:
                row.cells[i].width = Cm(w)

    doc.add_paragraph()
    return table


# ===== 封面 =====
doc.add_paragraph()
doc.add_paragraph()
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run('竞品调研报告')
run.font.size = Pt(28)
run.bold = True

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run('韩语背单词小程序 · 竞品分析与策略建议')
run.font.size = Pt(14)
run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

doc.add_paragraph()
info = doc.add_paragraph()
info.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = info.add_run(f'调研日期：2026-05-29\n调研方式：基于实际产品截图逐页分析（34张截图）\n生成日期：{datetime.date.today().isoformat()}')
run.font.size = Pt(11)
run.font.color.rgb = RGBColor(0x99, 0x99, 0x99)

doc.add_page_break()

# ===== 目录页 =====
doc.add_heading('目录', level=1)
toc_items = [
    '一、竞品选择与对比总览',
    '二、逐产品深度拆解',
    '    2.1 不背单词 — 审美 + 语境 + 主动回忆',
    '    2.2 疯狂背单词 — 应试四选一 + 多模式练习',
    '    2.3 韩语U学院 — 韩语垂直 + 浏览式学习',
    '    2.4 多邻国 — 游戏化之王',
    '三、横向对比：关键维度',
    '四、综合洞察与市场机会',
    '五、我们的差异化定位',
    '六、核心学习流程建议',
    '七、功能优先级矩阵',
]
for item in toc_items:
    p = doc.add_paragraph(item)
    p.paragraph_format.space_after = Pt(4)

doc.add_page_break()

# ===== 一、对比总览 =====
doc.add_heading('一、竞品选择与对比总览', level=1)

doc.add_paragraph('本次调研选取 4 款代表性产品，覆盖「审美驱动」「应试工具」「韩语垂类」「游戏化」四类方向：')

add_table(doc,
    ['维度', '不背单词', '疯狂背单词', '韩语U学院', '多邻国'],
    [
        ['定位', '语境沉浸+审美驱动', '应试工具型', '韩语综合学习', '游戏化全语种'],
        ['语种', '英语', '英语', '韩语', '多语种'],
        ['形态', '原生 App', '原生 App', '原生 App', '原生 App'],
        ['核心机制', '主动回忆+三级反馈+语境', '四选一选择题', '纯浏览+二级判断', '游戏化闯关+自适应'],
        ['记忆算法', 'SRS（间隔复习）', 'SRS+智能复习', '无明显SRS', '自适应难度'],
        ['视觉风格', '极致审美/毛玻璃', '黄色活泼/功能导向', '蓝色/可爱卡通', '彩色/游戏化/IP'],
        ['Tab数量', '3个', '4个', '5个', '5个'],
    ],
    col_widths=[2.5, 3.5, 3.5, 3.5, 3.5]
)

# ===== 二、逐产品拆解 =====
doc.add_heading('二、逐产品深度拆解', level=1)

# --- 2.1 不背单词 ---
doc.add_heading('2.1 不背单词 — 审美 + 语境 + 主动回忆', level=2)

doc.add_paragraph('以"最美背单词 App"为品牌心智，用高品质壁纸 + 真实语境例句打造沉浸体验。学习机制科学：先遮挡释义让用户主动回忆，再展示语境强化。')

doc.add_heading('页面结构（3 Tab）', level=3)
add_table(doc,
    ['页面', '功能'],
    [
        ['学习（首页）', '全屏壁纸 + Learn/Review 两个入口'],
        ['我的内容', '随身听、听写、词书、句库、笔记'],
        ['仪表盘', '学习数据 + 日历签到'],
    ])

doc.add_heading('背诵核心流程', level=3)
p = doc.add_paragraph()
p.add_run('阶段一：主动回忆').bold = True
doc.add_paragraph('• 只展示单词 + 发音（释义被遮挡）', style='List Bullet')
doc.add_paragraph('• 引导文案："瞬间想起词义，选认识；思考后想起，选模糊"', style='List Bullet')
doc.add_paragraph('• 三级反馈按钮：认识(🟢) / 模糊(🟡) / 忘了(🔴)', style='List Bullet')

p = doc.add_paragraph()
p.add_run('阶段二：揭示 + 语境强化').bold = True
doc.add_paragraph('• 音节拆分 + 释义揭示', style='List Bullet')
doc.add_paragraph('• 真实语境例句（影视来源）+ 中文翻译', style='List Bullet')
doc.add_paragraph('• 词组搭配 / 派生 / 词根 / 近义 多维信息', style='List Bullet')
doc.add_paragraph('• "下一词" / "记错了" 按钮（后悔修正机制）', style='List Bullet')

doc.add_heading('复习模式', level=3)
doc.add_paragraph('四选一选择题：展示单词+发音 → 提示先回想 → 4个同词性干扰项 → 答错标粉/正确标绿')

doc.add_heading('亮点与槽点', level=3)
add_table(doc,
    ['亮点 ✅', '槽点 ❌'],
    [
        ['三级反馈+释义遮挡=真正主动回忆', '英语专属，韩语空白'],
        ['"记错了"后悔机制减少算法误判', '壁纸资源大，不适合小程序'],
        ['认识后仍展示完整语境（不跳过学习）', 'Learn 3486 大数字可能劝退'],
        ['引导文案降低决策犹豫', ''],
        ['全屏壁纸首页=打开即审美享受', ''],
        ['极简3 Tab导航', ''],
    ])

# --- 2.2 疯狂背单词 ---
doc.add_heading('2.2 疯狂背单词 — 应试四选一 + 多模式练习', level=2)

doc.add_paragraph('面向专升本/四六级/考研等应试人群的背词工具，核心是四选一选择题 + 多种练习模式 + 遗忘曲线可视化。功能全面但偏"工具感"。')

doc.add_heading('页面结构（4 Tab）', level=3)
add_table(doc,
    ['页面', '功能'],
    [
        ['单词（首页）', '今日计划 + 新学/复习按钮 + 自由练习入口'],
        ['统计', '学习日历 + 成就 + 遗忘曲线对比图'],
        ['词典', '查词工具'],
        ['我的', '个人设置'],
    ])

doc.add_heading('背诵核心流程', level=3)
doc.add_paragraph('• 展示单词 + 音标 + 发音', style='List Bullet')
doc.add_paragraph('• 四选一选择题（选正确释义）', style='List Bullet')
doc.add_paragraph('• 答对绿色标记 / 答错红色标记 + 展示正确答案', style='List Bullet')
doc.add_paragraph('• 答题后展示：释义 + 双语例句 + 助记（谐音故事+插图）', style='List Bullet')

doc.add_heading('自由练习（5种模式）', level=3)
add_table(doc,
    ['模式', '形式'],
    [
        ['听力训练', '听音选义'],
        ['拼写练习', '看义拼词'],
        ['列表刷词', '快速浏览'],
        ['释义巩固', '看义选词'],
    ])

doc.add_heading('亮点与槽点', level=3)
add_table(doc,
    ['亮点 ✅', '槽点 ❌'],
    [
        ['遗忘曲线对比图——直观展示SRS效果', '四选一=被动识别，记忆深度有限'],
        ['门槛极低，碎片时间友好', '干扰项质量不高（跨词性）'],
        ['复习上限=新词×5，规则简单', '界面信息密集、留白少'],
        ['5种练习模式多维强化', '588天完成的数字劝退'],
        ['退出挽留弹窗', '无Streak社交激励'],
    ])

# --- 2.3 韩语U学院 ---
doc.add_heading('2.3 韩语U学院 — 韩语垂直 + 浏览式学习', level=2)

doc.add_paragraph('韩语综合学习 App，背词部分走纯浏览路线：展示释义 + 例句，用户自判"继续"或"太简单"。是唯一的韩语竞品参考。')

doc.add_heading('页面结构（5 Tab）', level=3)
add_table(doc,
    ['页面', '功能'],
    [
        ['背词', '首页，今日计划+打卡'],
        ['课程', '韩语课程'],
        ['学习中心', '综合资源'],
        ['发音', '发音训练'],
        ['我的', '个人数据'],
    ])

doc.add_heading('背诵核心流程', level=3)
doc.add_paragraph('每次5词一组：')
doc.add_paragraph('• 展示韩文 + 发音 + 收藏按钮', style='List Bullet')
doc.add_paragraph('• 释义直接展示（无遮挡，无主动回忆）', style='List Bullet')
doc.add_paragraph('• 韩文例句 + 中文翻译', style='List Bullet')
doc.add_paragraph('• 仅两个选项："继续背词" / "太简单"', style='List Bullet')
doc.add_paragraph()
p = doc.add_paragraph()
run = p.add_run('关键缺陷：没有"忘了"按钮，没有测试，没有主动回忆机制。')
run.bold = True
run.font.color.rgb = RGBColor(0xC8, 0x00, 0x00)

doc.add_heading('亮点与槽点', level=3)
add_table(doc,
    ['亮点 ✅', '槽点 ❌'],
    [
        ['"太简单"快速跳过已知词', '纯浏览无主动回忆=记忆效果极差'],
        ['韩文问候语增加沉浸感', '反馈只有二级，缺少"忘了"'],
        ['韩文例句+发音播放', '大量词无例句'],
        ['收藏/生词本功能', '释义不精炼（混入法律术语）'],
        ['词书分类覆盖面广', '无SRS间隔调度'],
        ['纠错入口（众包改善）', '5 Tab导航过于分散'],
    ])

# --- 2.4 多邻国 ---
doc.add_heading('2.4 多邻国 Duolingo — 游戏化之王', level=2)

doc.add_paragraph('全球最成功的语言学习 App，以行为心理学驱动的游戏化设计著称。不是纯背单词工具，而是综合语言技能训练平台。')

doc.add_heading('核心游戏化机制', level=3)
add_table(doc,
    ['机制', '心理学原理'],
    [
        ['Streak（连续天数）', '损失厌恶——断签焦虑'],
        ['XP + 排行榜', '社交比较 + 竞争驱动'],
        ['红心（Hearts）', '稀缺感——错误有代价'],
        ['宝石 + 道具', '可变奖励'],
        ['5分钟短会话', '极低启动门槛'],
        ['进度路径', '蔡格尼克效应（未完成冲动）'],
        ['IP形象（Duo猫头鹰）', '情感化连接'],
    ])

doc.add_heading('亮点与槽点', level=3)
add_table(doc,
    ['亮点 ✅', '槽点 ❌'],
    [
        ['游戏化设计教科书——Streak最强留存', '词汇深度不足（偏句子非系统背词）'],
        ['多种练习形式', '韩语内容质量一般（翻译腔）'],
        ['即时反馈+错误后立即纠正', '对有基础用户太慢'],
        ['5分钟短会话极低门槛', '游戏化过度可能"在玩非在学"'],
        ['进度可视化（路径/地图）', '重App形态，无法小程序复现'],
    ])

# ===== 三、横向对比 =====
doc.add_page_break()
doc.add_heading('三、横向对比：关键维度', level=1)

doc.add_heading('3.1 背诵核心机制对比', level=2)
add_table(doc,
    ['产品', '主动回忆', '反馈层级', 'SRS', '记忆效果'],
    [
        ['不背单词', '✅ 遮挡释义后自判', '3级（认识/模糊/忘了）', '✅', '⭐⭐⭐⭐⭐'],
        ['疯狂背单词', '❌ 四选一被动识别', '2级（对/错）', '✅', '⭐⭐⭐'],
        ['韩语U学院', '❌ 纯浏览', '2级（继续/太简单）', '❌', '⭐⭐'],
        ['多邻国', '⚠️ 部分', '2级（对/错）', '⚠️ 自适应', '⭐⭐⭐⭐'],
    ])

p = doc.add_paragraph()
run = p.add_run('结论：不背单词的"遮挡+三级反馈"是记忆效果最优方案，我们应采用此模式。')
run.bold = True

doc.add_heading('3.2 视觉风格对比', level=2)
add_table(doc,
    ['产品', '风格关键词', '背景', '信息密度'],
    [
        ['不背单词', '高级、克制、杂志感', '毛玻璃渐变/壁纸', '低（大留白）'],
        ['疯狂背单词', '活泼、工具感', '白底灰卡片', '高（功能密集）'],
        ['韩语U学院', '可爱、课堂感', '白底蓝顶', '中'],
        ['多邻国', '彩色、游乐场', '白/绿底', '中'],
    ])

p = doc.add_paragraph()
run = p.add_run('结论：对标不背单词"克制审美"，但用韩式极简（奶油白+低饱和蓝）替代毛玻璃。')
run.bold = True

doc.add_heading('3.3 导航复杂度对比', level=2)
add_table(doc,
    ['产品', 'Tab数', '学习入口层级'],
    [
        ['不背单词', '3', '首页直达（1步）'],
        ['疯狂背单词', '4', '首页直达（1步）'],
        ['韩语U学院', '5', '首页直达（1步）'],
        ['多邻国', '5', '首页直达（1步）'],
    ])

p = doc.add_paragraph()
run = p.add_run('结论：小程序应更极简，3 Tab 或更少。')
run.bold = True

# ===== 四、综合洞察 =====
doc.add_page_break()
doc.add_heading('四、综合洞察与市场机会', level=1)

doc.add_heading('4.1 市场空白', level=2)
doc.add_paragraph('1. 韩语 + 科学记忆 = 空白市场', style='List Number')
doc.add_paragraph('   • 韩语U学院有韩语但无科学机制；不背单词有科学机制但无韩语')
doc.add_paragraph('   • 没有产品同时做好"韩语 + 主动回忆 + SRS"')
doc.add_paragraph('2. 小程序形态 = 无竞争', style='List Number')
doc.add_paragraph('   • 所有竞品均为原生 App，我们的 1624 词精选词库完美适配小程序轻量形态')
doc.add_paragraph('   • 即开即用 + 微信社交裂变')
doc.add_paragraph('3. 审美差异化 = 低成本高感知', style='List Number')
doc.add_paragraph('   • 韩语U学院视觉平庸，韩式极简即可形成明显区隔')

# ===== 五、差异化定位 =====
doc.add_heading('五、我们的差异化定位', level=1)

p = doc.add_paragraph()
run = p.add_run('一句话定位：韩语精选 1624 词 × 科学主动回忆 × 小程序即开即用')
run.bold = True
run.font.size = Pt(12)

doc.add_paragraph()
add_table(doc,
    ['维度', '我们的选择', '依据'],
    [
        ['语种', '韩语专精', '市场空白，我们有母语级词库'],
        ['机制', '主动回忆+三级反馈+SRS', '不背单词验证的最优方案'],
        ['形态', '微信小程序', '轻量、即开即用、社交裂变'],
        ['审美', '韩式极简', '对标不背单词水准，区别于U学院'],
        ['词库', '1624词精选', '小而精，对标TOPIK分级'],
        ['交互', '极简（≤3页面）', '小程序天然要求精简'],
    ])

# ===== 六、核心流程 =====
doc.add_heading('六、核心学习流程建议', level=1)

doc.add_heading('首页', level=3)
doc.add_paragraph('• 韩文问候 + 今日任务卡片', style='List Bullet')
doc.add_paragraph('• [新词 X 个] [复习 Y 个]', style='List Bullet')
doc.add_paragraph('• 连续学习天数 + [开始学习] 按钮', style='List Bullet')

doc.add_heading('学习页', level=3)
doc.add_paragraph('• Step 1: 展示韩文（释义遮挡）→ 用户主动回忆', style='List Bullet')
doc.add_paragraph('• Step 2: 三级反馈（认识 / 模糊 / 忘了）', style='List Bullet')
doc.add_paragraph('• Step 3: 揭示全部信息（韩文+发音+词性+释义）', style='List Bullet')
doc.add_paragraph('• Step 4: "下一词" / "记错了"', style='List Bullet')
doc.add_paragraph('• "太简单" = 直接标记掌握跳过', style='List Bullet')

doc.add_heading('完成页', level=3)
doc.add_paragraph('• 今日数据：学习 X / 记住 Y / 正确率 Z%', style='List Bullet')
doc.add_paragraph('• [分享打卡] [返回首页]', style='List Bullet')

# ===== 七、功能优先级 =====
doc.add_page_break()
doc.add_heading('七、功能优先级矩阵', level=1)

doc.add_heading('MVP 必须做（P0/P1）', level=2)
add_table(doc,
    ['功能', '来源', '优先级'],
    [
        ['主动回忆（遮挡释义）', '不背单词', 'P0'],
        ['三级反馈（认识/模糊/忘了）', '不背单词+墨墨', 'P0'],
        ['SRS 间隔复习算法', '墨墨+疯狂背单词', 'P0'],
        ['"记错了"后悔修正', '不背单词', 'P0'],
        ['认识后仍展示完整信息', '不背单词', 'P0'],
        ['反馈引导文案', '不背单词', 'P0'],
        ['韩文发音播放', '韩语U学院', 'P0'],
        ['今日学习量展示', '全部竞品', 'P0'],
        ['"太简单"快速跳过', '韩语U学院', 'P1'],
        ['连续打卡（Streak）', '多邻国+疯狂背单词', 'P1'],
        ['学习完成页+数据统计', '全部竞品', 'P1'],
        ['退出挽留提示', '疯狂背单词', 'P2'],
    ])

doc.add_heading('后期迭代', level=2)
add_table(doc,
    ['功能', '来源', '阶段'],
    [
        ['遗忘曲线对比可视化', '疯狂背单词', 'V2'],
        ['韩文例句+发音', '韩语U学院+不背单词', 'V2'],
        ['打卡海报分享裂变', '通用', 'V2'],
        ['收藏/生词本', '韩语U学院', 'V2'],
        ['多种练习模式（听/写）', '疯狂背单词', 'V3'],
        ['随身听（音频复习）', '不背单词', 'V3'],
    ])

doc.add_heading('坚决不做', level=2)
add_table(doc,
    ['功能', '原因'],
    [
        ['全屏壁纸/毛玻璃', '小程序包体限制+性能'],
        ['5 Tab 复杂导航', '功能过重'],
        ['课程/发音独立模块', '偏离背词核心'],
        ['排行榜/社区', '冷启动无用户基础'],
        ['词根词缀/派生体系', '韩语不适用'],
        ['助记视频', '制作成本高'],
        ['游戏化关卡路径', '开发复杂度过高'],
    ])

# ===== 尾页 =====
doc.add_page_break()
doc.add_paragraph()
doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('— 报告完 —')
run.font.size = Pt(14)
run.font.color.rgb = RGBColor(0x99, 0x99, 0x99)

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('本报告基于实际产品截图分析（34张），所有结论均有视觉素材支撑。\n素材覆盖：不背单词(10张) / 疯狂背单词(9张) / 韩语U学院(8张) / 多邻国(7张)')
run.font.size = Pt(10)
run.font.color.rgb = RGBColor(0xAA, 0xAA, 0xAA)

# ===== 保存 =====
output_path = '/Users/kakami/Desktop/韩语知识库/竞品调研报告.docx'
doc.save(output_path)
print(f'✅ 已生成: {output_path}')
