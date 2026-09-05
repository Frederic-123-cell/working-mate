/* ============================================================
   Working Mate — Theme Switcher
   包豪斯双主题：light (奶油纸) / dark (墨黑)

   放在 <head> 里同步执行，避免页面先亮后暗的闪烁 (FOUC)。
   ============================================================ */
(function () {
    'use strict';

    var STORAGE_KEY = 'wm-theme';
    var root = document.documentElement;

    // ── 1. 立刻定主题（在 body 渲染前，防闪烁） ──
    var saved = null;
    try {
        saved = localStorage.getItem(STORAGE_KEY);
    } catch (e) {
        // 隐私模式下 localStorage 可能抛错，忽略即可
    }

    if (saved !== 'light' && saved !== 'dark') {
        // 没存过 → 跟随系统
        saved = (window.matchMedia &&
                 window.matchMedia('(prefers-color-scheme: dark)').matches)
                ? 'dark' : 'light';
    }
    root.setAttribute('data-theme', saved);

    // ── 2. 绑定切换按钮 ──
    function applyLabel(btn, theme) {
        btn.setAttribute('aria-label',
            theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
        btn.setAttribute('title',
            theme === 'dark' ? 'Light mode' : 'Dark mode');
    }

    function bind() {
        var btn = document.getElementById('themeToggle');
        if (!btn) return;

        applyLabel(btn, root.getAttribute('data-theme'));

        btn.addEventListener('click', function () {
            var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            root.setAttribute('data-theme', next);
            try {
                localStorage.setItem(STORAGE_KEY, next);
            } catch (e) {}
            applyLabel(btn, next);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bind);
    } else {
        bind();
    }

    // ── 3. 用户没手动选过时，跟随系统变化 ──
    if (window.matchMedia) {
        var mq = window.matchMedia('(prefers-color-scheme: dark)');
        var onSystemChange = function (e) {
            var hasManual = false;
            try {
                hasManual = !!localStorage.getItem(STORAGE_KEY);
            } catch (err) {}
            if (!hasManual) {
                root.setAttribute('data-theme', e.matches ? 'dark' : 'light');
                var b = document.getElementById('themeToggle');
                if (b) applyLabel(b, e.matches ? 'dark' : 'light');
            }
        };
        if (mq.addEventListener) {
            mq.addEventListener('change', onSystemChange);
        } else if (mq.addListener) {
            mq.addListener(onSystemChange);  // 老 Safari
        }
    }
})();
