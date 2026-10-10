/* Working Mate — 面包屑导航 + BreadcrumbList 结构化数据
   目的：提高搜索引擎「站点子链 / Sitelinks」概率（页面顶部出现 首页 / 功能名，
   并向搜索引擎声明页面层级）。只对 feature-*.html 生效。 */
(function () {
  "use strict";
  var page = (window.location.pathname || "").split("/").pop() || "index.html";
  if (page.indexOf("feature") !== 0) return;   // 只挂功能页
  document.addEventListener("DOMContentLoaded", function () {
    var h1 = document.querySelector("h1");
    var name = (h1 && h1.textContent || document.title || "").trim();
    if (!name) return;
    // UI 面包屑（样式内联，不依赖主题）
    try {
      var nav = document.createElement("nav");
      nav.className = "wm-crumbs";
      nav.setAttribute("aria-label", "面包屑");
      nav.style.cssText = "max-width:1120px;margin:0 auto;padding:14px 20px 0;" +
        "font-size:12.5px;opacity:.72;text-align:left";
      nav.innerHTML = '<a href="index.html" style="color:inherit;text-decoration:underline">' +
        "\u9996\u9875</a> \u2039 " + name;
      document.body.insertBefore(nav, document.body.firstChild);
    } catch (e) {}
    // 结构化数据
    try {
      var ld = document.createElement("script");
      ld.type = "application/ld+json";
      ld.textContent = JSON.stringify({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "\u9996\u9875",
            "item": "https://workingmateapp.com/" },
          { "@type": "ListItem", "position": 2, "name": name,
            "item": "https://workingmateapp.com/" + page }
        ]
      });
      document.head.appendChild(ld);
    } catch (e) {}
  });
})();
