/* ════════════════════════════════════════════════════════════
   Working Mate — 访客地区自动识别（2026-09-26）
   规则（老板需求）：
     · 中国大陆访客 → 人民币（¥）+ 中文文案
     · 海外访客     → 美元（$）+ 英文（其余语言交给 i18n.js 按浏览器语言走）
   实现：
     1) 先用 localStorage 缓存（24h）——避免每次访问都打 IP 接口；
     2) 无缓存时先用浏览器语言启发式（zh* 视为中国）立刻渲染，
        再异步请求 IP 归属纠正（ipwho.is → ipapi.co 两级兜底，2.5s 超时）；
     3) 币种只认 IP 结果；语言：仅当「用户没手动选过语言」时，
        中国大陆才强制中文（尊重手动选择 wm_lang，绝不覆盖）；
     4) 价格兑换用业务定价表（非实时汇率）：$4→¥28  $14→¥100  $42→¥300。
   用法：
     在 i18n.js 之前引入本文件：<script src="region.js"></script>
     价格块标记美元价：<div class="price" data-usd="14">…</div>
   ════════════════════════════════════════════════════════════ */
(function () {
  "use strict";

  var REGION_KEY = "wm_region";      // 缓存: "CN" | "OVERSEAS"
  var REGION_TS  = "wm_region_ts";   // 缓存时间戳
  var TTL = 60 * 60 * 1000;          // 1 小时（仅用于首屏，实际每次访问都会后台复检）

  // ── 美元 → 人民币 业务定价表（改价格只改这里 + HTML data-usd）──
  var USD2CNY = { "0": 0, "2": 12, "3": 22, "4": 28, "7": 50, "14": 100, "42": 300 };
  var CNY_FALLBACK_RATE = 7.2;       // 表里没有的价格按此汇率取整

  function savedLang() {
    try { return localStorage.getItem("wm_lang"); } catch (e) { return null; }
  }
  function getCache() {
    try {
      var r = localStorage.getItem(REGION_KEY);
      var ts = parseInt(localStorage.getItem(REGION_TS) || "0", 10);
      if (r && (Date.now() - ts) < TTL) return r;
    } catch (e) {}
    return null;
  }
  function putCache(region) {
    try {
      localStorage.setItem(REGION_KEY, region);
      localStorage.setItem(REGION_TS, String(Date.now()));
    } catch (e) {}
  }

  // ── 中文文案表（仅 pricing 页可见文案；精确原文匹配替换）──
  var ZH_TEXT = {
    "Features": "功能",
    "Pricing": "定价",
    "Models": "模型",
    "Download": "下载",
    "Pricing ": "定价",
    "Simple,": "简单、",
    "honest": "诚实",
    "pricing.": "的定价。",
    "Simple, honest pricing.": "简单、诚实的定价。",
    "Start free forever. Every new user gets 3,000 credits — enough to try every flagship model before you pay a cent.":
      "永久免费开始。每位新用户都送 3000 积分 — 足以把旗舰模型全试一遍，一分钱不用花。",
    "Start free forever. Upgrade when you need the world's most powerful AI models.":
      "永久免费开始。需要全球最强 AI 模型时再升级。",
    "Credits": "积分",
    "Top-up packs": "积分充值包",
    "One currency for every model. 1 credit ≈ $0.01. Buy in bigger packs, pay less per credit — and credits never expire.":
      "一个积分通用于所有模型。1 积分 ≈ ¥0.01。买大包单价更低，且积分永不过期。",
    "Starter": "入门包",
    "Plus": "超值包",
    "Mega": "畅享包",
    "Best value": "最划算",
    "credits": "积分",
    "$0.0020 / credit": "¥0.012 / 积分",
    "$0.0015 / credit": "¥0.011 / 积分",
    "$0.0014 / credit": "¥0.010 / 积分",
    "New users: 3,000 credits on the house — every flagship model unlocked until they run out.":
      "新用户：白送 3000 积分 — 用尽之前全部旗舰模型解锁。",
    "Daily check-in: +100 credits, 15 times for new accounts.":
      "每日签到：+100 积分，新账号可领 15 次。",
    "Metered honestly: each model has its own published credit rate — you see the balance tick down live in the status bar.":
      "计价透明：每个模型都有公开的积分费率 — 余额在状态栏实时跳动。",
    "Never wasted: when your balance bottoms out the app drops back to Free mode instead of silently charging you.":
      "不浪费：余额触底后 App 自动回到免费版，不会偷偷扣费。",
    "Free": "免费版",
    "Local AI on your own GPU, plus free OpenRouter models. Zero cost, nothing leaves your PC.":
      "本地 GPU AI + OpenRouter 免费模型。零成本，数据不出你的电脑。",
    "forever": "永久",
    "Unlimited local chat via Ollama": "Ollama 本地对话不限量",
    "3,000 welcome credits — try every model free": "新人赠 3000 积分 — 全模型免费试",
    "Daily check-in: 100 credits × 15": "每日签到领 100 积分 × 15 期",
    "78 built-in models, 14 China-direct platforms": "内置 78 个模型、14 个国内直连平台",
    "Free OpenRouter models included": "附赠 OpenRouter 免费模型",
    "87 built-in agent tools": "内置 87 个 Agent 工具",
    "File / image / vision support": "支持文件 / 图片 / 视觉",
    "Full privacy — nothing leaves your PC": "完全私密 — 数据不出本机",
    "Contains ads": "含广告",
    "Standard": "标准会员",
    "The value lineup — DeepSeek V4 Flash, Qwen3.8 Flash, GLM 4.6, Doubao Seed Lite. Fast, cheap, vision included.":
      "性价比阵容 — DeepSeek V4 Flash、Qwen3.8 Flash、GLM 4.6、豆包 Seed Lite。快、便宜、带识图。",
    "/ month": "/ 月",
    "800 credits every month included": "每月含 800 积分",
    "DeepSeek V4 Flash · Qwen3.8 Flash · GLM 4.6": "DeepSeek V4 Flash · Qwen3.8 Flash · GLM 4.6",
    "Smart routing with sticky model choice": "智能路由，手选模型不漂移",
    "Rolling context compression (saves tokens)": "滚动上下文压缩（省 token）",
    "Vision &amp; multimodal input": "视觉与多模态输入",
    "Vision & multimodal input": "视觉与多模态输入",
    "Everything in Free": "含免费版全部功能",
    "Ad-free experience · Email support": "无广告 · 邮件支持",
    "Get Standard": "购买标准会员",
    "Popular": "人气之选",
    "Pro": "专业会员",
    "Flagship Chinese lineup — DeepSeek V4 Pro, GLM 5.3, Kimi K3, Qwen3.8 Max — plus AI video and music generation.":
      "国产旗舰阵容 — DeepSeek V4 Pro、GLM 5.3、Kimi K3、Qwen3.8 Max — 再加 AI 视频与音乐生成。",
    "3,000 credits every month included": "每月含 3000 积分",
    "DeepSeek V4 Pro · GLM 5.3 · Kimi K3 · Qwen3.8 Max": "DeepSeek V4 Pro · GLM 5.3 · Kimi K3 · Qwen3.8 Max",
    "Dual-channel failover (primary + fallback)": "双通道互备（主 + 备自动切换）",
    "AI video generation (Kling) — animate any photo": "AI 视频生成（可灵）— 让照片动起来",
    "AI music generation (Suno) — full songs with vocals": "AI 音乐生成（Suno）— 带人声的完整歌曲",
    "Bring your own key: any OpenAI-compatible platform": "自带 Key：任意 OpenAI 兼容平台",
    "Everything in Standard · Priority support": "含标准会员全部功能 · 优先支持",
    "Get Pro": "购买专业会员",
    "Ultra": "旗舰会员",
    "Engineering-grade capability: true CAD modeling with B-rep solids, STEP / DXF export, larger context and higher limits.":
      "工程级能力：B-rep 实体真 CAD 建模、STEP / DXF 导出、更大上下文与更高额度。",
    "10,000 credits every month included": "每月含 10000 积分",
    "Engineering-level CAD (CadQuery / OpenCASCADE)": "工程级 CAD（CadQuery / OpenCASCADE）",
    "True B-rep solids — fillet, chamfer, boolean, holes": "真 B-rep 实体 — 圆角、倒角、布尔、打孔",
    "Export STEP / DXF / STL / OBJ": "导出 STEP / DXF / STL / OBJ",
    "Self-researched, cross-validated dimensions": "自研尺寸交叉校验",
    "Larger context windows · Higher daily limits": "更大上下文 · 更高每日额度",
    "Everything in Pro": "含专业会员全部功能",
    "Get Ultra": "购买旗舰会员",
    "No ceiling": "不设上限",
    "Max": "极限会员",
    "Pay as you go with no monthly ceiling — top up credits any time or let your card auto-charge.":
      "按量付费、无月度上限 — 随时充值积分，或绑卡自动扣费。",
    "+ usage": "+ 按量",
    "No monthly ceiling — billed by credits consumed": "无月度上限 — 按消耗的积分计费",
    "Top-up packs from $2 — never expire": "积分包 $2 起 — 永不过期",
    "Every model unlocked while you have credits": "有积分即解锁全部模型",

    "Specialist agents: deep research, autonomous coding": "专攻 Agent：深度研究、自主编程",
    "Self-researching CAD modeling agent": "自主研究型 CAD 建模 Agent",
    "Short-drama storyboarding & music agents": "短剧分镜与音乐 Agent",
    "Short-drama storyboarding &amp; music agents": "短剧分镜与音乐 Agent",
    "Early access to new models & providers": "新模型 / 新渠道抢先体验",
    "Early access to new models &amp; providers": "新模型 / 新渠道抢先体验",
    "Dedicated support": "专属客服",
    "Get Max": "购买极限会员",
    "FAQ": "常见问题",
    "Common Questions": "常见问题",
    "How do I activate after payment?": "付款后如何激活？",
    "Once payment completes you'll receive a license key by email. Open the app, switch the mode dropdown to your plan, and paste the key. Activation is bound to one device; reinstalling on the same PC keeps working. Locked tiers show a 🔒 in the dropdown until your subscription or license is active.":
      "付款完成后会通过邮件发放激活码。打开 App，在模式下拉框切到对应档位，粘贴激活码即可。激活绑定一台设备；同一台电脑重装不影响使用。未解锁的档位在下拉框里会显示 🔒。",
    "What payment methods do you accept?": "支持哪些付款方式？",
    "Visa, Mastercard and PayPal. Payments are processed securely by Creem, our merchant of record; we never see or store your card details.":
      "Visa、Mastercard、PayPal。支付由持牌收单方 Creem 安全处理；我们不接触也不存储你的银行卡信息。",
    "Do you add extra content filters on top of the models?": "你们在模型之上加额外的内容过滤吗？",
    "No. We don't bolt extra refusal lists or filters onto the models — you get the raw capability you're paying for. Standard provider safety still applies, and you're responsible for how you use the output.":
      "不加。我们不在模型外再叠加额外的拒绝清单或过滤器 — 你买到的就是模型本身的能力。渠道方自身的安全策略仍然适用，输出内容的使用责任由你承担。",
    "Can I cancel anytime?": "可以随时取消吗？",
    "Yes. Your plan stays active until the end of the paid period, then the app simply returns to Free mode. Your chat history is stored locally and never lost.":
      "可以。会员持续到已付周期结束，之后 App 自动回到免费版。聊天记录都存在本地，不会丢失。",
    "Is my data private?": "我的数据私密吗？",
    "Completely. Chat history, memories and settings are stored only on your computer. In Free mode nothing ever leaves your machine.":
      "完全私密。聊天记录、记忆与设置只存在你自己的电脑上。免费模式下没有任何数据离开你的机器。",
    "Which models can I use — and does my region matter?": "我能用哪些模型 — 地区有影响吗？",
    "Can I bring my own API key?": "可以自带 API Key 吗？",
    "Yes — and it is encouraged. Any OpenAI-compatible platform works: SiliconFlow, Alibaba Bailian, DeepSeek official, Volcano Ark, Zhipu, Moonshot Kimi, MiniMax, Tencent Hunyuan, ModelScope, 302.AI, DMXAPI, AIHubMix, NVIDIA NIM, StepFun or OpenRouter. Pick the platform from a dropdown, the base URL fills itself in, paste your key and you are running on your own quota. You can add two platforms at once and the app will fail over between them automatically.":
      "可以 — 而且鼓励。任何 OpenAI 兼容平台都能用：硅基流动、阿里百炼、DeepSeek 官方、火山方舟、智谱、Moonshot Kimi、MiniMax、腾讯混元、ModelScope、302.AI、DMXAPI、AIHubMix、NVIDIA NIM、StepFun、OpenRouter。下拉框选平台 → Base URL 自动带出 → 粘贴 Key 即可用自己的额度。可同时加两个平台，主通道挂了自动切换。",
    "What counts as \"usage\" on the Max plan?": "极限会员的「按量」怎么算？",
    "Credits burned by the calls you actually make. Each model is metered at its published credit rate, which is derived from the provider's live price with a small routing margin — there is no monthly message ceiling and no per-seat charge. You start with your 3,000 welcome credits; after that you top up manually or let a linked card auto-charge. Every call logs model, input/output tokens and credits spent, so you can reconcile the balance against your provider bill line by line.":
      "按你实际调用消耗的积分计费。每个模型按公开的积分费率计费（由渠道实时价 + 少量路由服务费换算而来）——没有月度条数上限，也不按席位收费。注册即送 3000 积分；之后可手动充值或绑卡自动扣费。每次调用都会记录模型、输入/输出 token 与消耗积分，可与渠道账单逐条对账。",
    "What exactly are credits, and how fast do they burn?": "积分到底是什么？烧得快吗？",
    "Credits are the single currency behind every model, so a cheap model and a flagship model can live in the same wallet. Each model has its own published rate per 1,000 tokens (input and output priced separately), shown in the app next to each model. A quick chat with a small model costs a fraction of a credit; hammering the most expensive frontier model costs more. Your balance sits in the status bar and ticks down live as the AI replies, so there is never a surprise invoice. New accounts start with 3,000 credits, and daily check-in adds another 100 for the first 15 days.":
      "积分是所有模型通用的唯一货币，便宜模型和旗舰模型共用一个钱包。每个模型都有公开的费率（按每 1000 token 计，输入与输出分开计价），在 App 里每个模型旁边就能看到。用小模型随便聊几句只花零点几积分；狠用最贵的旗舰模型则更贵。余额就在状态栏，AI 回复时实时往下跳，不会出现事后才知道的账单。新账号送 3000 积分，前 15 天每天签到再领 100。",
    "Do credits expire, and what happens when I run out?": "积分会过期吗？用完了会怎样？",
    "They never expire, and unused monthly credits stay in your balance. When your balance hits the floor the app automatically drops back to Free mode — local models and free OpenRouter models keep working, paid models pause, and a prompt offers a top-up. You are never silently charged and nothing is auto-renewed without you turning it on.":
      "不会过期，每月没用完的积分留在余额里。余额触底时 App 自动回到免费版 —— 本地模型和 OpenRouter 免费模型照常可用，付费模型暂停，并提示你充值。全程不会偷偷扣费，也不会在你没开启的情况下自动续订。",
    "I have my own API key — do I still need a membership?": "我自带 API Key，还需要买会员吗？",
    "Your own key runs in Free mode, on your own quota, forever, at no charge from us. What a membership adds is different: bundled credits at a lower per-credit price, and access to the tiers of models the app otherwise gates — flagship reasoning, media generation and the engineering toolchain. In short, your key pays your provider; a membership unlocks the app.":
      "自带 Key 在免费版下跑，用自己的额度，永久免费，我们不收钱。会员增加的是另一样东西：更低价位的批量积分，以及解锁 App 原本锁着的高阶模型 —— 旗舰推理、媒体生成和工程工具链。一句话：你的 Key 付钱给渠道，会员才是解锁 App 的钥匙。",
    "You get 78 built-in models across five plans, spanning DeepSeek, Qwen, GLM, Kimi, MiniMax, Doubao, Hunyuan, Ernie and Grok, plus the OpenRouter catalogue. Some closed models from OpenAI, Anthropic and Google are unavailable in certain billing regions. The app probes this automatically at startup (once per key, at no meaningful cost), badges the affected models as region-locked, and routes around them — so you are never left guessing why a model will not run. In mainland China it goes one step further: Auto mode prefers the domestic model group (DeepSeek / Qwen / GLM / Kimi and friends) so you keep full speed without a VPN. Fourteen China-direct platforms are also preconfigured, covering exactly the models that international aggregators restrict.":
      "五档会员共内置 78 个模型，覆盖 DeepSeek、Qwen、GLM、Kimi、MiniMax、豆包、混元、文心、Grok，以及 OpenRouter 整个目录。部分 OpenAI / Anthropic / Google 的闭源模型在特定账单地区不可用。App 会在启动时自动体检（每把 Key 一次，几乎零成本），把受影响的模型标为「地区受限」并自动绕开 —— 不用再猜为什么某个模型跑不起来。在中国大陆还更进一步：自动模式会优先选用国产模型组（DeepSeek / Qwen / GLM / Kimi 等），不挂 VPN 也能全速使用。同时预置了 14 个国内直连平台，正好覆盖国际聚合器限制的那些模型。",
    "Terms": "服务条款",
    "Refunds": "退款政策",
    "Privacy": "隐私政策",
    "Acceptable Use": "使用规范",
    "Home": "回首页"
  };

  // ── 文案替换：精确匹配文本节点 ──
  function swapTextZh() {
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    for (var i = 0; i < nodes.length; i++) {
      var t = nodes[i];
      var v = ZH_TEXT[t.nodeValue.trim()];
      if (v) {
        if (t.__origEn === undefined) t.__origEn = t.nodeValue;   // 首次替换前存原文
        t.nodeValue = v;
      }
    }
    // 属性里也有英文（aria-label 等）
    var labeled = document.querySelectorAll('[aria-label="Toggle theme"]');
    for (var j = 0; j < labeled.length; j++) labeled[j].setAttribute("aria-label", "切换主题");
  }

  // ── 海外残留中文自愈表：静态 HTML 里的英文短语被误翻成中文后，能换回来 ──
  var LEFTOVER_ZH = {
    "/ 月": "/ month", "/月": "/ month",
    "+ 按量": "+ usage", "按量": "usage",
    "永久": "forever"
  };

  // ── 还原英文（海外访客 / VPN 切换后）──
  function restoreTextEn() {
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    for (var i = 0; i < nodes.length; i++) {
      var t = nodes[i];
      if (t.__origEn !== undefined) { t.nodeValue = t.__origEn; t.__origEn = undefined; }
      var k = t.nodeValue.trim();
      if (LEFTOVER_ZH[k]) t.nodeValue = LEFTOVER_ZH[k];   // 兜底：清掉误翻残留
    }
    var badges = document.querySelector(".pay-badges");
    if (badges && badges.getAttribute("data-cn")) {
      badges.removeAttribute("data-cn");
      var sp = badges.querySelectorAll("span");
      for (var k = sp.length - 1; k >= 0; k--) {
        var txt = sp[k].textContent;
        if (txt === "支付宝" || txt === "微信支付") badges.removeChild(sp[k]);
      }
    }
  }

  // ── 币种替换 ──
  function cnyOf(usd) {
    var cny = USD2CNY[String(usd)];
    if (cny === undefined) cny = Math.round(usd * CNY_FALLBACK_RATE);
    return cny;
  }

  function applyCNY() {
    // 形态一：pricing.html 的 .price 块（.currency/.num/.per 结构）
    var blocks = document.querySelectorAll(".price[data-usd]");
    for (var i = 0; i < blocks.length; i++) {
      var b = blocks[i];
      var usd = parseFloat(b.getAttribute("data-usd") || "0");
      var cur = b.querySelector(".currency");
      var num = b.querySelector(".num");
      var per = b.querySelector(".per");
      if (cur) cur.textContent = "¥";
      if (num) num.textContent = String(cnyOf(usd));
      if (per) {
        per.textContent = per.textContent
          .replace("/ month", "/ 月")
          .replace("forever", "永久")
          .replace("+ usage", "+ 按量");
      }
    }
    // 形态二：通用 data-usd 元素（如 index.html 的 .amt "$4<small>/月</small>"）——
    // 直接遍历其文本节点，把 "$" 换 "¥"、美元数字换人民币数字
    var generic = document.querySelectorAll("[data-usd]:not(.price)");
    for (var g = 0; g < generic.length; g++) {
      var el = generic[g];
      var target = parseFloat(el.getAttribute("data-usd") || "-1");
      if (target < 0) continue;
      var tn = [];
      var w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null, false);
      while (w.nextNode()) tn.push(w.currentNode);
      var doneNum = false;
      for (var t = 0; t < tn.length; t++) {
        var s = tn[t].nodeValue;
        if (s.indexOf("$") >= 0) tn[t].nodeValue = s.replace(/\$/g, "¥");
        if (!doneNum) {
          var re = new RegExp("\\b" + target + "(?!\\d)");
          if (re.test(s)) {
            tn[t].nodeValue = tn[t].nodeValue.replace(re, String(cnyOf(target)));
            doneNum = true;
          }
        }
      }
    }
    // 支付方式徽章：国内补充支付宝 / 微信
    var badges = document.querySelector(".pay-badges");
    if (badges && !badges.getAttribute("data-cn")) {
      badges.setAttribute("data-cn", "1");
      var s1 = document.createElement("span"); s1.textContent = "支付宝";
      var s2 = document.createElement("span"); s2.textContent = "微信支付";
      badges.appendChild(s1); badges.appendChild(s2);
    }
  }

  function applyRegion(region) {
    document.documentElement.setAttribute("data-region", region);
    // 用户是否手动选过语言（i18n.js 的 isManual；手动选择永远优先）
    var manual = false;
    try {
      manual = !!(window.WM_I18N && window.WM_I18N.isManual && window.WM_I18N.isManual());
    } catch (e) { manual = false; }
    if (region === "CN") {
      applyCNY();
      if (!manual) {
        swapTextZh();                                   // pricing 页（无 i18n.js）中文
        try {
          if (window.WM_I18N && window.WM_I18N.get() !== "zh") {
            window.WM_I18N.apply("zh", false);          // index 页走 i18n 引擎，不落盘
          }
        } catch (e) {}
      } else if (savedLang() === "zh") {
        swapTextZh();
      }
    } else {
      // 海外：还原英文 + 美元（HTML 默认值本就是英文/美元）
      if (!manual) {
        restoreTextEn();
        try {
          if (window.WM_I18N && window.WM_I18N.get() !== "en") {
            window.WM_I18N.apply("en", false);
          }
        } catch (e) {}
      }
    }
    document.dispatchEvent(new CustomEvent("wm:region", { detail: { region: region } }));
  }

  function init() {
    var cached = getCache();
    var nav = (navigator.language || "en").toLowerCase();
    // 首屏：有缓存用缓存，没缓存用浏览器语言启发式（都只是「先渲染」，随后必被 IP 结果纠正）
    var guess = cached || ((nav.indexOf("zh") === 0) ? "CN" : "OVERSEAS");
    applyRegion(guess);

    // 异步 IP 探测纠正（ipwho.is 主 → ipapi.co 备，2.5s 超时）
    function probe(urls, idx) {
      if (idx >= urls.length) { putCache(guess); return; }
      var ctrl = null;
      try { ctrl = new AbortController(); } catch (e) { putCache(guess); return; }
      var timer = setTimeout(function () { try { ctrl.abort(); } catch (e) {} }, 2500);
      fetch(urls[idx], { signal: ctrl.signal })
        .then(function (r) { return r.json(); })
        .then(function (j) {
          clearTimeout(timer);
          var cc = String(j.country_code || j.countryCode || "").toUpperCase();
          var region = (cc === "CN") ? "CN" : "OVERSEAS";
          putCache(region);
          if (region !== document.documentElement.getAttribute("data-region")) {
            applyRegion(region);
          }
        })
        .catch(function () {
          clearTimeout(timer);
          probe(urls, idx + 1);
        });
    }
    probe(["https://ipwho.is/", "https://ipapi.co/json/"], 0);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  window.WM_REGION = {
    get: function () { return document.documentElement.getAttribute("data-region") || "OVERSEAS"; },
    apply: applyRegion
  };
})();
