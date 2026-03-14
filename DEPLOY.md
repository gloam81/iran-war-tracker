# 部署指南

## 快速开始

### 1. 创建 GitHub 仓库

1. 在 GitHub 上创建新仓库（例如 `iran-war-tracker`）
2. 不要初始化 README、.gitignore 或 license

### 2. 上传代码

将本项目的所有文件推送到 GitHub 仓库：

```bash
cd iran-war-tracker
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/iran-war-tracker.git
git push -u origin main
```

### 3. 启用 GitHub Pages

1. 进入仓库 Settings → Pages
2. 在 "Source" 选择 `Deploy from a branch`
3. Branch 选择 `gh-pages`，文件夹选择 `/ (root)`
4. 点击 Save

GitHub 会自动创建 `gh-pages` 分支并部署。

### 4. 配置 GitHub Actions（可选，用于自动更新）

如果你想每天自动更新新闻：

1. 在仓库 Settings → Secrets and variables → Actions 中，添加：
   - `NEWS_API_KEY`：（可选）从 [NewsAPI.org](https://newsapi.org) 获取免费 API key

2. GitHub Actions 工作流已配置，会自动运行：
   - 每天 UTC 00:00 自动收集新闻并更新 `data.js`
   - 通过 `workflow_dispatch` 可以手动触发
   - 更新后自动部署到 GitHub Pages

3. 首次运行后，GitHub Pages 会自动更新

### 5. 访问网站

等待几分钟，访问：`https://YOUR_USERNAME.github.io/iran-war-tracker/`

## 自定义

### 修改数据源

编辑 `collector.py` 文件中的 `RSS_FEEDS` 和 `SEARCH_KEYWORDS` 变量，添加或删除新闻源。

### 添加翻译

项目目前使用中英双语。如需翻译成其他语言，可在 `translations` 对象中添加。

### 样式调整

修改 `styles.css` 文件来自定义外观。

## 技术说明

- **前端：** 纯 HTML/CSS/JavaScript，Leaflet 地图
- **数据：** 由 Python 脚本从 RSS/NewsAPI 收集
- **部署：** GitHub Pages（免费）
- **自动化：** GitHub Actions

## 成本

- **完全免费**（使用 GitHub Pages 和免费 API）
- NewsAPI 免费版每月 100 次请求，足够个人使用

## 注意事项

- 内容来源于公开媒体，仅供参考
- 自动翻译可能不完美，建议人工校对重要内容
- 遵守各新闻源的使用条款
- 避免频繁请求，遵守 API 限制

## 故障排除

1. **GitHub Pages 显示 404**
   - 检查 Pages 设置是否正确
   - 等待 1-2 分钟让 GitHub 构建

2. **数据不更新**
   - 检查 Actions 日志
   - 确保 NEWS_API_KEY 正确设置（如使用）

3. **样式异常**
   - 确保所有文件在同一目录
   - 检查浏览器控制台错误

## 高级配置

如需更多功能（如更多数据源、复杂翻译、数据库存储），可以考虑：

- 使用 Python Anywhere 或 Railway 运行收集器
- 添加 Supabase 或 Firebase 作为数据库
- 使用 Cloudflare Workers 做代理和缓存
- 集成 Google Translate API 或 DeepL API 获得更好翻译

需要帮助？请提交 Issue。