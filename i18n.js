/* ════════════════════════════════════════════════════════════
   Working Mate — 静态站多语言引擎（与桌面端 i18n 思路一致）
   用法：
     <head> 里 <link rel="stylesheet" href="lang.css">
     </body> 前依次引入各语言包：lang.en.js … lang.pt.js
     最后引入本文件 i18n.js
   规则：
     元素加 data-i18n="key"        → 替换 textContent
     元素加 data-i18n-html="key"   → 替换 innerHTML（含 <small>/<span> 等）
     元素加 data-i18n-attr="attr1:key1,attr2:key2" → 替换属性（如 aria-label）
   中文为 HTML 默认值，引擎首次加载记下原文，切回 zh 时还原，
   故语言包只需 9 种外语（en/ja/ko/fr/de/ru/ar/es/pt）。
   ════════════════════════════════════════════════════════════ */
(function () {
  "use strict";

  var SUPPORTED = ["zh", "en", "ja", "ko", "fr", "de", "ru", "ar", "es", "pt"];
  var RTL = ["ar"];
  // 浏览器语言 → 站点语言 的归一（覆盖常见 region 变体）
  var ALIAS = {
    "zh-CN": "zh", "zh-TW": "zh", "zh-HK": "zh", "zh": "zh",
    "en-US": "en", "en-GB": "en", "en": "en",
    "ja": "ja", "ko": "ko",
    "fr": "fr", "fr-FR": "fr", "fr-CA": "fr",
    "de": "de", "de-DE": "de",
    "ru": "ru", "ru-RU": "ru",
    "ar": "ar", "ar-SA": "ar",
    "es": "es", "es-ES": "es", "es-MX": "es", "es-419": "es",
    "pt": "pt", "pt-BR": "pt", "pt-PT": "pt"
  };
  var LANG_NAMES = {
    zh: "简体中文", en: "English", ja: "日本語", ko: "한국어",
    fr: "Français", de: "Deutsch", ru: "Русский", ar: "العربية",
    es: "Español", pt: "Português"
  };
  var LOCALE = {
    zh: "zh-CN", en: "en", ja: "ja", ko: "ko", fr: "fr", de: "de",
    ru: "ru", ar: "ar", es: "es", pt: "pt"
  };
  var STORE_KEY = "wm_lang";

  var MANUAL_KEY = "wm_lang_manual";   // 只有用户手动切换过才置 1

  function detect() {
    // ① 用户手动选择过语言 → 最高优先，永不覆盖
    var saved = null, manual = null;
    try {
      saved = localStorage.getItem(STORE_KEY);
      manual = localStorage.getItem(MANUAL_KEY);
    } catch (e) {}
    if (manual && saved && SUPPORTED.indexOf(saved) >= 0) return saved;
    // ② 地区（region.js 已同步写入 data-region）→ 大陆中文 / 海外英文
    try {
      var region = document.documentElement.getAttribute("data-region");
      if (region === "CN") return "zh";
      if (region === "OVERSEAS") return "en";
    } catch (e) {}
    var navs = navigator.languages || [navigator.language || "en"];
    for (var i = 0; i < navs.length; i++) {
      var code = String(navs[i]).split("-")[0];
      var full = ALIAS[String(navs[i])];
      if (full && SUPPORTED.indexOf(full) >= 0) return full;
      if (SUPPORTED.indexOf(code) >= 0) return code;
    }
    return "en"; // 全球化默认回退英文
  }

  var DICT = (window.I18N = window.I18N || {});
  var current = detect();

  function look(key, lang) {
    var pack = DICT[lang];
    if (pack && Object.prototype.hasOwnProperty.call(pack, key)) return pack[key];
    var en = DICT.en;
    if (en && Object.prototype.hasOwnProperty.call(en, key)) return en[key];
    return undefined;
  }

  function applyLang(lang, persist) {
    current = lang;
    // persist === false → 地区自动判定，不写手动标记（否则海外用户会被永久钉在中文）
    if (persist !== false) {
      try {
        localStorage.setItem(STORE_KEY, lang);
        localStorage.setItem(MANUAL_KEY, "1");
      } catch (e) {}
    }

    var html = document.documentElement;
    html.setAttribute("lang", LOCALE[lang] || lang);
    html.setAttribute("dir", RTL.indexOf(lang) >= 0 ? "rtl" : "ltr");

    // 捕获原文（仅首次）：用于切回中文时还原
    var nodes = document.querySelectorAll("[data-i18n],[data-i18n-html]");
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      if (el.__orig === undefined) el.__orig = el.innerHTML;
    }

    for (var j = 0; j < nodes.length; j++) {
      var e = nodes[j];
      var key = e.getAttribute("data-i18n") || e.getAttribute("data-i18n-html");
      if (lang === "zh") {
        e.innerHTML = e.__orig;
        continue;
      }
      var val = look(key, lang);
      if (val === undefined) continue;
      if (e.getAttribute("data-i18n-html")) e.innerHTML = val;
      else e.textContent = val;
    }

    // 属性替换
    var attrNodes = document.querySelectorAll("[data-i18n-attr]");
    for (var k = 0; k < attrNodes.length; k++) {
      var an = attrNodes[k];
      var spec = an.getAttribute("data-i18n-attr").split(",");
      for (var s = 0; s < spec.length; s++) {
        var pair = spec[s].split(":");
        if (pair.length !== 2) continue;
        var attr = pair[0].trim();
        var akey = pair[1].trim();
        if (lang === "zh") {
          // 中文默认属性在 HTML 中已写好，无需还原处理（属性一般无所谓）
          continue;
        }
        var av = look(akey, lang);
        if (av !== undefined) an.setAttribute(attr, av);
      }
    }

    syncSwitcher();
    document.dispatchEvent(new CustomEvent("wm:lang", { detail: { lang: lang } }));
  }

  // ──────────── 语言切换器 ────────────
  function buildSwitcher() {
    var mount = document.getElementById("langmount");
    if (!mount) return;
    var wrap = document.createElement("div");
    wrap.className = "lang-sw";
    var items = SUPPORTED.map(function (l) {
      return '<li data-lang="' + l + '"><span class="dot-' + l + '"></span>' + LANG_NAMES[l] + "</li>";
    }).join("");
    wrap.innerHTML =
      '<button class="lang-btn" type="button" aria-haspopup="true" aria-expanded="false">' +
      '<span class="globe">🌐</span><span class="lang-cur">' + LANG_NAMES[current] + "</span>" +
      '<span class="caret">▾</span></button>' +
      '<ul class="lang-menu" role="menu">' + items + "</ul>";
    mount.appendChild(wrap);

    var btn = wrap.querySelector(".lang-btn");
    var menu = wrap.querySelector(".lang-menu");
    btn.addEventListener("click", function (ev) {
      ev.stopPropagation();
      var open = wrap.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    menu.addEventListener("click", function (ev) {
      var li = ev.target.closest("li[data-lang]");
      if (!li) return;
      applyLang(li.getAttribute("data-lang"));
      wrap.classList.remove("open");
      btn.setAttribute("aria-expanded", "false");
    });
    document.addEventListener("click", function () {
      wrap.classList.remove("open");
      btn.setAttribute("aria-expanded", "false");
    });
  }

  function syncSwitcher() {
    var cur = document.querySelector(".lang-cur");
    if (cur) cur.textContent = LANG_NAMES[current] || current;
    var lis = document.querySelectorAll(".lang-sw .lang-menu li");
    for (var i = 0; i < lis.length; i++) {
      lis[i].classList.toggle("active", lis[i].getAttribute("data-lang") === current);
    }
  }

  function init() {
    current = detect();      // 此时 region.js 已写入 data-region，按地区定语言（不闪）
    buildSwitcher();
    applyLang(current, false);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  window.WM_I18N = {
    apply: applyLang,
    get: function () { return current; },
    isManual: function () { try { return !!localStorage.getItem(MANUAL_KEY); } catch (e) { return false; } },
    dict: DICT
  };
})();
