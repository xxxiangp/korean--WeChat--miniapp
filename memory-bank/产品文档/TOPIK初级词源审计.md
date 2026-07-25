# TOPIK 初级词源审计

> 创建日期：2026-07-26
> 最后更新：2026-07-26
> 状态：外部来源池已建立 / 待人工复核与补词
> 用途：记录 TOPIK I（1-2级）词书的外部来源、覆盖差异和后续补词依据

---

## 一、结论先行

当前 `topik_beginner.json` 仍为候选版。本轮审计抓取公开 TOPIK I 词表后发现：

- 当前候选词书：1594 词
- 外部来源去重词池：2171 词
- 当前词书中被至少一个外部来源支持：1097 词
- 当前词书中未在本轮来源池出现：497 词
- 外部来源中当前词书缺失：1074 词
- 缺失词里项目现有主词库已包含：0 词
- 缺失词里项目现有主词库也没有：1074 词

这说明词书仍不能称为最终 TOPIK I 词书，必须继续补词和人工复核。

## 二、来源列表

| 来源 | 性质 | URL |
|------|------|-----|
| Tammy Korean / Learning Korean TOPIK I Vocabulary List 1671 | public TOPIK I vocabulary list; not an official fixed list | https://learning-korean.com/elementary/20210101-10466/ |
| KoreanTopik TOPIK 1 Vocabulary List 1850 | public TOPIK I vocabulary list; site-labeled 1850 beginner essential words; not an official fixed list | https://www.koreantopik.com/2024/05/topik-1-vocabulary-list-1850-for.html |

## 三、缺失词样例（前 100 条，优先显示多来源支持）

完整列表见 `memory-bank/数据文件/topik_i_source_audit.json`。

| 韩语 | 支持来源 | 支持数 | 项目主词库已有 | 英文释义提示 |
|------|----------|--------|----------------|--------------|
| 가요 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "song"} |
| 가족 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "family"} |
| 가지다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "have"} |
| 간단히 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "simply"} |
| 갈비탕 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "Galbitang, spareribs soup"} |
| 갈색 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "brown"} |
| 감기약 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "cold medicine"} |
| 감다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "close ~ (eyes)"} |
| 감사 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "thank"} |
| 값 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "price"} |
| 강아지 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "puppy"} |
| 갖다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "have"} |
| 거짓말 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "lie"} |
| 건너가다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "cross (a road)"} |
| 건너편 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "other side, opposite side"} |
| 걸리다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "get caught, take (time)"} |
| 걸어오다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "walk (come)"} |
| 검은색 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "black"} |
| 것 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "that, thing, it"} |
| 결정 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "decision"} |
| 경치 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "view, landscape"} |
| 계시다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "be, exist (honorific form)"} |
| 계절 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "season"} |
| 고등학생 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "high school student"} |
| 고맙다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "thank"} |
| 고속버스 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "express bus"} |
| 고프다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "hungry"} |
| 고향 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "hometown"} |
| 곳 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "place"} |
| 공 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "ball"} |
| 공부 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "study"} |
| 공짜 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "free"} |
| 공휴일 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "public holiday"} |
| 교통사고 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "traffic accident"} |
| 구 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "9"} |
| 구십 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "90"} |
| 구월 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "September"} |
| 국내 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "domestic"} |
| 국적 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "nationality, country of citizenship"} |
| 그 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "it"} |
| 그거 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "it"} |
| 그곳 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "there"} |
| 그날 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "that day"} |
| 그때 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "then, at that time"} |
| 그런 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "then, such"} |
| 그럼 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "then"} |
| 그렇다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "Yes, that's it."} |
| 그렇지만 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "nevertheless, but"} |
| 그리다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "draw"} |
| 그만 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "stop, finish"} |
| 그분 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "his, the person"} |
| 그저께 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "day before yesterday"} |
| 그쪽 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "there, the person"} |
| 그치다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "stop, end, cease"} |
| 글 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "post, sentence, character"} |
| 글쎄요 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "I do not know., well, I guess ~"} |
| 기간 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "term, period"} |
| 기름 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "oil, gasoline"} |
| 기뻐하다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "glad, delight"} |
| 기온 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "temperature"} |
| 까맣다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "black"} |
| 깎다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "cut, shave"} |
| 껌 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "chewing gum"} |
| 꽃집 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "florist"} |
| 꾸다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "dream"} |
| 끝내다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "finish"} |
| 나다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "occur, come out"} |
| 나중 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "later, after"} |
| 나흘 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "four days"} |
| 날 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "day"} |
| 날짜 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "date"} |
| 남 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "south, man"} |
| 남기다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "leave"} |
| 남녀 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "men and women"} |
| 남동생 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "younger brother"} |
| 남자 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "man"} |
| 남쪽 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "south"} |
| 남학생 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "male student"} |
| 내 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "of mine, my"} |
| 내다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "pay, put out"} |
| 내용 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "content"} |
| 넘어지다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "fall down, fall"} |
| 넷째 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "fourth"} |
| 노랗다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "yellow"} |
| 노트 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "note"} |
| 녹색 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "green"} |
| 녹차 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "green tea"} |
| 눈물 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "tear"} |
| 느낌 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "feeling"} |
| 늘다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "gain, increase"} |
| 다녀오다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "return, come back"} |
| 다니다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "go, commute"} |
| 다른 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "other ~, another ~, different ~"} |
| 단어 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "word"} |
| 달걀 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "egg"} |
| 달리다 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "run"} |
| 담배 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "tobacco"} |
| 답장 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "reply"} |
| 대학 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "university, college"} |
| 대학생 | tammy_1671, koreantopik_1850 | 2 | 否 | {"tammy_1671": "college student"} |

## 四、当前候选中未被来源池支持的词样例（前 80 条）

