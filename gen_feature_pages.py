# -*- coding: utf-8 -*-
"""生成 Working Mate 官网的功能详情页（每功能一页）+ 共享样式 + 首页「功能全景」卡片网格。

用法：
    python gen_feature_pages.py
产物：
    feature-<slug>.html      ×N
    feature.css              （详情页共享样式）
    index-v3.html            （把 <!--FEATURES_GRID--> 标记替换成全部功能卡片）

改内容只要改下面 FEATURES 列表，然后重跑本脚本。
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = "Working Mate"
GRID_MARK = "<!--FEATURES_GRID-->"

# ══════════════════════════════════════════════════════════════
#  功能数据（全部与实际客户端对齐）
# ══════════════════════════════════════════════════════════════
FEATURES = [
    {
        "slug": "models", "title": "多模型混合调度",
        "tag": "Multi-Model Router", "icon": "◧", "ico": "ico-blue",
        "sub": "本地 Ollama 与云端旗舰模型统一在一个对话框里，断网自动用本地，联网自动切云端；同一会话随手换模型，不用重启、不用改配置。",
        "facts": ["60+ 可接入模型", "本地 / 云端统一入口", "自动降级切换", "0 数据外传（本地模式）"],
        "what": [
            ("一个输入框，连通所有模型", "不用记 API、不用开一堆网页。DeepSeek、Qwen、GLM、Kimi、豆包、GPT、Claude、Gemini、OpenRouter 全量模型都在同一个下拉里。"),
            ("本地优先，断网也能跑", "接上 Ollama 即可完全离线：对话、文件操作、工作流编排都不依赖网络，数据不出本机。"),
            ("三档模型策略", "标准 / 专业 / 旗舰三档一键切换，系统按任务复杂度自动挑性价比最高的模型，也能手动指定。"),
            ("多模型自动降级", "一个模型限频或 5xx，自动切到下一个备选模型继续跑；只有余额不足、鉴权失败才停下并明确报错，不会静默失败。"),
            ("专家各带模型组", "17 位领域专家各自绑定「推理 / 通用 / 代码」三模型组，让写代码的用代码模型、写文案的用文案模型。"),
            ("同一会话实时切换", "聊到一半换模型，上下文不丢——真正意义上的「随手换脑子」。"),
        ],
        "steps": [
            "设置 → 模型与运行环境，选档位（标准 / 专业 / 旗舰）。",
            "需要离线就把本地 Ollama 打开，客户端会自动发现本地模型。",
            "在顶部模型下拉里选具体模型，或直接用「自动路由」让它自己挑。",
            "断网时自动落到本地模型，联网后自动恢复云端，无需手动干预。",
        ],
        "tech": [
            "统一 cloud_client 抽象层，本地 / 云端同一套调用签名。",
            "429 区分「限频」与「余额不足」：限频读 Retry-After 重试一次，余额不足立即停并提示充值。",
            "多模型 fallback 链：限频 / 5xx 才切换，鉴权类错误不切换（避免无意义重试烧钱）。",
            "模型按「档位 × 用途」索引，专家可直接引用模型组。",
        ],
        "shot": "assets/shots/home.png", "shot_cap": "同一个输入框，连通本地与云端",
        "related": ["experts", "workflow"],
    },
    {
        "slug": "experts", "title": "17 位领域专家协作",
        "tag": "Expert Team", "icon": "◇", "ico": "ico-violet",
        "sub": "给一个目标，AdminAgent 自动拆成子任务、派给对应领域的专家、再汇总成一份结果。你不用自己写提示词，也不用自己拆步骤。",
        "facts": ["17 位领域专家", "自动拆任务 / 派单", "每子任务最多 10 轮工具调用", "结果自动汇总"],
        "what": [
            ("一句话派活", "输入「帮我把这个 Excel 里三个月的销售数据做成趋势图并写一段分析」，系统会自己拆成「读表 → 清洗 → 绘图 → 写分析」并分派执行。"),
            ("17 位领域专家", "科研、视频短剧创作、图片设计、音乐生成、炒股、金融精算、一人企业、软件架构、AI、提示词、全栈 Codex、办公、代码、写作文案、数据科学、系统运维、通用。"),
            ("AdminAgent 负责拆解", "主控 Agent 读你的目标 → 生成子任务清单（含依赖关系）→ 逐个派发给合适的专家执行。"),
            ("专家各带模型组", "每位专家绑定「推理 / 通用 / 代码」三模型组，并在图像 / 视频 / 音乐维度上绑定对应的生成模型。"),
            ("工具调用有边界", "每个子任务最多 10 轮工具调用，白名单 / 黑名单双重限制，防止一个任务无限跑或调用危险工具。"),
            ("汇总成一份交付", "全部子任务完成后自动合并，输出一份可直接用的结果，而不是一堆零散片段。"),
        ],
        "steps": [
            "把顶部「Agent 模式」打开。",
            "直接描述你的目标（越具体越好），不用自己拆步骤。",
            "Agent 会先给你一份子任务清单，确认后开始执行。",
            "执行过程中可以随时「急停」，也可以看到每个子任务的状态与产物。",
        ],
        "tech": [
            "拆解阶段与执行阶段共用同一个多模型降级链，限频时不会让整个任务崩掉。",
            "子任务失败只跳过依赖它的下游，其余分支继续跑。",
            "跨空间调用有上限（防循环引用），避免专家之间互相派活成死循环。",
            "拆解结果解析失败时会抛出真实错误原因，而不是静默返回空任务。",
        ],
        "shot": "assets/shots/agent-split.png", "shot_cap": "目标 → 子任务 → 专家执行",
        "related": ["workflow", "spaces"],
    },
    {
        "slug": "memory", "title": "四层记忆系统",
        "tag": "Memory", "icon": "◈", "ico": "ico-mint",
        "sub": "它不是每次都从零开始。关键事实、历史会话、跑通过的流程、你的偏好与沟通风格，分别沉淀在四层记忆里，越用越懂你。",
        "facts": ["4 层记忆结构", "中文 n-gram 检索", "本地 SQLite 存储", "容量上限强制筛选"],
        "what": [
            ("L1 常驻记忆", "最重要的事实与偏好，每轮对话都注入。因为有容量上限，系统被强迫只留最有价值的那几条。"),
            ("L2 会话归档", "全部历史会话存进本地数据库，按关键词命中数召回最相关的几段，需要时才注入，不占用常驻预算。"),
            ("L3 技能库", "跑通过的流程会被自动抽成可复用技能——同样的活第二次只要一句话。"),
            ("L4 用户画像", "沟通风格、领域知识、做事习惯长期积累，让回复越来越像在跟你说话。"),
            ("换话题不断片", "上周聊过的需求，这周接着来；换到别的话题再回来，它还记得上下文。"),
            ("记忆可查可清", "侧栏「记忆文件」随时查看，觉得记错了可以清空或纠正。"),
        ],
        "steps": [
            "正常聊天即可，不需要手动「记住」。",
            "侧栏「记忆文件」查看当前 L1 常驻记忆与 L4 画像。",
            "「记忆清理」可以一键清空某层记忆，或删掉指定会话。",
            "想让它记住某条硬性规则，直接在对话里说明即可被判为长期事实。",
        ],
        "tech": [
            "中文用 2-4 字 n-gram 切片配合英文串分词，解决整串 LIKE 命中率低的问题。",
            "L2 用命中数评分排序，SQLite FTS5 不可用时自动降级为普通表 + LIKE 检索。",
            "轻量摘要不调 LLM，用首尾轮次拼接，控制成本。",
            "每层都有字符上限，保护记忆不被过时内容淹没。",
        ],
        "shot": "assets/shots/home.png", "shot_cap": "记忆文件随时可查可清",
        "related": ["skills", "privacy"],
    },
    {
        "slug": "skills", "title": "技能自动沉淀",
        "tag": "Self-Evolving Skills", "icon": "▲", "ico": "ico-amber",
        "sub": "你跑通过的流程，系统会自动把它抽成一条可复用技能存进技能库。第二次遇到同样的活，一句话就能复现整套动作。",
        "facts": ["自动抽取工作流", "技能库集中管理", "本地存储", "可复用可分享"],
        "what": [
            ("跑一次，变成技能", "一次完整的操作流程（读文件 → 处理 → 输出）跑通后，被自动抽取成结构化的可复用技能。"),
            ("第二次只要一句话", "下次直接说「照上次那样处理」，系统从技能库匹配并执行，不用你重新描述步骤。"),
            ("技能库可视化", "侧栏「技能库」集中浏览、搜索、启用或删除已有技能。"),
            ("和四层记忆打通", "技能属于 L3 层，和工作流、专家协作共享同一套记忆体系。"),
            ("失败不污染技能库", "只有真正跑通的流程才会被沉淀，半途失败的不会被记成技能。"),
            ("本地存储", "技能库存在你本机，不上传云端。"),
        ],
        "steps": [
            "照常让 Agent 完成一件有多步的活。",
            "任务成功结束后，系统自动抽取技能并入库。",
            "打开侧栏「技能库」确认新技能已收录（可改名、可删除）。",
            "下次直接引用该技能，或让 Agent 自动匹配。",
        ],
        "tech": [
            "技能抽取与工作流引擎共用同一套节点 / 步骤模型。",
            "技能以本地文件形式存放，便于备份与迁移。",
            "与 L1/L2 记忆分离，避免技能文本挤占常驻记忆预算。",
        ],
        "shot": "assets/shots/skill-hub.png", "shot_cap": "技能库：跑通即沉淀",
        "related": ["memory", "workflow"],
    },
    {
        "slug": "workflow", "title": "节点式工作流画布",
        "tag": "Workflow Canvas", "icon": "◎", "ico": "ico-blue",
        "sub": "像搭积木一样把 AI 串成流水线：拖节点、连线、跑起来。每一步都能单独预览、单独重跑、单独改提示词——提示词既能自己手写，也能让 AI 代写。",
        "facts": ["10 种节点类型", "拖拽 + 自动连线 + 自动排版", "单节点重跑", "提示词 DIY 或 AI 代写"],
        "what": [
            ("10 种节点，覆盖全流程", "LLM 文本、分镜拆解、AI 配图、AI 视频、AI 音乐、视频合成、工具节点、文本卡片、本地图片、本地音乐。"),
            ("拖拽 + 连线", "左侧节点库拖到画布，按住节点右侧拖到目标即可连线；也有「⚡ 自动连线」按类型逻辑一次接好。"),
            ("自动排版", "「⌗ 自动排版」按依赖关系分层排列，节点散了一键归位。"),
            ("每步即时预览", "点任意节点，右侧立刻显示该节点的文本 / 图片 / 视频 / 音频产物，带播放器。"),
            ("提示词完全可 DIY", "每个文本参数都是多行编辑器，想怎么写就怎么写；支持 {{节点名}} 占位符引用上游产物。"),
            ("🪄 AI 帮我写提示词", "给一句话需求，AI 按节点类型自动写出专业提示词（分镜师 / 美术指导 / 音乐制作人角色各有专用模板），生成后仍可继续手改。"),
            ("模板一键开跑", "内置 AI 短剧、音乐单曲、主题概念图等现成流程，改个主题就能跑。"),
            ("可靠性分析", "「🛡 可靠性分析」检查缺参数、缺 Key、断链、成环，给出评分和修复建议。"),
        ],
        "steps": [
            "打开侧栏「工作流」，从左侧拖入需要的节点（或直接「载入模板」）。",
            "连线：按住节点右侧拖到目标节点；懒人可直接点「⚡ 自动连线」。",
            "点节点，在右侧把提示词改成本次任务的内容（手写或点 🪄 让 AI 写）。",
            "「▶ 运行工作流」跑全流程，单节点失败不影响其余分支。",
            "画布可存成 JSON，「保存 JSON / 打开 JSON」方便复用与分享。",
        ],
        "tech": [
            "节点用扁平 dict + deps 表达依赖，引擎按拓扑串行执行，失败分支自动跳过下游。",
            "占位符引用上游产物，支持取列表第 N 项（如分镜第 1 个镜头）。",
            "参数按类型自动归一（时长转整数、纯音乐转布尔），避免云端接口报类型错。",
            "LLM 节点返回值做错误标记识别，避免把报错文本当成剧本流到下游。",
        ],
        "shot": "assets/shots/agent-split.png", "shot_cap": "节点画布：拖拽、连线、逐节点预览",
        "related": ["media", "experts"],
    },
    {
        "slug": "media", "title": "AI 媒体工厂",
        "tag": "AI Media Studio", "icon": "▶", "ico": "ico-coral",
        "sub": "从一句主题到一条成片：剧本 → 分镜 → AI 视频镜头 → 背景配乐 → 字幕 → 合成，整条链路内置在客户端里，不用来回切七八个网站。",
        "facts": ["剧本 / 分镜 / 视频 / 配乐", "字幕 + GIF", "短视频竖屏 9:16", "结果自动归档"],
        "what": [
            ("剧本生成", "给一个主题，产出 60 秒三镜头微短剧剧本，并自动切出每个镜头的画面提示词。"),
            ("分镜拆解", "把剧本里的镜头描述自动提取成结构化列表，逐个喂给视频节点。"),
            ("AI 视频镜头", "调用文生视频模型生成每个镜头，支持竖屏 9:16、时长可调，可单镜头重跑。"),
            ("背景配乐", "按剧本情绪生成纯音乐主题曲，或让 AI 写带歌词的完整歌曲。"),
            ("AI 配图", "电影感构图的概念图、封面图、分镜参考图，比例可选。"),
            ("字幕与 GIF", "自动生成字幕文件，也能把片段导出成 GIF 动图。"),
            ("视频合成", "把多个镜头按顺序合成一条成片输出。"),
            ("本地素材可插入", "自己的图片、音乐可以直接拖进工作流当参考图或配乐，和 AI 产物混合编排。"),
        ],
        "steps": [
            "工作流 → 载入「🎬 AI 短剧（3 镜头 + 配乐）」模板。",
            "把主题改成本次内容（如「一只打工小龙的日常」）。",
            "点剧本节点，手写剧本或点 🪄 让 AI 写；确认后运行。",
            "逐节点预览：先看剧本与分镜，再看生成的镜头视频与配乐。",
            "合成节点输出成片；产物自动落到本次任务的归档目录。",
        ],
        "tech": [
            "视频 / 音乐 / 图像分别对接可灵、Suno、图像生成模型，走统一的工具注册表。",
            "媒体节点按次计费，界面对消耗有明确提示（免费版可先用本地能力练流程）。",
            "镜头数量、比例、时长都可编辑；镜头提示词支持硬编码覆盖上游。",
            "产物路径自动回填到节点，下次重跑可直接复用。",
        ],
        "shot": "assets/shots/cards-video.png", "shot_cap": "剧本 → 分镜 → 镜头 → 配乐",
        "related": ["workflow", "experts"],
    },
    {
        "slug": "modules", "title": "六大行业场景模块",
        "tag": "Scenarios", "icon": "▦", "ico": "ico-mint",
        "sub": "研究、视频、图片、金融、软件、增长——六个开箱即用的场景入口，每个都预置了对应的专家、工具与快捷卡片，点进去就能用。",
        "facts": ["6 大场景", "预置卡片快捷开工", "可切多语言", "本地 / 云端都可用"],
        "what": [
            ("研究做调研", "论文检索、资料整理、结构化摘要与对比，适合写综述和开题。"),
            ("视频与图片创作", "短视频脚本到成片、配图与封面设计，接创作类专家。"),
            ("金融与投资", "行情数据、公司信息、做多逻辑与风险点梳理，接炒股大师 / 金融精算师。"),
            ("软件与代码", "需求拆解、代码生成、报错排查、顺手跑脚本，接软件架构师 / 全栈 Codex。"),
            ("增长与营销", "选题、文案、活动策划、增长实验设计。"),
            ("每个模块都有快捷卡", "不用从零开始想提示词，直接点卡片就用现成的任务模板。"),
        ],
        "steps": [
            "侧栏「NAVIGATION」里选一个场景（研究 / 视频 / 图片 / 金融 / 软件 / 增长）。",
            "点场景里的快捷卡片，或直接描述需求。",
            "需要跨场景时，项目空间可以把多个场景的产物汇总到一起。",
        ],
        "tech": [
            "场景卡片只是「任务模板 + 专家 + 工具」的组合，全部本地定义，可自行增删。",
            "场景共用同一套工具注册表与记忆体系，产物互通。",
            "界面支持 10 种语言，场景卡片文案跟随切换。",
        ],
        "shot": "assets/shots/cards-research.png", "shot_cap": "场景卡片：点一下就开始干活",
        "related": ["experts", "spaces"],
    },
    {
        "slug": "spaces", "title": "项目空间 & 任务中心",
        "tag": "Projects & Tasks", "icon": "⬢", "ico": "ico-violet",
        "sub": "一个目标一个空间，多个任务并行推进、互不串味；所有产物、日志、上下文都归档在空间里，随时回来接着做。",
        "facts": ["多任务并行", "空间级上下文隔离", "产物自动归档", "看板式进度"],
        "what": [
            ("项目空间", "给一个项目开一个空间，它的目标、附件、产物、对话历史都独立存放，不会被别的项目污染。"),
            ("多任务并行", "同一个空间里可以同时推进多个子任务，各自跑各自的进度。"),
            ("任务中心看板", "所有任务集中在一个看板里：状态、耗时、产物、失败原因一目了然。"),
            ("上下文总线", "空间之间可以有限度地互相引用产物；调用次数有上限，防止互相依赖成环。"),
            ("产物归档", "生成的文件、图片、视频、表格自动落到空间目录，不用自己找。"),
            ("随时接着做", "关掉客户端再打开，空间还在，进度还在。"),
        ],
        "steps": [
            "侧栏「项目空间」→ 新建空间，写清目标并挂上参考文件。",
            "在空间里把目标交给 Agent，它会拆成多个子任务并行推进。",
            "「任务中心」看整体进度与每个任务的产物。",
            "完成后在空间目录取走全部产物；需要继续迭代就在同一个空间里接着说。",
        ],
        "tech": [
            "空间之间通过上下文总线传递产物引用，跨空间调用有次数上限防止循环引用。",
            "任务状态与产物路径持久化，重启不丢。",
            "每个空间的执行日志独立留存，便于回溯是哪一步出的问题。",
        ],
        "shot": "assets/shots/project-spaces.png", "shot_cap": "项目空间：目标、任务、产物都在一处",
        "related": ["task_center", "automation"],
    },
    {
        "slug": "task_center", "title": "任务中心",
        "tag": "Task Center", "icon": "▤", "ico": "ico-blue",
        "sub": "所有跑过的任务集中在一个看板：谁在跑、跑到哪一步、用了多久、产出了什么、为什么失败——一眼看清。",
        "facts": ["集中看板", "状态实时刷新", "失败原因可溯", "产物一键打开"],
        "what": [
            ("一屏看全部", "不管是对话触发的、Agent 拆的、还是定时任务跑的，全部汇到同一个列表。"),
            ("实时状态", "排队中 / 执行中 / 已完成 / 失败 / 已跳过，状态变化即时刷新。"),
            ("失败看得懂", "失败不是只报一句「出错」，而是给出具体环节与原因（缺 Key、限频、文件不存在……）。"),
            ("产物直达", "点开任务即可打开它产出的文件、图片、视频、表格。"),
            ("配合工作流用", "工作流的每个节点执行结果也会落到任务记录里，方便定位是哪一步的问题。"),
        ],
        "steps": [
            "侧栏「任务中心」查看全部任务。",
            "点单个任务看详情：步骤、耗时、产物、日志。",
            "失败任务可定位原因后重跑该步骤。",
        ],
        "tech": [
            "任务与步骤两级结构，步骤级记录工具名、参数、耗时与结果。",
            "执行与 UI 线程分离，长任务不卡界面；线程异常退出时按钮状态会自动复位。",
        ],
        "shot": "assets/shots/task-center.png", "shot_cap": "任务中心：状态、耗时、产物",
        "related": ["spaces", "workflow"],
    },
    {
        "slug": "automation", "title": "自动化定时任务",
        "tag": "Automation", "icon": "◔", "ico": "ico-amber",
        "sub": "让 AI 按你定的节奏自己干活：每天早上整理资讯、每周汇总数据、到点提醒你——不盯着也会跑。",
        "facts": ["定时 / 周期执行", "本地调度", "执行历史可查", "失败可见"],
        "what": [
            ("一句话建任务", "「每天早上 9 点帮我把昨天的行业新闻整理成一份摘要」——说完就有了一条自动化。"),
            ("周期与一次性都支持", "每天、每周、每月，或者只在指定时间执行一次。"),
            ("本地调度", "调度与数据都在本机，不上传云端。"),
            ("执行历史", "跑过几次、每次结果如何、有没有失败，都有记录。"),
            ("可暂停可删除", "不想要了随时暂停或删掉。"),
        ],
        "steps": [
            "侧栏「自动化」→ 新建，写下要做什么。",
            "设定时间与频率（每天 / 每周 / 指定时间一次）。",
            "保存后在列表里查看下次执行时间与历史结果。",
        ],
        "tech": [
            "自动化定义与运行状态分别持久化，重启后调度不丢。",
            "每次执行独立记录结果，便于判断是内容问题还是环境问题。",
        ],
        "shot": "assets/shots/automation.png", "shot_cap": "按你定的节奏自动干活",
        "related": ["spaces", "privacy"],
    },
    {
        "slug": "gui", "title": "GUI 自动化",
        "tag": "Computer Control", "icon": "⊙", "ico": "ico-coral",
        "sub": "让 AI 直接操控本机上的其他程序：点按钮、填表单、翻菜单——那些没有 API 的老软件也能被自动化。",
        "facts": ["模拟鼠标键盘", "开启前能力检测", "每个操作可要求确认", "可随时关闭"],
        "what": [
            ("像人一样操作界面", "AI 会先「看」当前窗口，再决定点哪里、输入什么，逐步推进任务。"),
            ("开启前先做能力检测", "系统会先检查当前环境是否支持，不支持就直接告诉你原因，而不是开了之后一直失败。"),
            ("操作前请求确认", "默认每次关键操作都会问你一声；开了免确认模式才会自动放行。"),
            ("高危动作仍然拦截", "删除、覆盖等破坏性操作不会被免确认放行。"),
            ("随时可关", "一键关闭，AI 立刻失去键鼠控制权。"),
        ],
        "steps": [
            "设置 → 开启「GUI 自动化」，先通过能力检测。",
            "描述要完成的操作（越具体越好）。",
            "按提示确认每一步关键动作。",
            "任务结束后关闭开关。",
        ],
        "tech": [
            "能力检测在开启时执行并缓存结果，避免执行中途才发现环境不支持。",
            "操作粒度可配置，默认走逐条确认。",
            "与免确认模式联动：只有显式开启免确认才会跳过弹窗确认。",
        ],
        "shot": "assets/shots/automation.png", "shot_cap": "没有 API 的老软件也能自动化",
        "related": ["safety", "experts"],
    },
    {
        "slug": "safety", "title": "安全护栏：免确认 & 急停",
        "tag": "Safety", "icon": "⛨", "ico": "ico-mint",
        "sub": "该放的权放下去，该拦的拦得住。写操作可以逐条确认，也可以开免确认提速——但高危动作永远拦截，删除永远走回收站。",
        "facts": ["操作分级：WARNING / BLOCKED", "免确认模式", "一键急停", "删除走回收站"],
        "what": [
            ("默认逐条确认", "AI 每次要写文件、改数据、执行命令，都会先弹窗告诉你，你点同意才执行。"),
            ("免确认模式（提速档）", "信任之后打开它，常规写操作不再逐条弹窗，一口气跑完；适合已经验证过的重复流程。"),
            ("高危操作依然拦截", "BLOCKED 级别的破坏性动作不会被免确认放行，永远需要你点头。"),
            ("删除走回收站", "AI 的删除操作默认进回收站而不是直接抹掉，误删能捞回来。"),
            ("一键急停", "Agent 执行链跑到一半发现不对，随时急停，正在跑的任务立即收尾退出。"),
            ("工具白名单 / 黑名单", "可被调用的工具限定在白名单内，黑名单工具任何情况下都调不到。"),
        ],
        "steps": [
            "默认就是「每次操作弹窗确认」，什么都不用设置。",
            "信任度够了再开「免确认」，开启时会让你确认一次。",
            "开启后随时可以从顶栏关闭，恢复逐条确认。",
            "执行中发现不对，点「停止」急停当前任务。",
        ],
        "tech": [
            "操作按风险分级：WARNING 可被免确认放行，BLOCKED 永远拦截。",
            "工具调用有白名单 + 黑名单双重限制，单子任务最多 10 轮调用。",
            "删除统一走回收站备份路径，保留可恢复性。",
        ],
        "shot": "assets/shots/home.png", "shot_cap": "该放的权放下去，该拦的拦得住",
        "related": ["gui", "privacy"],
    },
    {
        "slug": "files", "title": "真实干文件",
        "tag": "Real File Work", "icon": "◧", "ico": "ico-blue",
        "sub": "它不是只会聊天：读你的文档表格、改内容、生成新文件、跑脚本、批量处理——干完直接把文件交给你。",
        "facts": ["读写 Office / 表格", "执行脚本", "批量处理", "拖拽 / 粘贴图片"],
        "what": [
            ("读得懂你的文件", "把 Word、Excel、PPT、PDF、图片直接拖进来，它读完就能基于内容干活。"),
            ("改完还是那个格式", "在原格式上修改并另存，不是给你一段文本让你自己复制回去。"),
            ("生成新文件", "表格、报告、清单、图表，直接产出可打开的文件。"),
            ("跑脚本", "需要批处理时直接执行脚本，输出结果回填到对话。"),
            ("拖拽与粘贴", "文件拖进输入框即成为上下文；剪贴板里的图片 Ctrl+V 直接变成附件。"),
            ("产物归档", "生成的文件落到本次任务目录，方便统一取走。"),
        ],
        "steps": [
            "把文件拖进输入框（或复制图片后 Ctrl+V 粘贴）。",
            "说明要做什么：「按月份汇总这个表，并画趋势图」。",
            "AI 处理完直接给你新文件，点开就能用。",
        ],
        "tech": [
            "文件读写走统一工具层，与工作流节点共用同一套能力。",
            "大文件先做结构解析再处理，避免把整份文档塞进上下文。",
            "生成的产物路径回填，便于后续引用与二次处理。",
        ],
        "shot": "assets/shots/cards-software.png", "shot_cap": "拖进来，改完还给你一个文件",
        "related": ["workflow", "spaces"],
    },
    {
        "slug": "i18n", "title": "多语言界面",
        "tag": "i18n", "icon": "⌘", "ico": "ico-violet",
        "sub": "界面支持 10 种语言实时切换，切换后立刻生效，不用重启。给海外用户或团队协作都方便。",
        "facts": ["10 种语言", "实时切换", "界面 + 场景卡片同步", "可继续扩展"],
        "what": [
            ("10 种语言", "简体中文、English、日本語、한국어、Deutsch、Français、Español、Português、Русский、العربية。"),
            ("切换立即生效", "设置里换语言，界面文案立刻跟着变，不需要重启客户端。"),
            ("覆盖到位", "主界面、设置、工作流画布、场景卡片文案都走同一套多语言。"),
            ("翻译可扩展", "语言资源以独立文件存放，新增语种只需补一份文案。"),
        ],
        "steps": [
            "设置 → 界面语言，选一个语种。",
            "若提示需要重启，重启一次即可全量生效。",
        ],
        "tech": [
            "所有界面文案通过运行时翻译函数取值，避免导入期就把文案固化成中文。",
            "语言资源独立成文件，便于校对与增补。",
        ],
        "shot": None, "shot_cap": "",
        "related": ["modules", "privacy"],
    },
    {
        "slug": "privacy", "title": "本地优先 & 隐私",
        "tag": "Local First", "icon": "⚿", "ico": "ico-amber",
        "sub": "对话、记忆、知识库、技能、产物默认全部存在你自己的电脑上。不联网也能用完整能力，联网只是为了调用你主动选择的云端模型。",
        "facts": ["0 数据外传（本地模式）", "断网可用", "数据全在本机", "本地数据库存储"],
        "what": [
            ("数据留在本机", "对话历史、四层记忆、技能库、项目产物都以本地文件 / 本地数据库形式存放。"),
            ("断网可用", "接上本地模型后，对话、文件操作、工作流编排完全不依赖网络。"),
            ("联网是你主动的选择", "只有当你选择使用云端模型或云端生成时，相关内容才会发给对应服务商。"),
            ("一键清理", "「记忆清理」可以清空指定记忆层或删除历史会话，清完就是真的没了。"),
            ("没有账号也能用", "免费版不强制注册，本地能力开箱即用。"),
        ],
        "steps": [
            "需要完全离线时，只用本地模型即可。",
            "想清空记录：侧栏「记忆清理」。",
            "担心某次对话内容敏感，就别选云端模型。",
        ],
        "tech": [
            "本地存储使用 SQLite 与本地目录，不依赖任何自建云服务。",
            "云端调用仅走你配置的服务商 Key，直连对应 API。",
            "记忆分层各自可清理，避免「清一个把全部清掉」。",
        ],
        "shot": "assets/shots/home.png", "shot_cap": "数据全在本机，断网也能跑",
        "related": ["memory", "safety"],
    },
]

BY_SLUG = {f["slug"]: f for f in FEATURES}

NAV = """<nav class="top" id="topnav">
  <div class="top-in">
    <a href="index-v3.html" class="logo"><img src="images/favicon.png" alt="Working Mate"></a>
    <div class="nav-links">
      <a href="index-v3.html#features">功能</a>
      <a href="index-v3.html#workflow">工作流</a>
      <a href="index-v3.html#models">模型</a>
      <a href="pricing.html">价格</a>
    </div>
    <div class="nav-right">
      <a href="index-v3.html#pricing" class="btn btn-amber">免费下载</a>
    </div>
  </div>
