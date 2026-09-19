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
        "sub": "78 个内置模型 + 14 个国内直连平台，统一在一个对话框里。主通道与兜底通道双活互备，一条通道抽风自动换另一条接着跑；断网还有本地 Ollama 顶上。",
        "facts": ["78 个内置模型", "OpenRouter + 14 个国内直连通道", "双通道互备自动顶替", "地区受限模型自动跳过"],
        "what": [
            ("一个输入框，连通所有模型", "不用记 API、不用开一堆网页。DeepSeek、Qwen、GLM、Kimi、MiniMax、豆包、混元、文心、Grok，以及 OpenRouter 上的全量模型，都在同一个下拉框里；本地 Ollama 装的模型也在一起。"),
            ("主通道 + 兜底通道，双活互备", "OpenRouter 作主力通道，七牛云或你自填的国内平台作兜底。某条通道限频、5xx、没配 Key、甚至整个挂掉，系统自动把请求交给另一条通道的同类模型继续跑——对话不中断，只会看到「已自动切换」。"),
            ("地区受限模型自动识别与跳过", "部分地区账单地址拿不到 OpenAI / Anthropic / Google 的闭源模型。客户端启动时用最小请求实测一次（花费≈$0）并把结果落盘，受限模型在下拉框标「🚫 地区受限」，自动选模也会绕开它们，不再把时间浪费在必然失败的调用上。"),
            ("14 个国内直连平台，预设一键切换", "硅基流动、阿里云百炼、DeepSeek 官方、火山方舟、智谱、Kimi、MiniMax、腾讯混元、魔搭、302.AI、DMXAPI、AIHubMix、NVIDIA NIM、阶跃星辰。选中即自动带出 Base URL，粘上 Key 就能用，不用翻文档抄地址。"),
            ("本地优先，断网也能跑", "接上 Ollama 即可完全离线：对话、文件操作、工作流编排都不依赖网络，数据不出本机。"),
            ("五档会员 × 多类用途矩阵", "免费 / 标准 / 专业 / 旗舰 / 极限五档，各档解锁不同模型池；模型按通用 / 推理 / 代码 / 视觉 / 音乐分类，系统按任务类型自动挑，也能手动锁定任意一个。"),
            ("模型状态一目了然", "下拉框里每个模型都带状态标记：「🔒 需 OpenRouter Key」说明缺哪把钥匙，「🚫 地区受限」说明这个地区用不了。可用的排最前，需要补 Key 的沉底，不用一个个点开试。"),
            ("同一会话实时切换", "聊到一半换模型，上下文不丢——真正意义上的「随手换脑子」。"),
        ],
        "steps": [
            "设置 → 云端模型，把要用的通道 Key 填上（OpenRouter、硅基流动、DeepSeek 官方等，填几家就有几家可用）。",
            "需要离线就把本地 Ollama 打开，客户端会自动发现本地模型。",
            "在顶部模型下拉里选具体模型，或直接用「自动路由」让它自己挑——缺 Key、地区受限的模型会被自动跳过。",
            "模型带「· 兜底」标记的，会在主通道失败时自动接手，无需手动干预。",
            "断网时自动落到本地模型，联网后自动恢复云端。",
        ],
        "tech": [
            "统一 cloud_client 抽象层：本地 / 云端 / 各家国内平台共用同一套调用签名，接一个新平台只需一条 base_url + Key。",
            "双通道路由：同名模型 id 在两条通道都存在时（DeepSeek V4 Pro、GLM 5.3、Kimi K3 这类），按「哪条通道配了 Key」+ 通道优先级动态选边。",
            "Key 不跨通道借用：七牛云的 Key 绝不会被打到 OpenRouter 上——这条修复消掉了一类「报 401 说 Key 过期、其实根本没配」的假故障。",
            "429 区分「限频」与「余额不足」：限频读 Retry-After 退避重试，余额不足立即停并提示充值；403 判定地区封锁后直接切兜底模型。",
            "启动时后台拉取 OpenRouter 公开目录（400+ 模型），实时刷新价格与上下文窗口；目录拉取本身不需要 Key。",
            "模型元数据自带上下文窗口 / 单价 / 起解锁档位，自动选模在「类别匹配 + 档位达标」基础上按价格打分，同价位优先便宜的。",
        ],
        "shot": "assets/shots/home.png", "shot_cap": "同一个输入框，连通本地与云端",
        "related": ["routing", "channels"],
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
            ("专家各带模型组", "每位专家绑定「推理 / 通用 / 代码」三模型组，并在图像 / 视频 / 音乐维度上绑定对应生成模型；换通道、换档位时模型组自动重算，专家不会因为模型不可用而「假死」。"),
            ("专攻 Agent 阵列（极限档）", "深度研究、自主编程、自搜自造建模、短剧分镜、音乐创作五个方向各配专属模型与专属工作流——研究用百万上下文推理模型，编程用代码专精模型，建模用推理顶配模型。"),
            ("地区不可用自动换装", "绑定的旗舰模型如果在你所在地区不可用，系统自动换到同档位的可用模型顶上，并把这件事记在日志里，而不是报错停下。"),
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
        "sub": "它不是每次都从零开始。关键事实、历史会话、跑通过的流程、你的偏好与沟通风格，分别沉淀在四层记忆里，越用越懂你；聊得太长时还会自动滚动压缩，早期轮次折叠成摘要，省 token 又不丢上下文。",
        "facts": ["4 层记忆结构", "中文 n-gram 检索", "滚动压缩 4 倍+", "本地 SQLite 存储"],
        "what": [
            ("L1 常驻记忆", "最重要的事实与偏好，每轮对话都注入。因为有容量上限，系统被强迫只留最有价值的那几条。"),
            ("L2 会话归档", "全部历史会话存进本地数据库，按关键词命中数召回最相关的几段，需要时才注入，不占用常驻预算。"),
            ("L3 技能库", "跑通过的流程会被自动抽成可复用技能——同样的活第二次只要一句话。"),
            ("L4 用户画像", "沟通风格、领域知识、做事习惯长期积累，让回复越来越像在跟你说话。"),
            ("滚动上下文压缩", "保留最近若干轮原文保证连贯，更早的轮次折叠成增量摘要。实测 5975 token 的对话压到 1401 token（4.3 倍），该记的事一件没少。"),
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
            "滚动压缩保最近 K 轮原文 + 更早轮次增量摘要，按模型上下文窗口余量动态回收最旧内容。",
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
    {
        "slug": "engineering", "title": "工程绘图",
        "tag": "Engineering Drawing", "icon": "📐", "ico": "ico-blue",
        "sub": "左侧聊天描述需求，AI 生成可运行的绘图代码，右侧实时出图预览；一键导出 Origin LabTalk 脚本，装了 Origin 直接跑，满足期刊出图规范。",
        "facts": ["聊天即绘图", "Origin 脚本一键导出", "本地执行 0 上传", "专业工程图表"],
        "what": [
            ("聊天式绘图", "在对话框里描述你要的图——剪力图、弯矩图、伯德图、误差棒——AI 生成代码并立刻渲染到右侧预览区。"),
            ("代码全透明", "每次生成都是可读的 Python 代码，参数、单位、公式都在明面上，可以改完再跑。"),
            ("本地渲染，数据不出本机", "绘图代码在你的电脑上执行（numpy / matplotlib / scipy），原始数据不需要上传到任何云端。"),
            ("一键导出 Origin 脚本", "预览满意后一键把方案转成 Origin LabTalk 脚本（.ogs），在正版 Origin 里打开即用。"),
            ("多种图表类型", "折线、柱状、散点、误差棒、双 y 轴、极坐标、3D 曲面……工程里常用的图都覆盖。"),
            ("上下文连续修改", "「把线改成红色」「y 轴取对数」——接着说就行，它记得上一轮画了什么。"),
        ],
        "steps": [
            "侧栏点「📐 工程绘图」打开绘图面板。",
            "左侧输入需求，例如「画悬臂梁在均布载荷下的剪力图与弯矩图」。",
            "AI 生成代码并本地执行，右侧预览区立刻显示图像。",
            "满意后选择「导出脚本 → Origin」，保存 .ogs 文件到本机。",
        ],
        "tech": [
            "云端代码模型生成绘图代码，按档位自动选模型（OpenRouter / 国内直连通道自动路由），省钱优先。",
            "本地沙箱执行：只预置 numpy / matplotlib / scipy，异常全捕获，报错直接显示在聊天区。",
            "Agg 后端离屏渲染，不弹窗、不抢焦点，出图即存本地。",
            "导出走第二次模型调用，把 Python 方案无损转成 LabTalk / MATLAB / COMSOL 代码。",
        ],
        "shot": "assets/shots/home.png", "shot_cap": "聊天出图，右侧实时预览",
        "related": ["models", "files"],
    },
    {
        "slug": "modeling", "title": "建模手",
        "tag": "Modeling Assistant", "icon": "🧮", "ico": "ico-violet",
        "sub": "数学建模竞赛水平的助手：建模假设 → 建立方程 → 代码求解 → 结果图，一条龙。可导出 MATLAB 脚本，给导师或队友一键复现。",
        "facts": ["假设→建模→求解→出图", "scipy 数值求解", "MATLAB 脚本导出", "国赛风格输出"],
        "what": [
            ("完整建模流程", "先给不超过 5 行的建模假设与思路，再给可运行的求解代码，最后用图展示结果并简短解读——就是竞赛论文的骨架。"),
            ("方程 / 拟合 / 优化全覆盖", "微分方程（solve_ivp）、最小二乘拟合、线性规划、蒙特卡洛模拟等常用建模方法都支持。"),
            ("结果立刻可视化", "求解完自动绘图：收敛曲线、相图、参数敏感性……直观检查模型行为。"),
            ("一键导出 MATLAB 脚本", "方案定稿后导出 .m 脚本，方便在 MATLAB 里复现，或交给需要 MATLAB 的课程与队友。"),
            ("参考历史不跑偏", "多轮对话保留上下文，改约束、换目标函数，接着说就行。"),
            ("参数单位写清楚", "生成的代码里参数带物理量纲注释，避免「0.5 到底是啥」的尴尬。"),
        ],
        "steps": [
            "侧栏点「🧮 建模手」。",
            "描述问题，例如「用逻辑斯蒂模型预测种群增长并做参数拟合」。",
            "阅读思路说明，等右侧出结果图；不满意就继续追问修改。",
            "导出脚本 → MATLAB，保存 .m 文件复现。",
        ],
        "tech": [
            "本地执行环境含 numpy / scipy / matplotlib 全家桶，数值能力完整。",
            "solve_ivp、least_squares 等直接可用，无需自实现求解器。",
            "多模型降级链复用主程序同一套调度，限频自动切换。",
            "代码执行异常全捕获回传，模型写错不会崩掉 App。",
        ],
        "shot": "assets/shots/home.png", "shot_cap": "建模假设 → 求解 → 结果图",
        "related": ["experts", "engineering"],
    },
    {
        "slug": "simulation", "title": "物理仿真",
        "tag": "Physics Simulation", "icon": "⚛", "ico": "ico-mint",
        "sub": "描述物理过程，AI 建立数值模型并仿真：单摆、振动、传热、波动、电路……结果曲线当场看，还能导出 COMSOL 建模脚本继续细化。",
        "facts": ["ODE/PDE 数值仿真", "结果实时预览", "COMSOL 脚本导出", "物理量与单位标注"],
        "what": [
            ("从描述到数值模型", "说出物理场景（单摆大角度摆动、悬臂梁振动、一维传热），AI 自动列方程、离散化、数值求解。"),
            ("曲线 / 场图即时预览", "物理量随时间或空间的变化当场画出来，角度-时间、温度场、波形图直观可见。"),
            ("物理量与单位齐全", "坐标轴标注物理量与单位，参数表带量纲，结果可直接放进报告。"),
            ("一键导出 COMSOL 脚本", "需要精细有限元时，把方案导出为 COMSOL Java API 脚本（.java），在 COMSOL 里继续建模细化。"),
            ("变参数对比实验", "「阻尼增大 3 倍再跑一次」——同一模型改参数重跑，对比曲线一目了然。"),
            ("本地计算零上传", "仿真在你的电脑上跑，模型与数据不出本机。"),
        ],
        "steps": [
            "侧栏点「⚛ 物理仿真」。",
            "描述物理过程与想要的输出，例如「单摆大角度摆动，画角度-时间曲线」。",
            "等右侧预览出图，继续追问改参数或换工况。",
            "导出脚本 → COMSOL，保存 .java 建模代码。",
        ],
        "tech": [
            "ODE 用 scipy solve_ivp（RK45），简单场景自动退化为 numpy 自实现欧拉 / RK4。",
            "离屏 Agg 渲染，仿真结果 PNG 落本地，随看随取。",
            "系统提示词强制约束输出格式与库白名单，生成代码可执行率优先。",
            "导出 COMSOL 走模型二次转换：几何 → 物理场 → 网格 → 求解 → 后处理五步齐全。",
        ],
        "shot": "assets/shots/home.png", "shot_cap": "数值仿真，当场看曲线",
        "related": ["engineering", "models"],
    },
    {
        "slug": "routing", "title": "智能路由与成本控制",
        "tag": "Smart Routing & Cost Control", "icon": "⇄", "ico": "ico-amber",
        "sub": "大模型按 token 计费，而最烧钱的往往不是你问的那句话，是每一轮都在重复发送的长上下文。三道防线——粘性选模、前缀缓存、滚动压缩——把账单压到最低。",
        "facts": ["三道省 token 防线", "上下文压缩 4 倍+", "前缀缓存输入按 1/10 计费", "用量与花费可追溯"],
        "what": [
            ("第一道：粘性选模，不来回换", "每次切换模型，服务商侧缓存的前缀就作废，整段上下文要重新按原价计费一遍。所以自动选模是「粘」的——同一类任务保持同一个模型，只在上下文将要超出窗口时才升级，避免为了省小钱反而多花大钱。"),
            ("第二道：提示前缀缓存", "系统提示词、专家人设、工具说明这些每轮都要重发的内容，被打上缓存标记。命中缓存后，这部分输入按约 1/10 的价格计费；聊得越久、前缀越长，省得越多。"),
            ("第三道：滚动上下文压缩", "保留最近若干轮原文（保证对话连贯），更早的内容折叠成增量摘要。实测一段 5975 token 的对话压到 1401 token，压缩比 4.3 倍，语义不丢。"),
            ("按任务类型挑模型", "写代码交给代码模型，图像理解交给视觉模型，长文推理交给大窗口推理模型。自动选模按「类别匹配 + 档位达标 + 价格」三项打分，同价位优先便宜的。"),
            ("限频退避，不硬撞", "撞上速率限制时读 Retry-After 做两段式退避（8 秒 → 30 秒等窗口滚动），而不是无脑重试；连续失败才降级换模型，避免把配额烧在重试上。"),
            ("失败自动换通道", "通道 5xx、超时、余额不足、地区封锁，各有不同的处理策略：能换模型就换，换不了就明确告诉你原因（而不是静默失败或重复扣费）。"),
            ("花费透明", "每次调用记录模型、输入输出 token 与预估花费；配合上游账单可以核对「钱花在哪了」，不会出现「不知道怎么就没了」。"),
        ],
        "steps": [
            "默认什么都不用设：自动路由会自动做粘性与压缩。",
            "想省钱就选低档模型跑日常任务，把旗舰模型留给建模、深度研究这类硬活。",
            "长对话不必手动清理历史——滚动压缩会自动折叠早期轮次。",
            "在设置里查看当前档位与模型池，确认自动选模用的是你想要的那一档。",
        ],
        "tech": [
            "滚动上下文采用「保最近 K 轮原文 + 更早轮次增量摘要」结构，摘要不调 LLM，用轮次拼接，额外成本为 0。",
            "预算裁剪按窗口余量动态回收最旧内容，保证请求永不超出模型上下文窗口。",
            "提示缓存对 OpenRouter / Claude 系在 system 前缀挂 cache_control，其余网关忽略该字段、无副作用。",
            "粘性决策只比较「当前模型是否还能装下上下文」，能装就不动——切模型带来的 KV 缓存失效成本远大于单价差异。",
            "token 估算用字符数与中英文差分（中文约 1.5 字符/token，英文约 4 字符/token），不额外调用 tokenizer 接口。",
        ],
        "shot": "assets/shots/home.png", "shot_cap": "同样的活，账单更低",
        "related": ["models", "membership"],
    },
    {
        "slug": "channels", "title": "模型通道与地区自适应",
        "tag": "Providers & Region", "icon": "◎", "ico": "ico-blue",
        "sub": "国内直连、不锁地区、一个 Key 打多家。14 个平台预设 + 双通道互备 + 地区体检，让「模型用不了」这件事不再需要你排查。",
        "facts": ["14 个国内直连平台预设", "双通道互备", "地区受限自动识别", "Key 绝不跨通道串用"],
        "what": [
            ("为什么需要多通道", "海外聚合平台会把部分厂商的闭源模型按「账单地区」封锁——同一平台上有的模型能用、有的直接 403。国内官方平台与合规聚合平台不存在这个问题，但一家只覆盖自家模型。两边互补，才是最稳的方案。"),
            ("14 个国内直连预设", "硅基流动、阿里云百炼、DeepSeek 官方、火山方舟、智谱 BigModel、月之暗面 Kimi、MiniMax、腾讯混元、魔搭 ModelScope、302.AI、DMXAPI、AIHubMix、NVIDIA NIM、阶跃星辰。全部 OpenAI 协议兼容，选平台即自动填 Base URL。"),
            ("主力 + 兜底，双活互备", "OpenRouter 作主通道时自动带上国内 Key 作兜底，反之亦然。一条通道抽风，另一条同类模型顶上，对话不中断。"),
            ("地区体检（自动，免费）", "启动时对目录里的模型逐个发一条最小请求（max_tokens=1，花费≈$0），实测哪些被地区封锁，结果落盘复用。换 Key 自动重测，同一把 Key 只测一次。"),
            ("受限模型明确标注", "被封的模型在下拉框标「🚫 地区受限」并沉底；自动选模直接跳过它们。你永远不会「选了才发现跑不通」。"),
            ("缺 Key 的模型也会说话", "没配某个平台 Key 时，属于该平台的模型标「🔒 需 X Key」——它告诉你去哪补哪把钥匙，而不是含糊地报一句鉴权失败。"),
            ("换平台不用改代码", "所有通道共用一套调用协议与同一套模型索引，切换平台只改一个下拉框选项，工作流、专家、技能全部照常工作。"),
        ],
        "steps": [
            "设置 → 云端模型，provider 下拉里挑一个平台（例如「硅基流动」）。",
            "弹窗会自动带出该平台的 Base URL，粘上你的 Key；模型名可填该平台的任意模型 id。",
            "验证并保存，重启后该平台的模型即可在顶部下拉里选择。",
            "想双通道互备，就把两个平台的 Key 都填上，系统会自动组主力 + 兜底。",
        ],
        "tech": [
            "通道能力表统一维护：每个平台一条记录（label / base_url / 注册地址 / 常见模型示例），新增平台不超过 10 行代码。",
            "地区体检结果与 Key 指纹绑定存储，避免每次启动都花 3 分钟重测；换 Key 立即失效重测。",
            "逐模型粒度判定（不是按厂商一刀切）：同一厂商里开源权重模型往往不受限，实测能过就放行。",
            "请求头按通道自适应：部分平台用 api-key 头而非 Bearer，客户端自动切换，用户无感。",
            "所有通道共用 429 / 5xx / 403 的统一错误分类与降级策略，行为一致可预期。",
        ],
        "shot": "assets/shots/home.png", "shot_cap": "通道状态一眼可见",
        "related": ["models", "routing"],
    },
    {
        "slug": "cad3d", "title": "3D 建模与 CAD 出图",
        "tag": "3D & CAD Modeling", "icon": "◫", "ico": "ico-violet",
        "sub": "说一句话就能出 3D 模型：概念级用 Blender 快速示意，工程级走真 CAD 内核生成 B-rep 实体，导出 STEP / DXF / OBJ 直接进工业流程。要什么参数，它自己去网上查、交叉验证后再建。",
        "facts": ["自搜参数 + 多源交叉验证", "概念级 / 工程级双内核", "B-rep 实体 · STEP / DXF 导出", "一个按钮管全部"],
        "what": [
            ("不硬喂参数，自己去查", "你说「建一个 Boeing 737-800 的机身」，它会自己去联网检索真实尺寸——而且不是抓一个网页就用：同一参数发多条不同表述的查询（中英文都发），聚合多个独立来源，取中位数作为共识值，并标注置信度（高 / 中 / 低 / 冲突）。"),
            ("多源交叉验证有据可查", "每个关键尺寸都能看到来源与校验结果：几源支持、值是多少、是否相互矛盾。检索报告落盘保存，交付时可以和模型一起给出去。"),
            ("概念级：Blender / bpy 快速示意", "生成 bpy 脚本、无头运行、导出 STL 并渲染预览图。所有档位可用，适合「先看看大概长啥样」。"),
            ("工程级：真 CAD 内核（B-rep）", "走 CAD 内核生成真正的 B-rep 实体——支持倒角、圆角、布尔运算、孔位特征，导出 STEP（通用 CAD 交换格式）与 DXF（二维工程图）。旗舰 / 极限档解锁。"),
            ("建模精度：一个按钮切换", "面板上的「3D 建模」按钮点开就是全部入口：立即建模、精度选择（自动 / 概念级 / 工程级）、FreeCAD 弧面建模、导入模型、内核路径。自动档会随档位与内核安装状态平滑升级，不用你操心。"),
            ("接着现成模型干活", "导入 STL / OBJ / GLB 直接进入后续流程（仿真、工程图、产品渲染），不用从零开始建。"),
            ("内核缺失会引导安装", "选工程级但没装内核时，它会问你要不要自动装（走国内镜像、装到独立目录，不污染你现有 Python 环境），装完自动落到工程级。"),
            ("提示词约束到位", "系统提示词强制「关键尺寸先定义为变量、基于变量算部件位置、禁止散落魔法数字」，并打印体积与表面积自检，减少「看着像但尺寸不对」。"),
        ],
        "steps": [
            "打开工程模式 → 建模，在输入框描述零件或对象（越具体越好，例如「60×40×8 板，四角 R5 圆角，中心 φ10 通孔」）。",
            "点「3D 建模」按钮 → 选建模精度：日常用「自动」，要工业交付就选「工程级」。",
            "等它检索参数（会显示交叉验证报告）→ 生成脚本 → 无头执行 → 右侧出预览图与实体文件。",
            "满意后导出 STEP / DXF / STL；要接着仿真就点「导入模型」把这套几何喂给仿真面板。",
        ],
        "tech": [
            "双内核调度：概念级走 bpy（无头 Blender），工程级走 CadQuery / OpenCASCADE（真 B-rep），按精度与档位自动分流。",
            "多源检索聚合：2~3 条不同表述的查询（中/英）→ 独立来源提取规格 → 中位数稳健共识 → 相对容差 8% 判一致，单源标低置信度、多源分歧标冲突。",
            "内核探测：自动发现便携版 Blender / FreeCAD，找不到时提示指定路径；内核安装走国内镜像、装进独立 site 目录。",
            "脚本执行全程子进程隔离 + 超时保护，模型写错不会卡死客户端，报错原文回传聊天区。",
            "导出格式按用途分流：STEP（CAD 交换）/ DXF（工程图）/ STL、OBJ（3D 打印与网格仿真）。",
        ],
        "shot": "assets/shots/home.png", "shot_cap": "一句话 → 真 B-rep 实体",
        "related": ["engineering", "simulation"],
    },
    {
        "slug": "membership", "title": "会员档位与用量",
        "tag": "Plans & Usage", "icon": "◆", "ico": "ico-mint",
        "sub": "五档会员对应不同的模型池与能力边界：免费档跑本地、标准档覆盖性价比阵容、旗舰档开工程级 CAD，极限档不设上限、按量实扣。新用户赠送 5 美元初始信用额度。",
        "facts": ["5 档会员", "新用户赠 $5 额度", "极限档不设上限", "专攻 Agent 仅极限档"],
        "what": [
            ("免费档：本地优先，零成本", "接 Ollama 跑本地模型，对话、文件操作、工作流、技能全部可用；也可以挂 OpenRouter 上的免费模型改善体验。数据不出本机。"),
            ("标准档：性价比阵容", "DeepSeek V4 Flash、Qwen3.8 Flash、GLM 4.6、豆包 Seed Lite 这类「够快够省」的主力模型，配识图能力，覆盖绝大多数日常任务。"),
            ("专业档：旗舰国产阵容", "解锁 DeepSeek V4 Pro、GLM 5.3、Kimi K3、Qwen3.8 Max 等旗舰，长文推理、复杂代码、视觉大模型都在内。"),
            ("旗舰档：工程级能力", "在专业档基础上解锁工程级 CAD 建模（真 B-rep + STEP/DXF 导出）、更大的上下文与更高的调用上限。"),
            ("极限档：不设上限", "不限云端消息条数，按量实扣（绑卡自动扣费或随时充值），专攻 Agent——深度研究、自主编程、自搜自造建模、短剧分镜——仅此档开放。新用户赠 $5 初始信用额度。"),
            ("档位随时切换", "设置里换档即刻生效，模型池、能力门禁（CAD、专攻 Agent）、可选模型数量同步刷新，不用重装、不用重新登录。"),
            ("额度看得见", "当前档位、模型数量、剩余信用额度与本次会话消耗都在设置里可查；额度耗尽会明确提示，不会静默降级。"),
        ],
        "steps": [
            "设置 → 会员与额度，查看五档差异与当前档位。",
            "选一个档位并保存；有激活码就填激活码，有信用卡额度就用信用额度。",
            "模型下拉框会立刻按新档位刷新可用模型清单。",
            "想退回免费模式随时切换，聊天记录与本地数据不受影响。",
        ],
        "tech": [
            "档位为单一事实源（single source of truth）：档位 → 模型池 → 能力门禁 → UI 文案全部由同一份配置推导，避免「改了档位但界面没变」这类状态不一致。",
            "能力门禁分两级：模型按 min_tier 解锁；工程级 CAD 与专攻 Agent 按档位单独判定。",
            "额度校验在客户端与服务端双端进行，客户端先拦、服务端为准。",
            "档位变更触发模型池重算与下拉框重绘，无需重启应用。",
        ],
        "shot": "assets/shots/home.png", "shot_cap": "五档能力边界清清楚楚",
        "related": ["models", "routing"],
    },
]

