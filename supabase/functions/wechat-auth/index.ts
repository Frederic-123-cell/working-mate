// ════════════════════════════════════════════════════════════════
//  Supabase Edge Function: 微信扫码登录
//  Supabase 没有内置微信 provider，这里用「微信开放平台网站应用」的
//  OAuth(code → openid) + Admin API 自建账号，再签发 magiclink 回跳。
//
//  部署： supabase secrets set WECHAT_APPID=xxx WECHAT_SECRET=xxx
//         supabase functions deploy wechat-auth
//  前提： 微信开放平台(https://open.weixin.qq.com) 已创建「网站应用」，
//         且 授权回调域名 填了你的域名（不含 https://）。
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const APPID = Deno.env.get("WECHAT_APPID") ?? "";
const SECRET = Deno.env.get("WECHAT_SECRET") ?? "";
const SUPABASE_URL = Deno.env.get("SUPABASE_URL") ?? "";
const SERVICE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "";

function redirect(to: string) {
  return new Response(null, { status: 302, headers: { Location: to } });
}

Deno.serve(async (req: Request) => {
  const url = new URL(req.url);
  const back = url.searchParams.get("redirect") || "/index.html";
  const code = url.searchParams.get("code");

  // ── 第一步：没有 code → 跳微信扫码授权页 ──
  if (!code) {
    if (!APPID) return new Response("WECHAT_APPID not set", { status: 500 });
    const cb = encodeURIComponent(
      `${url.origin}/functions/v1/wechat-auth?redirect=${encodeURIComponent(back)}`
    );
    const wx =
      `https://open.weixin.qq.com/connect/qrconnect` +
      `?appid=${APPID}&redirect_uri=${cb}&response_type=code` +
      `&scope=snsapi_login&state=wm#wechat_redirect`;
    return redirect(wx);
  }

  // ── 第二步：code → openid ──
  const r = await fetch(
    `https://api.weixin.qq.com/sns/oauth2/access_token` +
    `?appid=${APPID}&secret=${SECRET}&code=${code}&grant_type=authorization_code`
  );
  const tok = await r.json();
  if (!tok.openid) {
    return new Response("微信授权失败: " + JSON.stringify(tok), { status: 400 });
  }

  const admin = createClient(SUPABASE_URL, SERVICE_KEY, {
    auth: { persistSession: false, autoRefreshToken: false },
  });

  // ── 第三步：查映射 → 没有就建号 ──
  const { data: exist } = await admin
    .from("wechat_identities")
    .select("user_id")
    .eq("openid", tok.openid)
    .maybeSingle();

  let userId: string | undefined = exist?.user_id;

  if (!userId) {
    const email = `${tok.openid}@wechat.local`;   // 占位邮箱，微信不提供真实邮箱
    const { data: created, error } = await admin.auth.admin.createUser({
      email,
      email_confirm: true,
      user_metadata: { provider: "wechat", openid: tok.openid },
    });
    if (error && !created?.user) {
      return new Response("建号失败: " + error.message, { status: 500 });
    }
    userId = created!.user!.id;
    await admin.from("wechat_identities").insert({
      openid: tok.openid, user_id: userId, nickname: tok.nickname ?? null,
    });
  }

  // ── 第四步：签发一次性登录链接，回跳站点（由 auth-callback.html 收尾）──
  const { data: link, error: lerr } = await admin.auth.admin.generateLink({
    type: "magiclink",
    email: `${tok.openid}@wechat.local`,
    options: { redirectTo: `${new URL(back, url.origin).origin}/auth-callback.html?next=${encodeURIComponent(back)}` },
  });
  if (lerr || !link?.properties?.action_link) {
    return new Response("签发登录链接失败: " + (lerr?.message ?? "unknown"), { status: 500 });
  }
  return redirect(link.properties.action_link);
});