</nav>"""

FOOT = """<footer>
  <div class="wrap foot">
    <div>© 2026 Working Mate · 本地优先的 AI 工作间</div>
    <div class="foot-links">
      <a href="index-v3.html#features">功能</a>
      <a href="privacy.html">隐私</a><a href="terms.html">条款</a><a href="refunds.html">退款</a>
    </div>
  </div>
</footer>"""


def _li(items, cls="fcard"):
    return "".join(
        f'<div class="{cls}"><h3>{t}</h3><p>{d}</p></div>' for t, d in items
    )


def _steps(items):
    return "".join(
        f'<li><span class="n">{i+1}</span><div>{s}</div></li>' for i, s in enumerate(items)
    )


def _facts(items):
    return "".join(f'<span class="fchip">{x}</span>' for x in items)


def _tech(items):
    return "".join(f"<li>{x}</li>" for x in items)


def _shot(f):
    if not f.get("shot"):
        return ""
    return f"""
  <section class="fsec reveal">
    <h2>看一眼</h2>
    <figure class="fshot">
      <img src="{f['shot']}" alt="{f['title']} 界面截图" loading="lazy">
      <figcaption>{f.get('shot_cap','')}</figcaption>
    </figure>
  </section>"""


def _related(f):
    cards = []
    for s in f.get("related", []):
        r = BY_SLUG.get(s)
        if not r:
            continue
        cards.append(
            f'<a class="frel" href="feature-{r["slug"]}.html">'
            f'<span class="fico sm {r["ico"]}">{r["icon"]}</span>'
            f'<span><b>{r["title"]}</b><em>{r["tag"]}</em></span><i>→</i></a>'
        )
    if not cards:
        return ""
    return f"""
  <section class="fsec reveal">
    <h2>相关功能</h2>
    <div class="frels">{''.join(cards)}</div>
  </section>"""


def render(f):
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{f['title']} · {SITE} 功能</title>
<meta name="description" content="{f['sub'][:110]}">
<link rel="stylesheet" href="feature.css">
</head>
<body>
{NAV}

<header class="fhero">
  <div class="aurora aurora-1 on"></div>
  <div class="wrap fhero-in">
    <a class="fback" href="index-v3.html#features">← 返回功能全景</a>
    <div class="fico {f['ico']}">{f['icon']}</div>
    <div class="ftag">{f['tag']}</div>
    <h1>{f['title']}</h1>
    <p class="fsub">{f['sub']}</p>
    <div class="facts">{_facts(f['facts'])}</div>
    <div class="fcta-row">
      <a href="index-v3.html#pricing" class="btn btn-amber">免费下载体验</a>
      <a href="index-v3.html#features" class="btn btn-ghost">看其它功能</a>
    </div>
  </div>
</header>

<main class="wrap">
  <section class="fsec reveal">
    <h2>它能做什么</h2>
    <div class="fgrid">{_li(f['what'])}</div>
  </section>

  <section class="fsec reveal">
    <h2>怎么用</h2>
    <ol class="fsteps">{_steps(f['steps'])}</ol>
  </section>

  <section class="fsec reveal">
    <h2>技术亮点</h2>
    <ul class="fpoints">{_tech(f['tech'])}</ul>
  </section>
{_shot(f)}
{_related(f)}

  <section class="fsec fend reveal">
    <div class="fend-in">
      <h2>现在就试试「{f['title']}」</h2>
      <p>免费版永久可用，本地能力开箱即用，不需要信用卡。</p>
      <a href="index-v3.html#pricing" class="btn btn-amber">免费下载 {SITE}</a>
    </div>
  </section>
</main>

{FOOT}
<script>
const n=document.getElementById('topnav');
addEventListener('scroll',()=>n.classList.toggle('scrolled',scrollY>40),{{passive:true}});
const io=new IntersectionObserver(es=>{{es.forEach(e=>{{if(e.isIntersecting){{e.target.classList.add('in');io.unobserve(e.target)}}}})}},{{threshold:.12,rootMargin:'0px 0px -8% 0px'}});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
</script>
</body>
</html>
"""


