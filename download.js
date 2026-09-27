/* ════════════════════════════════════════════════════════════
   Working Mate — 下载按钮接管
   策略（2026-09-27 改版）：
     · 下载链路**绝不出现第三方代码托管站**（Creem 合规要求）。
       历史版本曾把兜底地址写成 GitHub Releases 页面，已废弃。
     · 静态 href 兜底写在 HTML 里，指向本站 #download 锚点
       （无 JS / JS 出错时也停在自己域名内）。
     · 运行时读 version.json 的 url 字段，换成安装包直链
       （与 App 内置自动更新共用同一个 url，发新版只改 version.json）。
   用法：下载按钮加 data-download；版本号占位加 data-download-ver。
   ════════════════════════════════════════════════════════════ */
(function () {
  "use strict";

  // 兜底：留在本站（不再指外部托管页）
  var FALLBACK = "#download";

  function finalize(url, ver) {
    var a = document.querySelectorAll("[data-download]");
    for (var i = 0; i < a.length; i++) {
      a[i].setAttribute("href", url);
      a[i].setAttribute("rel", "noopener");
    }
    var v = document.querySelectorAll("[data-download-ver]");
    for (var j = 0; j < v.length; j++) {
      if (ver) v[j].textContent = ver;
    }
  }

  function apply(url, ver) {
    if (!url) { finalize(FALLBACK, ver); return; }
    var crossOrigin = /^https?:\/\//i.test(url) && url.indexOf(location.origin) !== 0;
    if (!crossOrigin || !window.fetch) {
      // 本站域名（或相对路径）：直接信任，不做探测（避免多一次往返）
      finalize(url, ver);
      return;
    }
    // 外部托管：探一下是否真的存在，明确 404 时才回退
    fetch(url, { method: "HEAD", cache: "no-store" })
      .then(function (r) { finalize(r.ok ? url : FALLBACK, ver); })
      .catch(function () { finalize(url, ver); });   // 探测被 CORS/网络挡住时按原样用
  }

  function run() {
    var done = false;
    try {
      fetch("version.json", { cache: "no-store" })
        .then(function (r) { return r.json(); })
        .then(function (j) {
          if (done) return;
          done = true;
          apply((j && j.url) ? String(j.url) : "", (j && j.version) ? String(j.version) : "");
        })
        .catch(function () {
          if (done) return;
          done = true;
          apply("", "");
        });
    } catch (e) {
      apply("", "");
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }

  window.WM_DOWNLOAD = { refresh: run, fallback: FALLBACK };
})();
