-- ════════════════════════════════════════════════════════════════
--   Working Mate 账号体系（Supabase / Postgres）
--   在 Supabase 后台 → SQL Editor 整段粘贴执行即可（可重复执行）。
-- ════════════════════════════════════════════════════════════════

-- ── 用户资料（与 auth.users 一对一）──
create table if not exists public.profiles (
  id           uuid primary key references auth.users(id) on delete cascade,
  email        text,
  phone        text,
  provider     text,
  display_name text,
  avatar_url   text,
  region       text,
  created_at   timestamptz not null default now()
);
alter table public.profiles enable row level security;
drop policy if exists "own profile read"   on public.profiles;
create policy "own profile read"   on public.profiles for select using (auth.uid() = id);
drop policy if exists "own profile update" on public.profiles;
create policy "own profile update" on public.profiles for update using (auth.uid() = id);

-- ── 权益：会员档位 / 到期 / 积分余额（服务端权威，客户端只读）──
create table if not exists public.entitlements (
  user_id              uuid primary key references auth.users(id) on delete cascade,
  tier                 text not null default 'free',
  subscription_expires timestamptz,
  credits_balance      numeric(14,2) not null default 0,
  welcome_granted      boolean not null default false,
  updated_at           timestamptz not null default now()
);
alter table public.entitlements enable row level security;
drop policy if exists "own entitlement read" on public.entitlements;
create policy "own entitlement read" on public.entitlements
  for select using (auth.uid() = user_id);
-- 写入只允许 service_role（Creem 支付 webhook / 后端），客户端无写权限

-- ── 积分流水 ──
create table if not exists public.credit_ledger (
  id         bigserial primary key,
  user_id    uuid not null references auth.users(id) on delete cascade,
  delta      numeric(14,2) not null,
  reason     text,
  model_id   text,
  created_at timestamptz not null default now()
);
alter table public.credit_ledger enable row level security;
drop policy if exists "own ledger read" on public.credit_ledger;
create policy "own ledger read" on public.credit_ledger
  for select using (auth.uid() = user_id);

-- ── 微信 openid ↔ 用户映射（微信登录用；微信不提供邮箱）──
create table if not exists public.wechat_identities (
  openid     text primary key,
  user_id    uuid not null references auth.users(id) on delete cascade,
  nickname   text,
  created_at timestamptz not null default now()
);
alter table public.wechat_identities enable row level security;
-- 仅 service_role 可读写（不开放给客户端）

-- ── 新用户自动建档 + 赠送 3000 积分 ──
-- 与 credits.py 的 newbie_gift_credits = 3000 对齐
create or replace function public.handle_new_user()
returns trigger
language plpgsql security definer set search_path = public
as $$
begin
  insert into public.profiles (id, email, phone, provider)
  values (
    new.id, new.email, new.phone,
    coalesce(
      new.raw_app_meta_data->>'provider',
      new.identities->0->>'provider',
      'email'
    )
  )
  on conflict (id) do nothing;

  insert into public.entitlements (user_id, tier, credits_balance, welcome_granted)
  values (new.id, 'free', 3000, true)
  on conflict (user_id) do nothing;

  return new;
end $$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();