def grid_html():
    cards = []
    for f in FEATURES:
        cards.append(
            f'<a class="b-card fcard-link reveal" href="feature-{f["slug"]}.html">'
            f'<div class="ico {f["ico"]}">{f["icon"]}</div>'
            f'<h3>{f["title"]}</h3><p>{f["facts"][0]} · {f["facts"][1]}</p>'
            f'<span class="go">查看详情 →</span></a>'
        )
    return (
        '<section class="zone" id="features">\n'
        '  <div class="wrap">\n'
        '    <div class="zone-head reveal" style="margin:0 auto 40px;text-align:center;max-width:660px">\n'
        '      <div class="zone-tag">All Features</div>\n'
        '      <h2>全部功能，点开看细节</h2>\n'
        '      <p style="color:var(--text2);margin-top:12px">每张卡片都能点进去看完整介绍：能做什么、怎么用、技术亮点。</p>\n'
        '    </div>\n'
        '    <div class="feature-grid">\n      ' + "\n      ".join(cards) + '\n    </div>\n'
        '  </div>\n'
        '</section>'
    )


def main():
    for f in FEATURES:
        (HERE / f"feature-{f['slug']}.html").write_text(render(f), encoding="utf-8")
    print(f"[ok] 生成 {len(FEATURES)} 个详情页")

    css = (HERE / "feature.css").write_text(FEATURE_CSS, encoding="utf-8")
    print("[ok] 写入 feature.css")

    idx = HERE / "index-v3.html"
    if idx.exists():
        html = idx.read_text(encoding="utf-8")
        if GRID_MARK in html:
            html = html.replace(GRID_MARK, grid_html())
            idx.write_text(html, encoding="utf-8")
            print("[ok] 首页卡片网格已注入")
        else:
            print(f"[skip] 首页没有找到标记 {GRID_MARK}（先手动加一行再跑）")
    print("完成。")


