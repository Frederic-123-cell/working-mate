/* ════════════════════════════════════════════════════════════════
   Working Mate — 站点配置（登录 / 支付 / 下载的唯一配置入口）

   ⚠ 上线前必须填的两项：supabase.url 与 supabase.anonKey
     Supabase 后台 → Project Settings → API：
       Project URL  → 填进 supabase.url
       anon public  → 填进 supabase.anonKey（这个 key 本来就是公开的，
                      安全靠的是 RLS 行级策略，不是靠藏 key）
   两项留空 → login.html 自动显示「登录即将开放」，不会报错。
   ════════════════════════════════════════════════════════════════ */
window.WM_CONFIG = {
  /* ── Supabase（身份 + 数据库）── */
  supabase: {
    url: "",                                   // 例: "https://abcdefgh.supabase.co"
    anonKey: ""                                // 例: "eyJhbGciOi..."
  },

  /* ── 按地区展示的登录方式（region.js 会写入 data-region）──
     海外: Google / Apple / 邮箱 / GitHub
     大陆: 手机号+验证码 / 微信（邮箱作为备选小字入口）           */
  providers: {
    CN:       ["phone", "wechat", "email"],
    OVERSEAS: ["google", "apple", "email", "github"]
  },
  defaultProviders: ["email", "google", "github"],   // 地区判定失败时的兜底

  /* ── 微信登录 ──
     Supabase 没有内置微信 provider，走 Edge Function：
       1) 微信开放平台（网站应用）拿 appid + secret
       2) 部署 supabase/functions/wechat-auth（见该文件）
       3) 把 Function URL 填到下面                               */
  wechat: {
    appId: "",                                 // 例: "wx1234567890abcdef"
    authFunctionUrl: ""                        // 例: "https://xxx.supabase.co/functions/v1/wechat-auth"
  },

  /* ── OAuth 回调 ──
     必须在 Supabase 后台 Authentication → URL Configuration 里
     把这些地址加进 Redirect URLs，否则登录后会跳不回来。          */
  redirectAfterLogin: "index.html",

  /* ── 新用户赠送积分（与 credits.py 的 newbie_gift_credits 对齐）── */
  welcomeCredits: 3000
};

/* 是否已配置（login.html 用它决定显示登录表单还是「即将开放」） */
window.WM_AUTH_READY = (function () {
  var c = window.WM_CONFIG && window.WM_CONFIG.supabase;
  return !!(c && c.url && c.anonKey &&
            c.url.indexOf("YOUR-PROJECT") < 0 && c.anonKey.indexOf("YOUR-ANON") < 0);
})();