这些词不一定错误；只表示它们没有出现在本轮两个公开来源池中。后续需要按 TOPIK I 场景人工判断保留、降权或移出。

| ID | 韩语 | 中文释义 | 词性 |
|----|------|----------|------|
| 477 | 가스레인지 | 燃气灶 | 名词 |
| 1419 | 감동적이다 | 感动的 | 形容词 |
| 1344 | 감소하다 | 减少 | 动词 |
| 1291 | 감정 | 感情，情感 | 名词 |
| 1227 | 강의실 | 授课教室；讲堂 | 名词 |
| 525 | 개미 | 蚂蚁 | 名词 |
| 1476 | 개선하다 | 改善 | 动词 |
| 1240 | 개학 | 开学 | 名词 |
| 749 | 거스름돈 | 找零 | 名词 |
| 1363 | 거절하다 | 拒绝 | 动词 |
| 644 | 건조하다 | 干燥的 | 形容词 |
| 471 | 걸레 | 抹布；拖把 | 名词 |
| 1479 | 검색하다 | 检索，搜索 | 动词 |
| 1094 | 게 | 螃蟹 | 名词 |
| 1443 | 게다가 | 而且 | 副词 |
| 1145 | 게스트하우스 | 青年旅舍 | 名词 |
| 1023 | 게시물 | 帖子 | 名词 |
| 1496 | 격려하다 | 鼓励 | 动词 |
| 1426 | 결국 | 结果，最终 | 副词 |
| 1450 | 경력 | 经历，资历 | 名词 |
| 1357 | 경쟁하다 | 竞争 | 动词 |
| 1121 | 계산서 | 账单 | 名词 |
| 1459 | 고객 | 顾客 | 名词 |
| 946 | 고구마 | 红薯 | 名词 |
| 1098 | 고등어 | 青花鱼 | 名词 |
| 1365 | 고민하다 | 烦恼 | 动词 |
| 449 | 고속도로 | 高速公路 | 名词 |
| 922 | 고장나다 | 坏了（机器） | 动词 |
| 1484 | 공유하다 | 共享 | 动词 |
| 1478 | 관리하다 | 管理 | 动词 |
| 999 | 괜찮아요 | 没关系 | 叹词 |
| 450 | 교차로 | 十字路口 | 名词 |
| 1487 | 교환하다 | 交换 | 动词 |
| 1030 | 구독 | 订阅 | 名词 |
| 1031 | 구독자 | 订阅者 | 名词 |
| 870 | 구르다 | 滚 | 动词 |
| 825 | 구멍 | 洞 | 名词 |
| 1361 | 구분하다 | 区分 | 动词 |
| 940 | 국물 | 汤汁 | 名词 |
| 1155 | 궁궐 | 宫殿 | 名词 |
| 1429 | 그래도 | 即使那样 | 副词 |
| 740 | 그리워하다 | 想念 | 动词 |
| 823 | 그림자 | 影子 | 名词 |
| 697 | 글피 | 大后天 | 名词 |
| 1158 | 기념품 | 纪念品 | 名词 |
| 1366 | 기대하다 | 期待 | 动词 |
| 1477 | 기록하다 | 记录 | 动词 |
| 869 | 기어가다 | 爬行 | 动词 |
| 591 | 기침하다 | 咳嗽 | 动词 |
| 1159 | 길을잃다 | 迷路 | 动词 |
| 668 | 꽤 | 相当 | 副词 |
| 590 | 꿈꾸다 | 做梦 | 动词 |
| 524 | 나비 | 蝴蝶 | 名词 |
| 1114 | 나이프 | 刀（餐刀） | 名词 |
| 315 | 나중에 | 以后 | 副词 |
| 1205 | 난방 | 采暖；供暖 | 名词 |
| 632 | 날카롭다 | 锋利的 | 形容词 |
| 767 | 남자친구 | 男朋友 | 名词 |
| 1410 | 낯설다 | 陌生 | 形容词 |
| 848 | 냄새 맡다 | 闻 | 动词 |
| 806 | 넓이 | 面积 | 名词 |
| 634 | 네모나다 | 方的 | 形容词 |
| 595 | 노크하다 | 敲门 | 动词 |
| 725 | 노트북 | 笔记本电脑 | 名词 |
| 1057 | 녹음하다 | 录音 | 动词 |
| 1135 | 녹이다 | 融化；化开 | 动词 |
| 436 | 놀이공원 | 游乐园 | 名词 |
| 425 | 놀이터 | 游乐场 | 名词 |
| 555 | 농부 | 农民 | 名词 |
| 544 | 눈썹 | 眉毛 | 名词 |
| 1373 | 늘리다 | 增加，扩大 | 动词 |
| 1262 | 늦게 | 晚地；迟 | 副词 |
| 1208 | 다리미 | 熨斗 | 名词 |
| 903 | 다림질하다 | 熨衣服 | 动词 |
| 1393 | 다양하다 | 多样 | 形容词 |
| 599 | 다운로드하다 | 下载 | 动词 |
| 703 | 다음 달 | 下个月 | 名词 |
| 700 | 다음 주 | 下周 | 名词 |
| 879 | 담다 | 盛（饭） | 动词 |
| 1131 | 담백하다 | 清淡可口 | 形容词 |

## 五、下一步规则

1. 先补齐外部来源缺失词，优先处理两个来源共同支持的词。
2. 对项目主词库已有的词，复用既有释义、发音、quiz 和音频映射。
3. 对项目主词库没有的词，必须新增韩文、发音、词性、中文释义、干扰项，并记录英文释义提示和来源。
4. 对当前候选中未被来源支持的词，不能直接删除；要按 TOPIK I 主题、词频和是否日常高频人工复核。
5. 审计完成前不得 push 为正式版。
