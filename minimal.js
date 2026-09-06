/* ============================================================
   Working Mate — Minimal Mode toggle
   与 theme.js 同级：放在 </head> 前同步执行，避免先普通后律动的闪烁。
   开关写在 <html data-mode="minimal">，偏好存 localStorage('wm-mode')。
   ============================================================ */
(function () {
    'use strict';

    var KEY = 'wm-mode';
    var root = document.documentElement;

    // ── 1. 立刻定状态（body 渲染前，防闪烁） ──
    var saved = null;
    try { saved = localStorage.getItem(KEY); } catch (e) {}
    if (saved === 'minimal') {
        root.setAttribute('data-mode', 'minimal');
    }

    // ── 2. 同步按钮视觉 ──
    function apply(btn) {
        if (!btn) return;
        var on = root.getAttribute('data-mode') === 'minimal';
        btn.setAttribute('aria-pressed', on ? 'true' : 'false');
        btn.setAttribute('aria-label', on ? 'Exit minimal mode' : 'Minimal mode');
        btn.setAttribute('title', on ? 'Exit minimal mode' : 'Minimal mode');
    }

    // ── 3. 绑定点击 ──
    function bind() {
        var btn = document.getElementById('modeToggle');
        if (!btn) return;
        apply(btn);
        btn.addEventListener('click', function () {
            var on = root.getAttribute('data-mode') === 'minimal';
            if (on) {
                root.removeAttribute('data-mode');
                try { localStorage.setItem(KEY, 'normal'); } catch (e) {}
            } else {
                root.setAttribute('data-mode', 'minimal');
                try { localStorage.setItem(KEY, 'minimal'); } catch (e) {}
            }
            apply(btn);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bind);
    } else {
        bind();
    }
})();
