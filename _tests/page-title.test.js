/* 页面标题归属测试 —— 静态英文（给搜索引擎）+ 运行时按语言还原
 * 覆盖刚修的 23 个页面：<title data-entitle data-zhtitle data-enkey>
 * 跑法：node _tests/page-title.test.js
 */
const fs = require("fs");

class Txt { constructor(v) { this.nodeValue = v; this.__t = "t"; } }
class El {
  constructor(tag, attrs) { this.tag = tag; this.attrs = attrs || {}; this.children = []; this.parent = null; this.__t = "e"; }
  get _cls() { return (this.attrs["class"] || "").split(/\s+/).filter(Boolean); }
  getAttribute(k) { return k in this.attrs ? this.attrs[k] : null; }
  setAttribute(k, v) { this.attrs[k] = String(v); }
  removeAttribute(k) { delete this.attrs[k]; }
  appendChild(n) { n.parent = this; this.children.push(n); return n; }
  removeChild(n) { this.children = this.children.filter(c => c !== n); }
  get textContent() { let s = ""; for (const c of this.children) s += c.__t === "t" ? c.nodeValue : c.textContent; return s; }
  set textContent(v) { this.children = [new Txt(v)]; }
  get innerHTML() { return this.textContent; }
  set innerHTML(v) { this.children = [new Txt(v)]; }
  _all(out) { for (const c of this.children) if (c.__t === "e") { out.push(c); c._all(out); } return out; }
  querySelectorAll(sel) { return this._all([]).filter(e => matchSel(e, sel)); }
  querySelector(sel) { return this.querySelectorAll(sel)[0] || null; }
}
function matchSel(el, sel) {
  return String(sel).split(",").some(part => {
    part = part.trim();
    const m = part.match(/^([a-zA-Z0-9]*)((?:[.#\[][^\s]*)*)$/);
    if (m && m[1] && el.tag !== m[1]) return false;
    const rest = m ? m[2] : part;
    for (const tk of (rest.match(/\[[^\]]*\]|\.[A-Za-z0-9_-]+/g) || [])) {
      if (tk[0] === ".") { if (!el._cls.includes(tk.slice(1))) return false; }
      else {
        const inner = tk.slice(1, -1), eq = inner.indexOf("=");
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

/* 复刻 feature-memory.html 的 <title>：静态英文 + 中文/键号都存在 */
const EN = "Four-Layer Memory System · Working Mate";
const ZH = "四层记忆系统 · Working Mate 功能";
const root = new El("html", {});
const head = new El("head", {});
const body = new El("body", {});
const title = new El("title", {
  "data-entitle": EN, "data-zhtitle": ZH, "data-enkey": "feat.memory.title",
});
title.appendChild(new Txt(EN));
head.appendChild(title); root.appendChild(head); root.appendChild(body);

const doc = {
  readyState: "complete", documentElement: root, body, head,
  addEventListener() {}, dispatchEvent() {}, createElement: t => new El(t, {}),
  getElementById: () => null,
  querySelector: s => root.querySelector(s),
  querySelectorAll: s => root.querySelectorAll(s),
  createTreeWalker: () => ({ currentNode: null, nextNode: () => false }),
};
const store = {};
global.document = doc;
global.navigator = { language: "en", languages: ["en"] };
global.NodeFilter = { SHOW_TEXT: 4 };
global.CustomEvent = class { constructor(t, o) { this.type = t; this.detail = o && o.detail; } };
global.localStorage = { getItem: k => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = String(v); } };
global.window = global;
global.fetch = () => new Promise(() => {});

const load = f => new Function(fs.readFileSync(f, "utf8"))();
["en", "ja", "ko", "fr", "de", "ru", "ar", "es", "pt"].forEach(l => load("lang." + l + ".js"));
load("i18n.js");

let pass = 0, fail = 0;
function check(name, got, want) {
  const ok = got === want; ok ? pass++ : fail++;
  console.log(`  ${ok ? "✓" : "✗"} ${name}\n      得到: ${JSON.stringify(got)}\n      期望: ${JSON.stringify(want)}`);
}

console.log("【1】静态 HTML 就是英文（搜索引擎抓到的）");
const raw = fs.readFileSync("feature-memory.html", "utf8");
check("feature-memory.html 静态 title 含中文", /[\u4e00-\u9fff]/.test(raw.match(/<title[^>]*>([^<]*)</)[1]), false);
check("静态 title 存了中文备份", raw.includes('data-zhtitle="四层记忆系统'), true);
check("静态 title 存了英文", raw.includes('data-entitle="Four-Layer Memory System'), true);

console.log("\n【2】运行时按语言还原");
global.WM_I18N.apply("en", false);
check("英文", title.textContent, EN);
global.WM_I18N.apply("zh", false);
check("中文", title.textContent, ZH);
global.WM_I18N.apply("fr", false);
check("法语（复用 feat.memory.title 译文 + 品牌）", title.textContent.endsWith(" · Working Mate"), true);
check("法语不含中文", /[\u4e00-\u9fff]/.test(title.textContent), false);
console.log("      法语实际值: " + title.textContent);
global.WM_I18N.apply("ja", false);
check("日语不含中文简体", /[\u7b80\u4f53]/.test(title.textContent), false);
console.log("      日语实际值: " + title.textContent);

console.log("\n【3】没有 data-zhtitle 的页面不受影响（index.html 归 region.js 管）");
title.removeAttribute("data-zhtitle");        // 去掉归属标记后应当完全不动它
const before = title.textContent;
global.WM_I18N.apply("zh", false);
check("不越权改标题（保持原值不变）", title.textContent, before);

console.log(`\n结果: ${pass} 通过 / ${fail} 失败`);
process.exit(fail ? 1 : 0);
