# Zenith AI 研学社 · 官网

> 向下扎根，向上破界。务实落地，长期主义。山顶见。

## 技术栈

纯静态站点（HTML + CSS + 原生 JS），零依赖、零构建，浏览器直接打开就能看。

```
官网/
├── index.html        # 单页长站（Hero + 5 区块）
├── 404.html          # 品牌化 404 页（GitHub Pages 自动启用）
├── css/style.css     # 淡紫品牌色 × 深夜山顶意象
├── js/main.js        # 交互：导航/滚动显现/打字机金句/四个小工具
├── assets/og-cover.png   # 社交分享封面（1200x630）
├── tools/            # make_og_cover.py 生成分享图；check_site.py 一键自检
├── robots.txt        # 收录声明
├── sitemap.xml       # 站点地图
├── vercel.json       # 备选：Vercel 部署配置
├── netlify.toml      # 备选：Netlify 部署配置
└── 01-设计案-v1.md   # 设计文档（需求/审美/建模/架构）
```

## 本地预览

任选一种：

```bash
# 方式 1：Python
python -m http.server 8080 --directory 官网
# 然后浏览器打开 http://localhost:8080

# 方式 2：Node
npx serve 官网
```

## 部署到 GitHub Pages（推荐，先内测）

1. 新建 GitHub 仓库，把本目录内容推上去（建议仓库名 `zenith-website`，或按组织命名）
2. 仓库 Settings → Pages → Source 选 `Deploy from a branch`，分支 `main`，目录 `/`（root）
3. 保存后等 1-2 分钟，访问 `https://<用户名>.github.io/<仓库名>/`
4. 之后每次 `git push` 自动重新部署

### 绑定自定义域名（可选）

- 买域名后，在仓库 Pages 设置里填自定义域名
- 去域名服务商加 CNAME 记录指向 `<用户名>.github.io`
- 在仓库根目录放一个 `CNAME` 文件（内容为域名，如 `zenith.example.com`），推送即可

## 部署到 Vercel / Netlify（备选，国内访问一般）

- **Vercel**：vercel.com → New Project → 导入 GitHub 仓库 → Framework Preset 选 `Other` → Deploy（已带 `vercel.json`）
- **Netlify**：app.netlify.com → Add new site → Import from Git → Build command 留空，Publish directory 填 `.`（已带 `netlify.toml`）

## 国内正式上线（后续考虑）

国内访问稳定需要备案，路径：域名备案 → 对象存储（腾讯云 COS / 阿里云 OSS）静态网站托管 + CDN。
站点是纯静态，直接传文件即可，无服务器成本。

## 上线前待补（占位清单）

- [ ] 内容板块：公众号文章真实链接（认知革命系列 5 篇 URL）
- [ ] 社群入口：公众号二维码图（放「关注我们」卡片，现在是文字引导）
- [x] 接客邮箱：`zenith0097@163.com`（已填）
- [ ] 平台矩阵：抖音 / 视频号 主页链接（现在是纯文字，点不动）
- [ ] 金句墙与系列标题：以最终发布内容为准校对

## 设计依据

按 [[01-设计案-v1]] 出牌：需求牌（用户分层 A/B/C/D）→ 审美牌（最佳实践池子 + 8 维评价模型）→ 信息架构（8 区块，三种出口：关注/进群/咨询）。
