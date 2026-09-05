# 迁到 GitHub Pages — 操作说明

> 目的：解决 Creem 第 7 条「production-ready custom domain」。
> 现在站点挂在 `688bc...app.workbuddy.link`（WorkBuddy 沙箱临时子域），Creem 必拒。
> 迁到 GitHub Pages 后站点变成 `https://frederic-123-cell.github.io/working-mate/`，Creem 认可。

---

## 架构（为什么这么分）

| 内容 | 放哪 | 为什么 |
|---|---|---|
| 网站 HTML/CSS/JS（377 KB） | **GitHub Pages** | 小，Pages 擅长这个 |
| 240MB 安装包 | **GitHub Releases** | git 单文件硬上限 100MB，塞不进仓库；Releases 单文件上限 2GB |

- 站点地址：`https://frederic-123-cell.github.io/working-mate/`
- 下载直链：`https://github.com/Frederic-123-cell/working-mate/releases/download/v1.2.6/AIAgent-Setup-1.2.6.exe`
- 额外好处：Releases 走 GitHub CDN，**不消耗 Pages 的 100GB/月流量**

---

## 四步操作

### 第 1 步：在 GitHub 建空仓库

打开 https://github.com/new

| 项 | 填什么 |
|---|---|
| Repository name | `working-mate` |
| Visibility | **Public**（免费版 Pages 必须公开） |
| Add a README / .gitignore / license | **全部不要勾**（保持空仓库） |

点 **Create repository**。

### 第 2 步：双击 `deploy-github.bat`

就在 `website-v2/` 目录里。它会：

1. 检查能不能连上你刚建的仓库（连不上会提示你先去建）
2. `git init`
3. 设远端
4. `git add`（240MB 安装包已被 `.gitignore` 排除）
5. commit
6. push

跑完显示 `SUCCESS` 就 OK 了。

> 如果 push 报权限错误：打开一次 **GitHub Desktop** 登录你的账号，再跑一次脚本。

### 第 3 步：开 Pages

打开：https://github.com/Frederic-123-cell/working-mate/settings/pages

| 项 | 选什么 |
|---|---|
| Source | **Deploy from a branch** |
| Branch | `main` + `/root` |

点 **Save**，等约 1 分钟，然后访问：

**https://frederic-123-cell.github.io/working-mate/**

### 第 4 步：上传安装包到 Releases

打开：https://github.com/Frederic-123-cell/working-mate/releases/new

| 项 | 填什么 |
|---|---|
| Tag version | `v1.2.6` |
| Release title | `Working Mate v1.2.6` |
| 附件 | 拖入 `downloads\AIAgent-Setup-1.2.6.exe`（240MB，上传要几分钟） |

点 **Publish release**。

验证下载直链能通（浏览器打开应该开始下载 exe）：

```
https://github.com/Frederic-123-cell/working-mate/releases/download/v1.2.6/AIAgent-Setup-1.2.6.exe
```

---

## 已完成的代码改动（我这边做好的）

### 官网（`website-v2/`）

| 文件 | 改动 |
|---|---|
| `acceptable-use.html` | **新建** — Creem 第 9 条（AI 产品必须有使用规范） |
| `index.html` | footer 加客服邮箱 + AUP 链接；i18n 加 `ft_aup` |
| `privacy.html` | Paddle→Creem；第三方服务加七牛云/可灵/302.ai；footer 加 AUP+邮箱 |
| `terms.html` | Paddle→Creem；footer 加 AUP+邮箱 |
| `refunds.html` | Paddle→Creem；footer 加 AUP+邮箱 |
| `pricing.html` | FAQ 的 merchant of record 指 Creem；footer 加 AUP+邮箱 |
| `version.json` | url 指向 GitHub Releases 直链 |
| `.gitignore` | **新建** — 排除 240MB exe / bak / 本地脚本 |
| `.nojekyll` | **新建** — 禁用 Jekyll 处理 |
| `deploy-github.bat` | **新建** — 本文件配套的部署脚本 |

客服邮箱统一为：`wanjunjie13341418310@outlook.com`

### 桌面端（`local-agent/`）— 三处内置默认 URL

| 文件:行 | 变量 | 新值 |
|---|---|---|
| `updater.py:33` | `UPDATE_CHECK_URL` | `https://frederic-123-cell.github.io/working-mate/version.json` |
| `billing.py:24` | `PAYMENT_URL` | `https://frederic-123-cell.github.io/working-mate/pricing.html` |
| `main.py:682` | `DEFAULT_SUPPORT_URL` | `https://frederic-123-cell.github.io/working-mate/` |

> 这三处都是 `configured_endpoint()` 包装过的 —— **老用户不用重新打包**，
> 在 `data/config.json` 里配 `update_check_url` / `payment_url` / `support_url` 就能覆盖。
> 只有新装机的用户才会用到内置默认值（所以下次打包时带上这些改动即可）。

---

## ⚠️ 待办 / 已知问题

1. **版本号对不上**：`local-agent/updater.py:30` 的 `APP_VERSION` 已经是 **1.3.0**，
   但线上 `version.json` 还是 **1.2.6**。这意味着本地 1.3.0 的包去检查更新，
   发现服务器版本更低 → **不会触发更新**。要么把 version.json 升到 1.3.0，
   要么把 APP_VERSION 降回 1.2.6，二选一。

2. **购买按钮还是死链**：`pricing.html` 里 Standard / Pro 的按钮是
   `href="#checkout-standard"` / `"#checkout-pro"`，等你从 Creem 后台拿到真实
   checkout URL 后替换。（这次 Creem 的 9 条里没提，但购买流实际跑不通。）

3. **以后想绑自己的域名**：在 `website-v2/` 里放一个 `CNAME` 文件，内容写你的域名
   （如 `www.workingmate.app`），然后在域名服务商那里加一条 CNAME 记录指向
   `frederic-123-cell.github.io`。GitHub 会自动签发 HTTPS 证书。

4. **七牛云账单暂停**：`AIAgent部署交接文档.md` 第 6 节提到账号处于
   `account_billing_suspended`，对话/生图/生视频会 403。这个跟官网无关，
   但影响用户装完软件后的实际体验。

---

## 2026-09-05 增量改动（本次 push 自动包含）

| 改动 | 说明 |
|---|---|
| 首页真实截图墙 | `assets/shots/` 12 张英文界面截图（1.5MB，进 git），替换原假 chat 模型 |
| 功能卡 8 → 11 张 | 新增：技能库与工作流设计器 / 定时自动化任务 / 10 种界面语言 |
| "and more / 等"文案 | 13 处清零，全部展开为完整列举（Creem 对营销文案的规范性要求） |
| 下载按钮 | 已改为 GitHub Releases 直链（`releases/download/v1.2.6/...`）——**必须先完成上面第 4 步上传 Release，下载按钮才会真正可用** |
| Creem 审核项自查 | Privacy / Terms / Refunds / Acceptable Use 链接 ✓、support email ✓、下载直链 ✓ |

**推荐执行顺序**：第 1 步建仓 → 第 2 步 push（截图墙上线）→ 第 3 步开 Pages → 第 4 步传 Release（下载按钮激活）→ 浏览器验证站点 + 下载直链 → Creem 重新提交审核。