BY_SLUG = {f["slug"]: f for f in FEATURES}

NAV = """<nav class="top" id="topnav">
  <div class="top-in">
    <a href="index.html" class="logo"><img src="images/favicon.png" alt="Working Mate"></a>
    <div class="nav-links">
      <a href="index.html#features" data-i18n="feat.nav.features">功能</a>
      <a href="index.html#workflow" data-i18n="feat.nav.workflow">工作流</a>
      <a href="index.html#models" data-i18n="feat.nav.models">模型</a>
      <a href="pricing.html" data-i18n="feat.nav.pricing">价格</a>
    </div>
    <div class="nav-right">
      <a href="index.html#pricing" class="btn btn-amber" data-i18n="feat.nav.download">免费下载</a>
    </div>
  </div>
</nav>"""

FOOT = """<footer>
  <div class="wrap foot">
    <div data-i18n="feat.foot.copy">© 2026 Working Mate · 本地优先的 AI 工作间</div>
    <div class="foot-links">
      <a href="index.html#features" data-i18n="feat.foot.features">功能</a>
      <a href="privacy.html" data-i18n="feat.foot.privacy">隐私</a><a href="terms.html" data-i18n="feat.foot.terms">条款</a><a href="refunds.html" data-i18n="feat.foot.refunds">退款</a>
    </div>
  </div>
</footer>"""


