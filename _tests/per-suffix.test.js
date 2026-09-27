/* region.js 价格后缀行为测试 —— 用最小 DOM 桩复现真实调用顺序
 * 重点复现「用户截图那个组合」：海外地区 + 用户手动选过中文 => 之后手选英文。
 * 之前的实现里 region.js 被 if(!manual) 整段跳过，静态中文就漏出来了。
 */
const fs = require("fs");

/* ─────────── 最小 DOM 桩 ─────────── */
class Txt { constructor(v) { this.nodeValue = v; this.__t = "t"; } }
class El {
  constructor(tag, attrs) {
    this.tag = tag; this.attrs = attrs || {}; this.children = []; this.parent = null; this.__t = "e";
  }
  get _cls() { return (this.attrs["class"] || "").split(/\s+/).filter(Boolean); }
  getAttribute(k) { return k in this.attrs ? this.attrs[k] : null; }
  setAttribute(k, v) { this.attrs[k] = String(v); }
  removeAttribute(k) { delete this.attrs[k]; }
  appendChild(n) { n.parent = this; this.children.push(n); return n; }
  removeChild(n) { this.children = this.children.filter(c => c !== n); }
  get textContent() {
    let s = "";
    for (const c of this.children) s += c.__t === "t" ? c.nodeValue : c.textContent;
    return s;
  }
  set textContent(v) { this.children = [new Txt(v)]; }
  get innerHTML() {
    let s = "";
    for (const c of this.children) {
      if (c.__t === "t") { s += c.nodeValue; continue; }
      const a = Object.keys(c.attrs).map(k => ` ${k}="${c.attrs[k]}"`).join("");
      s += `<${c.tag}${a}>${c.innerHTML}</${c.tag}>`;
    }
    return s;
  }
  set innerHTML(v) { this.children = [new Txt(v)]; }
  matches(sel) { return matchSel(this, sel); }
  _all(out) { for (const c of this.children) if (c.__t === "e") { out.push(c); c._all(out); } return out; }
  querySelectorAll(sel) { return this._all([]).filter(e => matchSel(e, sel)); }
  querySelector(sel) { return this.querySelectorAll(sel)[0] || null; }
  closest(sel) { let n = this; while (n) { if (n.__t === "e" && matchSel(n, sel)) return n; n = n.parent; } return null; }
}
function matchSel(el, sel) {
  // 支持逗号分组。每个 token：tag / .class / [attr] / [attr="v"] / :not(.class)
  return String(sel).split(",").some(part => {
    part = part.trim();
    const m = part.match(/^([a-zA-Z0-9]*)((?:[.#\[][^\s]*)*)$/);
    let rest;
    if (m) { rest = m[2]; if (m[1] && el.tag !== m[1]) return false; }
    else rest = part;
    const tokens = rest.match(/\[[^\]]*\]|\.[A-Za-z0-9_-]+|:not\([^)]*\)/g) || [];
    for (const tk of tokens) {
      if (tk[0] === ".") { if (!el._cls.includes(tk.slice(1))) return false; }
      else if (tk === ":not(.price)") { if (el._cls.includes("price")) return false; }
      else if (tk[0] === "[") {
        const inner = tk.slice(1, -1);
        const eq = inner.indexOf("=");
        if (eq < 0) { if (el.getAttribute(inner) === null) return false; }
        else {
          const k = inner.slice(0, eq), v = inner.slice(eq + 1).replace(/^"|"$/g, "");
          if (el.getAttribute(k) !== v) return false;
        }
      }
    }
    return true;
  });
}
function walkText(root) {
  const out = [];
  (function go(n) { for (const c of n.children) { if (c.__t === "t") out.push(c); else go(c); } })(root);
  return out;
}

/* ─────────── 组装 index.html 的定价卡片结构 ─────────── */
function buildDoc() {
  const body = new El("body", {});
  const doc = {
    readyState: "complete",
    documentElement: new El("html", {}),
    body,
    addEventListener() {}, dispatchEvent() {},
    createElement: t => new El(t, {}),
    createTreeWalker(root) {
      const nodes = walkText(root); let i = 0;
      const w = {
        currentNode: null,
        nextNode() {
          if (i < nodes.length) { w.currentNode = nodes[i++]; return w.currentNode; }
          return false;
        },
      };
      return w;
    },
  };
  doc.documentElement.appendChild(new El("head", {}));
  doc.documentElement.appendChild(body);
  doc.querySelector = s => body.querySelector(s) || doc.documentElement.querySelector(s);
  doc.querySelectorAll = s => body.querySelectorAll(s).concat(doc.documentElement.querySelectorAll(s).filter(e => e !== body));

  // 定价卡片：.amt[data-usd] = "$4<small data-per=month>/ month</small>"
  const plans = [
    [4, "month", "/ month"], [14, "month", "/ month"],
    [42, "month", "/ month"], [0, "usage", "+ usage"],
  ];
  doc.cards = plans.map(([usd, kind, txt]) => {
    const amt = new El("div", { class: "amt", "data-usd": String(usd) });
    amt.appendChild(new Txt("$" + usd));
    const sm = new El("small", { "data-per": kind });
    sm.appendChild(new Txt(txt));
    amt.appendChild(sm);
    const h3 = new El("h3", { "data-i18n": "home.price.name" });
    h3.appendChild(new Txt("标准版"));
    const wrap = new El("div", {});
    wrap.appendChild(h3); wrap.appendChild(amt);
    body.appendChild(wrap);
    return { amt, sm };
  });
  return doc;
}

/* ─────────── 加载 region.js ─────────── */
const doc = buildDoc();
const langBox = { v: "en", manual: false };
global.document = doc;
global.navigator = { language: langBox.v, languages: [langBox.v] };
global.NodeFilter = { SHOW_TEXT: 4 };
global.CustomEvent = class { constructor(t, o) { this.type = t; this.detail = o && o.detail; } };
global.location = { href: "https://workingmateapp.com/", origin: "https://workingmateapp.com" };
global.fetch = () => new Promise(() => {});          // 不真发 IP 探测
const store = {};
global.localStorage = {
  getItem: k => (k in store ? store[k] : null),
  setItem: (k, v) => { store[k] = String(v); },
};
global.window = global;
global.setTimeout = (fn) => fn && 0;
global.window.WM_I18N = {
  get: () => langBox.v,
  isManual: () => langBox.manual,
  apply: (l) => { langBox.v = l; },
};

const src = fs.readFileSync("region.js", "utf8");
new Function(src)();

/* ─────────── 断言 ─────────── */
let pass = 0, fail = 0;
function check(name, got, want) {
  const ok = got === want;
  ok ? pass++ : fail++;
  console.log(`  ${ok ? "✓" : "✗"} ${name}\n      得到: ${JSON.stringify(got)}  期望: ${JSON.stringify(want)}`);
  return ok;
}
function snap() { return doc.cards.map(c => c.amt.textContent); }

console.log("【场景 1】海外 + 英文（默认国际版）");
langBox.v = "en"; langBox.manual = false;
global.WM_REGION.apply("OVERSEAS");
check("卡片文案", snap().join(" | "), "$4/ month | $14/ month | $42/ month | $0+ usage");

console.log("\n【场景 2】大陆 + 中文");
langBox.v = "zh"; langBox.manual = false;
global.WM_REGION.apply("CN");
check("货币+后缀", snap().join(" | "), "¥28/ 月 | ¥100/ 月 | ¥300/ 月 | ¥0+ 按量");

console.log("\n【场景 3】海外 + 用户手动选过中文（← 你截图那个组合，之前必漏）");
langBox.v = "zh"; langBox.manual = true;
global.WM_REGION.apply("OVERSEAS");
check("地区海外 -> 货币必须是 $", snap()[0][0], "$");
check("语言中文 -> 后缀必须是 / 月", snap()[0].includes("/ 月"), true);
check("全部卡片", snap().join(" | "), "$4/ 月 | $14/ 月 | $42/ 月 | $0+ 按量");

console.log("\n【场景 4】海外 + 用户手动选英文（你截图的目标状态）");
langBox.v = "en"; langBox.manual = true;
global.WM_REGION.apply("OVERSEAS");
check("卡片文案", snap().join(" | "), "$4/ month | $14/ month | $42/ month | $0+ usage");

console.log("\n【场景 5】地区纠错：CN 误判 -> 纠正为 OVERSEAS，货币要能退回 $");
langBox.v = "zh"; langBox.manual = false;
global.WM_REGION.apply("CN");
check("CN 时", snap()[0], "¥28/ 月");
langBox.v = "en";
global.WM_REGION.apply("OVERSEAS");
check("纠正后必须退回 $", snap().join(" | "), "$4/ month | $14/ month | $42/ month | $0+ usage");

console.log("\n【场景 6】幂等：同一个状态反复 apply 结果不变");
global.WM_REGION.apply("OVERSEAS"); global.WM_REGION.apply("OVERSEAS");
check("重复调用", snap().join(" | "), "$4/ month | $14/ month | $42/ month | $0+ usage");

console.log("\n【场景 7】10 种语言的月付后缀");
const want = { en: "/ month", zh: "/ 月", ja: "/ 月", ko: "/ 월", fr: "/ mois", de: "/ Monat",
               ru: "/ месяц", ar: "/ شهريًا", es: "/ mes", pt: "/ mês" };
for (const l of Object.keys(want)) {
  langBox.v = l; langBox.manual = true;
  global.WM_REGION.apply("OVERSEAS");
  check(l, doc.cards[0].amt.textContent, "$4" + want[l]);
}

console.log(`\n结果: ${pass} 通过 / ${fail} 失败`);
process.exit(fail ? 1 : 0);
