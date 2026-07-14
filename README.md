# Quiet Cosmos — 个人技术博客

[![中文](https://img.shields.io/badge/README-中文-blue?style=flat-square)](README.zh-CN.md)
[![English](https://img.shields.io/badge/README-English-blue?style=flat-square)](README.en-US.md)
[![日本語](https://img.shields.io/badge/README-日本語-blue?style=flat-square)](README.ja-JP.md)

基于 **Django 6** 的个人技术博客，集成 Three.js 交互式星系背景，支持中/英/日三语界面。

---

## 功能特性

- **博客系统** — CKEditor 5 富文本编辑、分类/标签管理、语言筛选、阅读时间估算、浏览量统计
- **作品集** — Tab 分类筛选 + 卡片网格布局、项目详情弹窗、技能标签
- **评论系统** — 通用外键设计、游客/注册用户评论、楼中楼回复、后台审核
- **用户系统** — 注册/登录/密码找回、邮箱验证、个人资料编辑
- **多语言** — 中文 / English / 日本語，Django i18n 完整实现
- **交互背景** — Three.js 3D 星系粒子动画，自动适应页面场景
- **响应式** — 桌面 3 列 → 平板 2 列 → 手机 1 列
- **后台管理** — Django Admin 管理文章、评论、用户、首页内容

## 技术栈

| 类别 | 技术 |
|------|------|
| 后端 | Django 6.0 + SQLite |
| 前端 | HTML/CSS/JavaScript + Three.js |
| 编辑器 | CKEditor 5 |
| 静态文件 | WhiteNoise |
| 部署 | Gunicorn + Nginx / PythonAnywhere |
| CI/CD | GitHub Actions |
| 国际化 | Django i18n (gettext + .po/.mo) |
| 认证 | Django Auth + 自定义邮箱登录后端 |

## 快速开始

```bash
# 克隆
git clone https://github.com/EthanBAI-dev/myblog_Django.git
cd myblog_Django

# 虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py migrate

# 初始化数据（About 页面和首页内容）
python manage.py shell -c "
from blog.models import SitePage, HomePage
SitePage.objects.get_or_create(slug='about', defaults={'title': 'About', 'content': '<p>Welcome.</p>'})
HomePage.objects.get_or_create(defaults={})
"

# 收集静态文件
python manage.py collectstatic --noinput

# 编译翻译
python manage.py compilemessages

# 启动开发服务器
python manage.py runserver
```

访问 http://localhost:8000/

## 多语言维护

```bash
# 提取新文字
python manage.py makemessages -l zh-hans -l en -l ja

# 编译生效
python manage.py compilemessages
```

常见问题：
- `#, fuzzy` 标记会导致翻译不生效，需手动删除该行
- `#, python-format` 条目中 `%%` 数量需与 `msgstr` 一致
- 数据库字段值会绕过 `{% trans %}` 翻译，需清空字段或使用 JSON 多语言存储

## 部署

### PythonAnywhere

参考 [articles/deploy.md](articles/deploy.md) 中的步骤。

### GitHub Actions 自动部署

推送 `personal-website-redesign` 分支后自动触发：
1. 执行 `~/deploy-full.sh`（拉代码、迁移、编译翻译、收集静态文件）
2. 重载 Web 服务

需配置 GitHub Secrets：`PA_API_TOKEN`、`PA_USERNAME`。

## 项目结构

```
myblog/
├── myblog/               # Django 项目配置
│   ├── settings.py       # 全局配置
│   ├── urls.py           # 根路由
│   └── wsgi.py           # WSGI 入口
├── blog/                 # 博客应用（核心）
│   ├── models.py         # 数据模型
│   ├── views.py          # 视图函数
│   └── templates/blog/   # 博客模板
├── users/                # 用户应用
├── comments/             # 评论应用
├── locale/               # 多语言翻译文件
│   ├── zh_Hans/          # 中文
│   ├── en/               # 英文
│   └── ja/               # 日文
├── static/               # 静态文件
├── requirements.txt      # Python 依赖
└── .github/workflows/    # CI/CD 配置
```

## License

MIT