def _li(items, slug, cls="fcard"):
    return "".join(
        f'<div class="{cls}"><h3 data-i18n="feat.{slug}.what{i}t">{t}</h3>'
        f'<p data-i18n="feat.{slug}.what{i}d">{d}</p></div>'
        for i, (t, d) in enumerate(items)
    )


def _steps(items, slug):
    return "".join(
        f'<li><span class="n">{i+1}</span><div data-i18n="feat.{slug}.step{i}">{s}</div></li>'
        for i, s in enumerate(items)
    )


def _facts(items, slug):
    return "".join(
        f'<span class="fchip" data-i18n="feat.{slug}.fact{i}">{x}</span>'
        for i, x in enumerate(items)
    )


def _tech(items, slug):
    return "".join(
        f'<li data-i18n="feat.{slug}.tech{i}">{x}</li>' for i, x in enumerate(items)
    )


def _shot(f, slug):
    if not f.get("shot"):
        return ""
    return f"""
  <section class="fsec reveal">
    <h2 data-i18n="feat.tpl.shot">看一眼</h2>
    <figure class="fshot">
      <img src="{f['shot']}" alt="{f['title']} 界面截图" loading="lazy">
      <figcaption data-i18n="feat.{slug}.shot">{f.get('shot_cap','')}</figcaption>
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
            f'<span><b data-i18n="feat.{r["slug"]}.title">{r["title"]}</b>'
            f'<em data-i18n="feat.{r["slug"]}.tag">{r["tag"]}</em></span><i>→</i></a>'
        )
    if not cards:
        return ""
    return f"""
  <section class="fsec reveal">
    <h2 data-i18n="feat.tpl.related">相关功能</h2>
    <div class="frels">{''.join(cards)}</div>
  </section>"""


def render(f):
    slug = f["slug"]
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{f['title']} · {SITE} 功能</title>
<meta name="description" content="{f['sub'][:110]}">
<link rel="stylesheet" href="feature.css">
<link rel="stylesheet" href="lang.css">
</head>
<body>
{NAV}

<header class="fhero">
  <div class="aurora aurora-1 on"></div>
  <div class="wrap fhero-in">
    <a class="fback" href="index.html#features">← <span data-i18n="feat.tpl.back">返回功能全景</span></a>
    <div class="fico {f['ico']}">{f['icon']}</div>
    <div class="ftag" data-i18n="feat.{slug}.tag">{f['tag']}</div>
    <h1 data-i18n="feat.{slug}.title">{f['title']}</h1>
    <p class="fsub" data-i18n="feat.{slug}.sub">{f['sub']}</p>
    <div class="facts">{_facts(f['facts'], slug)}</div>
    <div class="fcta-row">
      <a href="index.html#pricing" class="btn btn-amber" data-i18n="feat.tpl.heroCta1">免费下载体验</a>
      <a href="index.html#features" class="btn btn-ghost" data-i18n="feat.tpl.heroCta2">看其它功能</a>
    </div>
  </div>
</header>

<main class="wrap">
  <section class="fsec reveal">
    <h2 data-i18n="feat.tpl.what">它能做什么</h2>
    <div class="fgrid">{_li(f['what'], slug)}</div>
  </section>

  <section class="fsec reveal">
    <h2 data-i18n="feat.tpl.how">怎么用</h2>
    <ol class="fsteps">{_steps(f['steps'], slug)}</ol>
  </section>

  <section class="fsec reveal">
    <h2 data-i18n="feat.tpl.tech">技术亮点</h2>
    <ul class="fpoints">{_tech(f['tech'], slug)}</ul>
  </section>
{_shot(f, slug)}
{_related(f)}

  <section class="fsec fend reveal">
    <div class="fend-in">
      <h2 data-i18n="feat.tpl.end">现在就试试</h2>
      <p data-i18n="feat.tpl.endP">免费版永久可用，本地能力开箱即用，不需要信用卡。</p>
      <a href="index.html#pricing" class="btn btn-amber" data-i18n="feat.tpl.endBtn">免费下载 {SITE}</a>
    </div>
  </section>
</main>

{FOOT}
<div id="langmount"></div>
<script>
const n=document.getElementById('topnav');
addEventListener('scroll',()=>n.classList.toggle('scrolled',scrollY>40),{{passive:true}});
const io=new IntersectionObserver(es=>{{es.forEach(e=>{{if(e.isIntersecting){{e.target.classList.add('in');io.unobserve(e.target)}}}})}},{{threshold:.12,rootMargin:'0px 0px -8% 0px'}});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
</script>
<script src="lang.en.js"></script>
<script src="lang.ja.js"></script>
<script src="lang.ko.js"></script>
<script src="lang.fr.js"></script>
<script src="lang.de.js"></script>
<script src="lang.ru.js"></script>
<script src="lang.ar.js"></script>
<script src="lang.es.js"></script>
<script src="lang.pt.js"></script>
<script src="i18n.js"></script>
</body>
</html>
"""


