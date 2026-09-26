/* ════════════════════════════════════════════════════════════
   Working Mate — 下载按钮接管（2026-09-27）
   问题：首页/定价页的下载按钮原来是 href="#" 占位，点了没反应。
   做法：静态 href 兜底指向 GitHub Releases 最新版页面（永不 404），
        再读 version.json 把 href 换成**精确的安装包直链**（与 App
        内置的自动更新走同一个 url 字段，发新版只需改 version.json）。
   用法：给下载按钮加 data-download；给版本号占位加 data-download-ver。
   ════════════════════════════════════════════════════════════ */
(function () {
  "use strict";

  var RELEASE_PAGE = "https://github.com/Frederic-123-cell/working-mate/releases/latest";

  function apply(url, ver) {
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

  function run() {
    var done = false;
    try {
      fetch("version.json", { cache: "no-store" })
        .then(function (r) { return r.json(); })
        .then(function (j) {
          if (done) return;
          done = true;
          var url = (j && j.url) ? String(j.url) : "";
          apply(url || RELEASE_PAGE, (j && j.version) ? String(j.version) : "");
        })
        .catch(function () {
          if (done) return;
          done = true;
          apply(RELEASE_PAGE, "");
        });
    } catch (e) {
      apply(RELEASE_PAGE, "");
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }

  window.WM_DOWNLOAD = { refresh: run, releasePage: RELEASE_PAGE };
})();
