/* login.html 语言行为测试 —— 用最小 DOM 桩加载真实的 region.js + lang.*.js + i18n.js
 * 复现的故障：Supabase 未配置时显示「登录即将开放」，而该块的文案既没有 i18n 挂钩、
 * boot() 又在未配置分支直接 return，导致国际访客永远看到中文。
 * 跑法：node _tests/login-i18n.test.js
 */
const fs = require("fs");

/* ─────────── 最小 DOM 桩 ─────────── */
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
  _all(out) { for (const c of this.children) if (c.__t === "e") { out.push(c); c._all(out); } return out; }
  querySelectorAll(sel) { return this._all([]).filter(e => matchSel(e, sel)); }
  querySelector(sel) { return this.querySelectorAll(sel)[0] || null; }
  closest(sel) { let n = this; while (n) { if (n.__t === "e" && matchSel(n, sel)) return n; n = n.parent; } return null; }
}
function matchSel(el, sel) {
  return String(sel).split(",").some(part => {
    part = part.trim();
    const m = part.match(/^([a-zA-Z0-9]*)((?:[.#\[][^\s]*)*)$/);
    let rest;
    if (m) { rest = m[2]; if (m[1] && el.tag !== m[1]) return false; } else rest = part;
    const tokens = rest.match(/\[[^\]]*\]|\.[A-Za-z0-9_-]+|:not\([^)]*\)/g) || [];
    for (const tk of tokens) {
      if (tk[0] === ".") { if (!el._cls.includes(tk.slice(1))) return false; }
      else if (tk === ":not(.price)") { if (el._cls.includes("price")) return false; }
      else if (tk[0] === "[") {
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
function walkText(root) { const out = []; (function go(n) { for (const c of n.children) { if (c.__t === "t") out.push(c); else go(c); } })(root); return out; }

/* ─────────── 搭出 login.html 的关键节点 ─────────── */
const root = new El("html", {});
const head = new El("head", {});
const body = new El("body", {});
root.appendChild(head); root.appendChild(body);
const el = (tag, attrs, text) => { const e = new El(tag, attrs || {}); if (text !== undefined) e.appendChild(new Txt(text)); return e; };

const title = el("title", { "data-i18n": "login.docTitle" }, "登录 / 注册 — Working Mate");
head.appendChild(title);
// 注：登录页已固定为原版包豪斯风，不再有「简约」切换按钮（见下方静态断言）

const notCfg = el("div", { id: "notConfigured" });
const soonH1 = el("h1", { "data-i18n": "login.soonTitle" }, "登录即将开放");
const soonSub = el("div", { "data-i18n-html": "login.soonSub" }, "账号系统正在最后联调…");
const soonBtn = el("a", { "data-i18n": "login.freeDownload" }, "免费下载桌面版");
notCfg.appendChild(soonH1); notCfg.appendChild(soonSub); notCfg.appendChild(soonBtn);
body.appendChild(notCfg);

const loginView = el("div", { id: "loginView" });
const lgH1 = el("h1", { "data-i18n": "login.h1" }, "登录 / 注册");
const lgSub = el("div", { "data-i18n": "login.sub" }, "无需密码。");
const orText = el("span", { "data-i18n": "login.or" }, "或");
const lbEmail = el("label", { "data-i18n": "login.email" }, "邮箱地址");
const codeInput = el("input", { "data-i18n-attr": "placeholder:login.phCode", placeholder: "6 位数字验证码" });
loginView.appendChild(lgH1); loginView.appendChild(lgSub); loginView.appendChild(orText);
loginView.appendChild(lbEmail); loginView.appendChild(codeInput);
body.appendChild(loginView);

const logoutBtn = el("button", { "data-i18n": "login.logout" }, "退出登录");
body.appendChild(logoutBtn);
const backLink = el("a", { "data-i18n": "login.backHome" }, "← 返回官网");
body.appendChild(backLink);

const doc = {
  readyState: "complete",
  documentElement: root,
  body, head,
  addEventListener() {}, dispatchEvent() {},
  createElement: t => new El(t, {}),
  getElementById(id) { return root._all([]).concat([root]).find(e => e.getAttribute("id") === id) || null; },
  querySelector: s => root.querySelector(s),
  querySelectorAll: s => root.querySelectorAll(s),
  createTreeWalker(r) {
    const nodes = walkText(r); let i = 0;
    const w = { currentNode: null, nextNode() { if (i < nodes.length) { w.currentNode = nodes[i++]; return w.currentNode; } return false; } };
    return w;
  },
};

/* ─────────── 环境 ─────────── */
const store = {};
global.document = doc;
global.navigator = { language: "en", languages: ["en"] };
global.NodeFilter = { SHOW_TEXT: 4 };
global.CustomEvent = class { constructor(t, o) { this.type = t; this.detail = o && o.detail; } };
global.location = { href: "https://workingmateapp.com/login.html", origin: "https://workingmateapp.com" };
global.fetch = () => new Promise(() => {});
global.localStorage = { getItem: k => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = String(v); } };
global.window = global;

const load = f => new Function(fs.readFileSync(f, "utf8"))();

/* ─────────── 复现真实加载顺序 ─────────── */
load("region.js");                       // 先定地区（真实顺序：region.js 在 i18n.js 之前）
["en", "ja", "ko", "fr", "de", "ru", "ar", "es", "pt"].forEach(l => load("lang." + l + ".js"));
load("i18n.js");                         // 再应用语言

/* ─────────── 断言 ─────────── */
let pass = 0, fail = 0;
function check(name, got, want) {
  const ok = got === want;
  ok ? pass++ : fail++;
  console.log(`  ${ok ? "✓" : "✗"} ${name}\n      得到: ${JSON.stringify(got)}  期望: ${JSON.stringify(want)}`);
}

console.log("【场景 0】静态守卫：单一风格 + 下载链路无第三方托管站");
{
  const loginSrc = fs.readFileSync("login.html", "utf8");
  check("登录页不再加载 minimal.js（只保留原版包豪斯风）", /minimal\.js/.test(loginSrc), false);
  check("登录页没有「简约」切换按钮", /modeToggle/.test(loginSrc), false);
  check("登录页已加 Facebook 图标", /facebook: '<svg/.test(loginSrc), true);
  const dlSrc = fs.readFileSync("download.js", "utf8");
  const idxSrc = fs.readFileSync("index.html", "utf8");
  check("download.js 兜底不再指向 GitHub", /github\.com/.test(dlSrc), false);
  check("index.html 下载按钮不再指向 GitHub", /github\.com\/Frederic/.test(idxSrc), false);
}

console.log("\n【场景 1】海外访客（未配置 Supabase，页面显示「即将开放」屏）");
global.WM_REGION.apply("OVERSEAS");
check("浏览器标题", title.textContent, "Sign in / Sign up — Working Mate");
check("大标题(截图那行)", soonH1.textContent, "Sign-in is opening soon");
check("说明文字", soonSub.textContent.slice(0, 21), "The account system is");
check("按钮", soonBtn.textContent, "Free download");
check("页脚返回", backLink.textContent, "← Back to site");
check("登录表单大标题", lgH1.textContent, "Sign in / Sign up");
check("输入框占位符(属性)", codeInput.getAttribute("placeholder"), "6-digit code");
check("退出按钮", logoutBtn.textContent, "Sign out");

console.log("\n【场景 2】大陆访客 → 全中文");
global.WM_I18N.apply("zh", false);
check("大标题", soonH1.textContent, "登录即将开放");
check("按钮", soonBtn.textContent, "免费下载桌面版");
check("登录表单大标题", lgH1.textContent, "登录 / 注册");

console.log("\n【场景 3】海外访客手动选法语 → 全法语（不是中文也不是英文）");
global.WM_I18N.apply("fr", false);
check("大标题", soonH1.textContent, "La connexion arrive bientôt");
check("按钮", soonBtn.textContent, "Téléchargement gratuit");
check("页脚返回", backLink.textContent, "← Retour au site");
check("登录表单大标题", lgH1.textContent, "Connexion / Inscription");

console.log("\n【场景 4】10 种语言逐一检查「即将开放」大标题都不含中文");
const seen = {};
for (const l of ["en", "ja", "ko", "fr", "de", "ru", "ar", "es", "pt"]) {
  global.WM_I18N.apply(l, false);
  seen[l] = soonH1.textContent;
}
const anyCJK = Object.keys(seen).filter(l => /[\u4e00-\u9fff]/.test(seen[l]));
check("含中文的语言数（应为 0，ja 的「近日公開」是日文汉字不算）", anyCJK.filter(l => l !== "ja").length, 0);
Object.keys(seen).forEach(l => console.log(`      ${l}: ${seen[l]}`));

console.log(`\n结果: ${pass} 通过 / ${fail} 失败`);
process.exit(fail ? 1 : 0);