def grid_html():
    cards = []
    for f in FEATURES:
        slug = f["slug"]
        cards.append(
            f'<a class="b-card fcard-link reveal" href="feature-{slug}.html">'
            f'<div class="ico {f["ico"]}">{f["icon"]}</div>'
            f'<h3 data-i18n="feat.{slug}.title">{f["title"]}</h3>'
            f'<p data-i18n="feat.{slug}.grid">{f["facts"][0]} · {f["facts"][1]}</p>'
            f'<span class="go" data-i18n="feat.tpl.view">查看详情 →</span></a>'
        )
    return (
        '<section class="zone" id="features">\n'
        '  <div class="wrap">\n'
        '    <div class="zone-head reveal" style="margin:0 auto 40px;text-align:center;max-width:660px">\n'
        '      <div class="zone-tag" data-i18n="home.feat.tag">All Features</div>\n'
        '      <h2 data-i18n="home.feat.h2">全部功能，点开看细节</h2>\n'
        '      <p data-i18n="home.feat.p" style="color:var(--text2);margin-top:12px">每张卡片都能点进去看完整介绍：能做什么、怎么用、技术亮点。</p>\n'
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

    idx = HERE / "index.html"
    if idx.exists():
        html = idx.read_text(encoding="utf-8")
        if GRID_MARK in html:
            html = html.replace(GRID_MARK, grid_html())
            idx.write_text(html, encoding="utf-8")
            print("[ok] 首页卡片网格已注入")
        else:
            # 标记已被上次注入消费：原位替换已有的功能网格区块
            import re as _re
            pat = _re.compile(
                r'<section class="zone" id="features">.*?</section>', _re.S)
            if pat.search(html):
                html = pat.sub(grid_html(), html, count=1)
                idx.write_text(html, encoding="utf-8")
                print("[ok] 首页卡片网格已原位更新")
            else:
                print("[warn] 未找到网格标记或已有网格区块，首页未改动")
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