FEATURE_CSS = r"""
/* ═══ 功能详情页共享样式（与首页同一套设计令牌） ═══ */
:root{
  --bg:#1A1E2A; --bg2:#222837; --surface:#1F2530;
  --card:rgba(255,255,255,.04); --cardSolid:#262C3A;
  --stroke:rgba(255,255,255,.10); --stroke2:rgba(255,255,255,.20);
  --text:#EEF0FF; --text2:rgba(238,240,255,.62); --text3:rgba(238,240,255,.32);
  --brand:#F5B642; --brandDeep:#C68A1E; --amber:#FAC775;
  --coral:#ff7a8c; --mint:#5ad6a0;
  --r-sm:8px; --r-md:14px; --r-lg:20px; --r-xl:28px; --r-full:999px;
  --ease:cubic-bezier(.22,.61,.36,1); --ease-spring:cubic-bezier(.34,1.56,.64,1);
  --t:.45s; --t-fast:.22s;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);line-height:1.65;overflow-x:hidden;
  font-family:"Segoe UI Variable","Segoe UI","PingFang SC","Microsoft YaHei UI",sans-serif;
  -webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
::selection{background:var(--brand);color:#1A1E2A}
.wrap{max-width:1080px;margin:0 auto;padding:0 32px}

/* 顶栏（与首页一致） */
nav.top{position:fixed;top:0;left:0;right:0;z-index:100;padding:16px 0;
  transition:background var(--t) var(--ease),backdrop-filter var(--t),padding var(--t) var(--ease)}
nav.top.scrolled{background:rgba(26,30,42,.78);backdrop-filter:blur(20px) saturate(180%);
  padding:8px 0;border-bottom:1px solid var(--stroke)}
.top-in{max-width:1320px;margin:0 auto;padding:0 32px;display:flex;align-items:center;gap:30px}
.logo img{height:34px;width:auto;display:block;border-radius:8px}
.nav-links{display:flex;gap:24px;font-size:14px;color:var(--text2);align-items:center}
.nav-links a:hover{color:var(--text)}
.nav-right{margin-left:auto;display:flex;gap:12px;align-items:center}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;padding:9px 18px;
  border-radius:var(--r-full);font-size:13.5px;font-weight:600;border:none;cursor:pointer;
  transition:transform var(--t-fast) var(--ease-spring),box-shadow var(--t) var(--ease),background var(--t) var(--ease)}
.btn:active{transform:scale(.96)}
.btn-ghost{background:transparent;color:var(--text);border:1px solid var(--stroke2)}
.btn-ghost:hover{background:rgba(255,255,255,.06)}
.btn-amber{background:linear-gradient(135deg,var(--brand),var(--brandDeep));color:#1A1E2A;
  box-shadow:0 6px 22px rgba(245,182,66,.32);font-weight:700}
.btn-amber:hover{box-shadow:0 10px 32px rgba(245,182,66,.5);transform:translateY(-2px)}

/* Hero */
.fhero{position:relative;overflow:hidden;padding:150px 0 70px;
  border-bottom:1px solid var(--stroke);background:#0E1320}
.fhero-in{position:relative;z-index:3}
.aurora{position:absolute;inset:0;pointer-events:none;opacity:0;transition:opacity .9s var(--ease)}
.aurora.on{opacity:.55}
.aurora::before{content:"";position:absolute;right:-20%;top:-30%;width:70%;height:150%;
  filter:blur(120px) saturate(130%);
  background:conic-gradient(from 0deg,#5ad6a0,#2540ff,#9a8bff,#7c3aed,#5ad6a0);
  animation:spin 26s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.fback{display:inline-block;font-size:13px;color:var(--text2);margin-bottom:26px;
  transition:color var(--t-fast),transform var(--t-fast)}
.fback:hover{color:var(--brand);transform:translateX(-3px)}
.fico{width:58px;height:58px;border-radius:16px;display:grid;place-items:center;
  color:#fff;font-size:25px;font-weight:700;margin-bottom:18px;
  box-shadow:0 12px 30px rgba(0,0,0,.35)}
.fico.sm{width:38px;height:38px;border-radius:11px;font-size:17px;margin:0}
.ico-blue{background:linear-gradient(135deg,#2540ff,#1e6bff)}
.ico-violet{background:linear-gradient(135deg,#7c3aed,#9a8bff)}
.ico-coral{background:linear-gradient(135deg,#ff7a8c,#ff9f6b)}
.ico-mint{background:linear-gradient(135deg,#5ad6a0,#34d399)}
.ico-amber{background:linear-gradient(135deg,#F5B642,#F59E0B);color:#1A1E2A}
.ftag{font-size:12.5px;font-weight:600;letter-spacing:1.4px;text-transform:uppercase;
  color:var(--brand);margin-bottom:12px}
.fhero h1{font-size:clamp(30px,4.4vw,50px);line-height:1.12;letter-spacing:-1.4px;font-weight:700;max-width:820px}
.fsub{font-size:16.5px;color:var(--text2);margin:20px 0 26px;max-width:760px}
.facts{display:flex;flex-wrap:wrap;gap:9px;margin-bottom:32px}
.fchip{padding:7px 15px;border-radius:var(--r-full);background:var(--card);
  border:1px solid var(--stroke);font-size:12.5px;color:var(--text2)}
.fcta-row{display:flex;gap:12px;flex-wrap:wrap}

/* Sections */
.fsec{padding:64px 0 8px}
.fsec h2{font-size:clamp(21px,2.5vw,29px);letter-spacing:-.6px;font-weight:700;margin-bottom:24px}
.fgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
.fcard{background:var(--card);border:1px solid var(--stroke);border-radius:var(--r-md);
  padding:20px 22px;transition:transform var(--t) var(--ease),border-color var(--t),background var(--t)}
.fcard:hover{transform:translateY(-4px);border-color:var(--stroke2);background:rgba(255,255,255,.06)}
.fcard h3{font-size:15px;font-weight:600;margin-bottom:7px}
.fcard p{font-size:13.5px;color:var(--text2)}
.fsteps{list-style:none;display:grid;gap:12px;counter-reset:s}
.fsteps li{display:flex;gap:14px;align-items:flex-start;background:var(--card);
  border:1px solid var(--stroke);border-radius:var(--r-md);padding:15px 18px;font-size:14px}
.fsteps .n{flex:none;width:26px;height:26px;border-radius:50%;display:grid;place-items:center;
  background:linear-gradient(135deg,var(--brand),var(--brandDeep));color:#1A1E2A;
  font-size:12.5px;font-weight:700;margin-top:1px}
.fpoints{list-style:none;display:grid;gap:11px}
.fpoints li{position:relative;padding-left:24px;font-size:14px;color:var(--text2)}
.fpoints li::before{content:"";position:absolute;left:0;top:9px;width:7px;height:7px;
  border-radius:50%;background:var(--mint)}
.fshot{margin:0;border:1px solid var(--stroke2);border-radius:var(--r-lg);overflow:hidden;
  background:#0B1120}
.fshot img{width:100%;display:block}
.fshot figcaption{padding:13px 18px;font-size:13px;color:var(--text3);border-top:1px solid var(--stroke)}

/* 相关功能 */
.frels{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
.frel{display:flex;align-items:center;gap:14px;background:var(--card);border:1px solid var(--stroke);
  border-radius:var(--r-md);padding:15px 18px;transition:transform var(--t) var(--ease),border-color var(--t)}
.frel:hover{transform:translateX(5px);border-color:var(--brand)}
.frel b{display:block;font-size:14px;font-weight:600}
.frel em{font-style:normal;font-size:11.5px;color:var(--text3);letter-spacing:.6px;text-transform:uppercase}
.frel i{margin-left:auto;color:var(--brand);font-style:normal;font-weight:700}

/* 收尾 CTA */
.fend{padding:70px 0 90px}
.fend-in{background:linear-gradient(135deg,rgba(245,182,66,.14),rgba(198,138,30,.10));
  border:1px solid var(--stroke2);border-radius:var(--r-xl);padding:48px 32px;text-align:center}
.fend-in h2{font-size:clamp(21px,2.6vw,32px);margin-bottom:12px}
.fend-in p{color:var(--text2);margin-bottom:24px;font-size:15px}

footer{border-top:1px solid var(--stroke);padding:38px 0;font-size:13px;color:var(--text3);margin-top:20px}
.foot{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;align-items:center}
.foot-links{display:flex;gap:20px}
.foot-links a:hover{color:var(--brand)}

.reveal{opacity:0;transform:translateY(22px);transition:opacity .7s var(--ease),transform .7s var(--ease)}
.reveal.in{opacity:1;transform:none}

/* 首页「全部功能」网格（注入 index-v3.html 用） */
.feature-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.fcard-link{position:relative;display:flex;flex-direction:column}
.fcard-link .go{margin-top:auto;padding-top:14px;font-size:12.5px;font-weight:600;color:var(--brand);
  opacity:0;transform:translateX(-6px);transition:opacity var(--t) var(--ease),transform var(--t) var(--ease)}
.fcard-link:hover .go{opacity:1;transform:none}
@media (max-width:960px){
  .nav-links{display:none}
  .fgrid,.frels{grid-template-columns:1fr}
  .feature-grid{grid-template-columns:repeat(2,1fr)}
}
@media (max-width:560px){ .feature-grid{grid-template-columns:1fr} }
@media (prefers-reduced-motion:reduce){
  *{animation-duration:.01ms!important;transition-duration:.01ms!important}
  .reveal{opacity:1;transform:none}
}
"""

if __name__ == "__main__":
    main()
