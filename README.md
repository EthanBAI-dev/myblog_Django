# Ethan BAI's Blog — Quiet Cosmos

---

[中文](#项目概述) · [English](#project-overview) · [日本語](#プロジェクト概要)

---

## 项目概述

一个基于 **Django 6** 构建的个人技术博客项目，融合 Three.js 交互式星系背景，支持中/英/日三语界面。包含博客文章系统、作品集展示、评论互动、用户注册登录、个人中心等完整功能。

### 核心功能

- **博客文章系统**：支持富文本编辑器（CKEditor 5）、分类/标签管理、按语言筛选、阅读时间估算、浏览量统计
- **作品集展示**：Tab 分类筛选 + 卡片网格布局，支持项目详情弹窗、技能标签展示
- **评论系统**：通用外键设计，支持游客评论和注册用户评论、楼中楼回复、后台审核
- **用户系统**：注册/登录/找回密码，邮箱验证，个人资料编辑，支持邮箱或用户名登录
- **多语言支持**：中文、English、日本語，Django i18n 完整实现
- **交互式背景**：Three.js 3D 星系粒子动画，自动适应页面场景
- **响应式设计**：桌面端 2-3 列网格 → 平板 2 列 → 手机 1 列适配
- **管理员后台**：Django Admin 界面，管理文章、评论、用户、首页内容等

### 技术栈

| 类别 | 技术 |
|------|------|
| **后端框架** | Django 6.0 + SQLite |
| **前端** | HTML/CSS/JavaScript + Three.js (3D 背景) |
| **富文本编辑器** | CKEditor 5 |
| **静态文件服务** | WhiteNoise |
| **部署** | Gunicorn + Nginx (反向代理) / PythonAnywhere |
| **CI/CD** | GitHub Actions (自动部署到 PythonAnywhere) |
| **国际化** | Django i18n (gettext + .po/.mo 文件) |
| **认证** | Django Auth + 自定义邮箱登录后端 |

### 项目结构

```
myblog/
├── myblog/                  # Django 项目配置
│   ├── settings.py          # 全局配置（数据库、静态文件、i18n 等）
│   ├── urls.py              # 根 URL 路由
│   ├── wsgi.py              # WSGI 入口（生产部署用）
│   └── asgi.py              # ASGI 入口
│
├── blog/                    # 博客应用（核心）
│   ├── models.py            # Post, Category, Tag, SitePage, HomePage
│   ├── views.py             # 首页、文章列表/详情、搜索等视图
│   ├── urls.py              # 博客 URL 路由
│   ├── admin.py             # 后台管理配置
│   ├── context_processors.py# 侧边栏全局上下文（最新文章、热门、归档）
│   ├── templatetags/        # 自定义模板标签
│   └── templates/blog/      # 博客模板（base, home, post_list, detail 等）
│
├── users/                   # 用户应用
│   ├── models.py            # UserProfile（扩展用户模型）
│   ├── views.py             # 注册/登录/个人中心/密码管理
│   ├── forms.py             # 用户表单
│   ├── urls.py              # 用户 URL 路由
│   └── templates/users/     # 用户模板（登录、注册、个人中心等）
│
├── comments/                # 评论应用
│   ├── models.py            # Comment（通用外键 + 楼中楼）
│   ├── forms.py             # 评论表单
│   └── admin.py             # 评论后台管理
│
├── locale/                  # 多语言翻译文件
│   ├── zh_Hans/LC_MESSAGES/ # 中文翻译
│   ├── en/LC_MESSAGES/      # 英文翻译
│   └── ja/LC_MESSAGES/      # 日文翻译
│
├── static/                  # 全局静态文件
│   ├── blog/css/style.css   # 主样式表
│   └── blog/images/         # 图片资源
│
├── staticfiles/             # collectstatic 输出目录
├── media/                   # 用户上传文件
├── db.sqlite3               # SQLite 数据库
│
├── requirements.txt         # Python 依赖
├── .github/workflows/       # GitHub Actions 部署配置
└── README.md                # 本文件
```

---

## 多语言维护

本项目通过 Django i18n 支持 **中文 / English / 日本語** 三语界面。

### 核心文件

- `locale/zh_Hans/LC_MESSAGES/django.po` — 中文翻译
- `locale/en/LC_MESSAGES/django.po` — 英文翻译
- `locale/ja/LC_MESSAGES/django.po` — 日文翻译

### 常用命令

```bash
# 提取新文字
python manage.py makemessages -l zh-hans
python manage.py makemessages -l en
python manage.py makemessages -l ja

# 编译生效
python manage.py compilemessages
```

### 常见陷阱

| 问题 | 解决 |
|:-----|:-----|
| 翻译不生效 | 检查是否带 `#, fuzzy` 标记，需删除该行 |
| `compilemessages` 报错 | 检查 `#, python-format` 条目中 `%%` 数量是否与 `msgstr` 一致 |
| 数据库字段跳过翻译 | 清空数据库字段值，或改用 JSON 多语言存储 |

详细规则见项目根目录 `.trae/skills/multi-lang-maintenance/SKILL.md`。

---

## 部署

### PythonAnywhere

1. 在 PA 上创建 Web App，从 GitHub 克隆项目
2. 配置虚拟环境和 WSGI 文件
3. 运行标准部署命令

详细步骤见 `articles/deploy.md`。

### GitHub Actions 自动部署

推送 `personal-website-redesign` 分支后自动触发：

1. PA 上执行 `~/deploy-full.sh`（拉代码、迁移、编译翻译、收集静态文件）
2. 重载 Web 服务

确保 GitHub Secrets 已配置 `PA_API_TOKEN` 和 `PA_USERNAME`。

---

## 本地开发环境搭建

### 环境要求

- Python 3.10+
- pip（Python 包管理器）
- Git

### 克隆项目

```bash
git clone https://github.com/your-username/your-blog-repo.git
cd your-blog-repo
```

### 创建虚拟环境

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows PowerShell
python -m venv .venv
.venv\Scripts\activate
```

### 安装依赖

```bash
pip install -r requirements.txt
```

### 数据库配置

项目默认使用 SQLite 数据库，无需额外安装数据库服务。

```bash
# 创建或更新数据库表结构
python manage.py migrate

# 创建超级管理员（首次部署时执行）
python manage.py createsuperuser
```

### 初始化数据

```bash
# 创建 About 页面
python manage.py shell -c "
from blog.models import SitePage
SitePage.objects.get_or_create(slug='about', defaults={'title': 'About', 'content': '<p>Welcome to my blog.</p>'})
"

# 创建首页内容
python manage.py shell -c "
from blog.models import HomePage
HomePage.objects.get_or_create(slogan='「探索 · 创造 · 分享」', defaults={})
"
```

### 收集静态文件

```bash
python manage.py collectstatic --noinput
```

### 多语言编译

```bash
# 提取待翻译文本（修改 UI 文字后执行）
python manage.py makemessages -l zh-hans
python manage.py makemessages -l en
python manage.py makemessages -l ja

# 编译翻译文件
python manage.py compilemessages
```

### 启动开发服务器

```bash
python manage.py runserver 0.0.0.0:8000
```

访问 `http://localhost:8000/` 查看效果。

---

## 生产环境部署

### 方案一：Gunicorn + Nginx（推荐用于 VPS）

#### 1. 环境准备

```bash
# 安装系统依赖
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx git

# 克隆项目
git clone https://github.com/your-username/your-blog-repo.git
cd your-blog-repo

# 创建虚拟环境并安装依赖
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

#### 2. 配置生产设置

编辑 `myblog/settings.py`：

```python
# 关闭调试模式
DEBUG = False

# 设置允许访问的域名
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# 设置 SECRET_KEY 为环境变量
import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-dev-key')
```

也可以设置环境变量 `DJANGO_DEBUG=False` 自动禁用 DEBUG。

#### 3. 数据库迁移 & 静态文件

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py compilemessages
```

#### 4. 配置 Gunicorn 服务

创建 Systemd 服务文件 `/etc/systemd/system/myblog.service`：

```ini
[Unit]
Description=myblog Gunicorn Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/myblog
Environment="PATH=/path/to/myblog/.venv/bin"
ExecStart=/path/to/myblog/.venv/bin/gunicorn --workers 3 --bind unix:/path/to/myblog/myblog.sock myblog.wsgi:application

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl start myblog
sudo systemctl enable myblog
```

#### 5. 配置 Nginx 反向代理

创建 Nginx 配置文件 `/etc/nginx/sites-available/myblog`：

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # 静态文件
    location /static/ {
        alias /path/to/myblog/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # 媒体文件
    location /media/ {
        alias /path/to/myblog/media/;
        expires 30d;
    }

    # 反向代理到 Gunicorn
    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/myblog/myblog.sock;

        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $host;
    }

    # 安全头部
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

启用配置并重启 Nginx：

```bash
sudo ln -s /etc/nginx/sites-available/myblog /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 6. 配置 SSL（HTTPS）

推荐使用 Let's Encrypt：

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

---

### 方案二：PythonAnywhere（简易部署）

#### 1. 准备工作

- 在 [PythonAnywhere](https://www.pythonanywhere.com/) 注册账号（免费版可用）
- 创建 Web App：选择 Manual Configuration → Python 3.10

#### 2. 上传代码

```bash
# 在 PythonAnywhere Bash Console 中
git clone https://github.com/your-username/your-blog-repo.git
cd your-blog-repo

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### 3. 配置 Web 应用

在 Web 页面中设置：

- **Source code**: `/home/your-username/your-blog-repo`
- **Working directory**: `/home/your-username/your-blog-repo`
- **Virtual environment**: `/home/your-username/your-blog-repo/.venv`
- **WSGI configuration file**: 编辑为以下内容：

```python
import sys
path = '/home/your-username/your-blog-repo'
if path not in sys.path:
    sys.path.append(path)

from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = 'myblog.settings'
application = get_wsgi_application()
```

#### 4. 数据库 & 静态文件

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py compilemessages
```

#### 5. 配置静态文件映射

在 Web 页面 Static files 中添加：

- **URL**: `/static/` → **Directory**: `/home/your-username/your-blog-repo/staticfiles/`
- **URL**: `/media/` → **Directory**: `/home/your-username/your-blog-repo/media/`

#### 6. 重载 Web App

点击 **Reload** 按钮。

---

## 依赖管理

### requirements.txt

```txt
Django>=6.0,<6.1
django-ckeditor-5>=0.2,<1.0
Pillow>=10.0
gunicorn>=21.0
whitenoise>=6.0
markdown>=3.10
```

### 添加新依赖

```bash
pip install package-name
pip freeze > requirements.txt
```

---

## 基础功能使用指引

### 管理员后台

访问 `http://your-domain.com/admin/` 使用超级管理员账号登录。

#### 文章管理

- **写文章**：点击「写文章」按钮，使用 CKEditor 5 富文本编辑器
- **分类管理**：创建和管理文章分类
- **标签管理**：添加和管理文章标签
- **草稿箱**：已保存但未发布的文章

#### 评论审核

- 新评论默认不显示，需在后台审核通过后才会公开
- 支持删除违规评论

#### 首页内容

- 可编辑首页 Hero 区域的标语和副标题
- 可编辑首页四个卡片的内容：「关于」「当下」「技能栈」「热爱与坚持」

### 文章发布

1. 在 Django Admin 后台创建文章
2. 填写标题、正文、选择分类和标签
3. 选择文章语言（中文 / English / 日本語）
4. 状态选择「已发布」保存即可
5. 文章 URL 别名（slug）可自动生成或手动指定

### 多语言切换

- 网站右上角提供语言切换下拉菜单
- 文章可按语言筛选显示
- 管理员可分别为不同语言撰写文章版本

### 用户注册与登录

- 支持用户名或 Email 登录
- 注册后可在个人中心编辑资料
- 支持找回密码功能

---

## 常见部署问题排查

### 1. 页面 500 错误：数据库表不存在

```bash
# 原因：数据库迁移未执行
python manage.py migrate
```

### 2. 页面 404 错误：About 页面无法打开

```bash
# 原因：SitePage 表中缺少 slug='about' 的记录
python manage.py shell -c "
from blog.models import SitePage
SitePage.objects.get_or_create(slug='about', defaults={'title': 'About', 'content': '<p>Welcome to my blog.</p>'})
"
```

### 3. 静态文件 404

```bash
# 原因：静态文件未收集或配置不正确
python manage.py collectstatic --noinput

# 确认 settings.py 中的配置：
# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STORAGES 配置了 WhiteNoise 后端
```

### 4. 中文显示乱码

```python
# 确认 settings.py 中的配置：
LANGUAGE_CODE = 'zh-hans'
# 确保 locale 目录包含对应语言的 .mo 文件
```

### 5. 图片上传失败

- 检查 `media/` 目录是否存在且有写权限
- 确认 `CKEDITOR_5_MAX_FILE_SIZE` 配置（默认 10MB）
- 检查上传文件类型是否在白名单中

### 6. 多语言不生效

```bash
# 重新编译翻译文件
python manage.py compilemessages

# 确认浏览器语言设置或手动切换网站语言
# 在 URL 后添加 ?language=en 可强制切换语言
```

### 7. Gunicorn 启动失败

```bash
# 检查日志
sudo journalctl -u myblog

# 常见原因：路径错误、权限不足、.venv Python 版本不匹配
# 尝试手动启动测试：
/path/to/.venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 myblog.wsgi:application
```

### 8. Permission denied（权限拒绝）

```bash
# 确保静态文件和媒体文件目录有正确权限
sudo chown -R www-data:www-data /path/to/myblog/staticfiles/
sudo chown -R www-data:www-data /path/to/myblog/media/
sudo chmod -R 755 /path/to/myblog/staticfiles/
sudo chmod -R 755 /path/to/myblog/media/
```

---

---

## Project Overview

A personal technical blog built with **Django 6**, featuring an interactive Three.js galaxy background and support for Chinese, English, and Japanese interfaces. Includes a blog post system, portfolio showcase, comment interaction, user registration/login, and user profile management.

### Core Features

- **Blog Post System**: Rich text editor (CKEditor 5), category/tag management, language filtering, estimated reading time, view count
- **Portfolio Showcase**: Tab filtering + card grid layout, project detail modals, skill tags
- **Comment System**: Generic foreign key design, supports guest comments and registered user comments, nested replies, admin review
- **User System**: Registration/login/password reset, email verification, profile editing, supports email or username login
- **Multi-language**: Chinese, English, Japanese — full Django i18n implementation
- **Interactive Background**: Three.js 3D galaxy particle animation, auto-adapts to page context
- **Responsive Design**: 2-3 column grid on desktop → 2 columns on tablet → 1 column on mobile
- **Admin Panel**: Django Admin interface for managing posts, comments, users, homepage content, etc.

### Tech Stack

| Category | Technology |
|----------|------------|
| **Backend** | Django 6.0 + SQLite |
| **Frontend** | HTML/CSS/JavaScript + Three.js (3D background) |
| **Rich Text Editor** | CKEditor 5 |
| **Static Files** | WhiteNoise |
| **Deployment** | Gunicorn + Nginx (reverse proxy) / PythonAnywhere |
| **CI/CD** | GitHub Actions (auto-deploy to PythonAnywhere) |
| **i18n** | Django i18n (gettext + .po/.mo files) |
| **Auth** | Django Auth + custom email login backend |

### Project Structure

```
myblog/
├── myblog/                  # Django project configuration
│   ├── settings.py          # Global settings (DB, static, i18n, etc.)
│   ├── urls.py              # Root URL routing
│   ├── wsgi.py              # WSGI entry point
│   └── asgi.py              # ASGI entry point
│
├── blog/                    # Blog app (core)
│   ├── models.py            # Post, Category, Tag, SitePage, HomePage
│   ├── views.py             # Home, post list/detail, search views
│   ├── urls.py              # Blog URL routing
│   ├── admin.py             # Admin configuration
│   ├── context_processors.py# Sidebar global context
│   ├── templatetags/        # Custom template tags
│   └── templates/blog/      # Blog templates
│
├── users/                   # User app
│   ├── models.py            # UserProfile (extended user model)
│   ├── views.py             # Register/login/profile/password management
│   ├── forms.py             # User forms
│   └── templates/users/     # User templates
│
├── comments/                # Comment app
│   ├── models.py            # Comment (generic foreign key + nested replies)
│   ├── forms.py             # Comment form
│   └── admin.py             # Comment admin
│
├── locale/                  # i18n translation files
│   ├── zh_Hans/LC_MESSAGES/ # Chinese translations
│   ├── en/LC_MESSAGES/      # English translations
│   └── ja/LC_MESSAGES/      # Japanese translations
│
├── static/                  # Global static files
│   ├── blog/css/style.css   # Main stylesheet
│   └── blog/images/         # Image assets
│
├── staticfiles/             # collectstatic output
├── media/                   # User uploads
├── db.sqlite3               # SQLite database
│
├── requirements.txt         # Python dependencies
├── .github/workflows/       # GitHub Actions deployment config
└── README.md                # This file
```

---

## Local Development Setup

### Prerequisites

- Python 3.10+
- pip
- Git

### Clone

```bash
git clone https://github.com/your-username/your-blog-repo.git
cd your-blog-repo
```

### Virtual Environment

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows PowerShell
python -m venv .venv
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Database Setup

The project uses SQLite by default — no separate database server required.

```bash
python manage.py migrate
python manage.py createsuperuser
```

### Initialize Data

```bash
# Create About page
python manage.py shell -c "
from blog.models import SitePage
SitePage.objects.get_or_create(slug='about', defaults={'title': 'About', 'content': '<p>Welcome to my blog.</p>'})
"

# Create homepage content
python manage.py shell -c "
from blog.models import HomePage
HomePage.objects.get_or_create(slogan='「探索 · 创造 · 分享」', defaults={})
"
```

### Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Compile Translations

```bash
python manage.py makemessages -l zh-hans
python manage.py makemessages -l en
python manage.py makemessages -l ja
python manage.py compilemessages
```

### Start Development Server

```bash
python manage.py runserver 0.0.0.0:8000
```

Visit `http://localhost:8000/`.

---

## Production Deployment

### Option 1: Gunicorn + Nginx (Recommended for VPS)

#### 1. System Setup

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx git
git clone https://github.com/your-username/your-blog-repo.git
cd your-blog-repo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

#### 2. Production Settings

Edit `myblog/settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-dev-key')
```

Or set environment variable `DJANGO_DEBUG=False`.

#### 3. Database & Static Files

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py compilemessages
```

#### 4. Configure Gunicorn Service

Create `/etc/systemd/system/myblog.service`:

```ini
[Unit]
Description=myblog Gunicorn Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/myblog
Environment="PATH=/path/to/myblog/.venv/bin"
ExecStart=/path/to/myblog/.venv/bin/gunicorn --workers 3 --bind unix:/path/to/myblog/myblog.sock myblog.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start myblog
sudo systemctl enable myblog
```

#### 5. Configure Nginx

Create `/etc/nginx/sites-available/myblog`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location /static/ {
        alias /path/to/myblog/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /path/to/myblog/media/;
        expires 30d;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/myblog/myblog.sock;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $host;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/myblog /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 6. SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### Option 2: PythonAnywhere

1. Register at [PythonAnywhere](https://www.pythonanywhere.com/)
2. Create Web App: Manual Configuration → Python 3.10
3. Clone the repo and set up the virtual environment
4. Configure WSGI file, static files mapping
5. Run `migrate`, `collectstatic`, `compilemessages`
6. Click **Reload**

---

## Common Deployment Issues

### 1. 500 Error: Database tables not found

```bash
python manage.py migrate
```

### 2. 404 Error: About page

```bash
python manage.py shell -c "
from blog.models import SitePage
SitePage.objects.get_or_create(slug='about', defaults={'title': 'About', 'content': '<p>Welcome to my blog.</p>'})
"
```

### 3. Static files 404

```bash
python manage.py collectstatic --noinput
# Verify STATIC_URL, STATIC_ROOT, and STORAGES config in settings.py
```

### 4. Character encoding issues

```python
# Check settings.py:
LANGUAGE_CODE = 'zh-hans'
# Ensure .mo files exist in the locale directory
```

### 5. Image upload fails

- Check `media/` directory exists and is writable
- Check `CKEDITOR_5_MAX_FILE_SIZE` (default 10MB)
- Check file type whitelist

### 6. i18n not working

```bash
python manage.py compilemessages
# Force language switch: add ?language=en to URL
```

### 7. Gunicorn fails to start

```bash
sudo journalctl -u myblog
# Test manually: /path/to/.venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 myblog.wsgi:application
```

### 8. Permission denied

```bash
sudo chown -R www-data:www-data /path/to/myblog/staticfiles/
sudo chown -R www-data:www-data /path/to/myblog/media/
```

---

---

## プロジェクト概要

**Django 6** をベースに構築された個人技術ブログ。Three.js によるインタラクティブな銀河背景を備え、中国語・英語・日本語の3言語に対応しています。ブログ記事システム、ポートフォリオ展示、コメント機能、ユーザー登録・ログイン、プロフィール管理などの完全な機能を提供します。

### 主な機能

- **ブログ記事システム**: リッチテキストエディター（CKEditor 5）、カテゴリ/タグ管理、言語フィルタリング、読了時間推定、閲覧数カウント
- **ポートフォリオ**: タブフィルタリング＋カードグリッドレイアウト、プロジェクト詳細モーダル、スキルタグ表示
- **コメントシステム**: ジェネリック外部キー設計、ゲストコメントと登録ユーザーコメント対応、ネスト返信、管理画面承認
- **ユーザーシステム**: 登録/ログイン/パスワードリセット、メール認証、プロフィール編集、メールまたはユーザー名ログイン対応
- **多言語対応**: 中文、English、日本語 — Django i18n 完全実装
- **インタラクティブ背景**: Three.js 3D 銀河パーティクルアニメーション、自動ページ適応
- **レスポンシブデザイン**: デスクトップ2〜3列 → タブレット2列 → モバイル1列
- **管理パネル**: Django Admin インターフェースで記事・コメント・ユーザー・ホームページ内容などを管理

### 技術スタック

| カテゴリ | 技術 |
|----------|------|
| **バックエンド** | Django 6.0 + SQLite |
| **フロントエンド** | HTML/CSS/JavaScript + Three.js (3D背景) |
| **リッチテキストエディター** | CKEditor 5 |
| **静的ファイル** | WhiteNoise |
| **デプロイ** | Gunicorn + Nginx (リバースプロキシ) / PythonAnywhere |
| **CI/CD** | GitHub Actions (PythonAnywhere 自動デプロイ) |
| **国際化** | Django i18n (gettext + .po/.mo ファイル) |
| **認証** | Django Auth + カスタムメールログインバックエンド |

### プロジェクト構造

```
myblog/
├── myblog/                  # Django プロジェクト設定
│   ├── settings.py          # 全体設定（DB、静的ファイル、i18n 等）
│   ├── urls.py              # ルート URL ルーティング
│   ├── wsgi.py              # WSGI エントリーポイント
│   └── asgi.py              # ASGI エントリーポイント
│
├── blog/                    # ブログアプリ（コア）
│   ├── models.py            # Post, Category, Tag, SitePage, HomePage
│   ├── views.py             # ホーム、記事一覧/詳細、検索ビュー
│   ├── urls.py              # ブログ URL ルーティング
│   ├── admin.py             # 管理画面設定
│   ├── context_processors.py# サイドバーのグローバルコンテキスト
│   └── templates/blog/      # ブログテンプレート
│
├── users/                   # ユーザーアプリ
│   ├── models.py            # UserProfile（拡張ユーザーモデル）
│   ├── views.py             # 登録/ログイン/プロフィール/パスワード管理
│   └── templates/users/     # ユーザーテンプレート
│
├── comments/                # コメントアプリ
│   ├── models.py            # Comment（ジェネリック外部キー＋ネスト返信）
│   ├── forms.py             # コメントフォーム
│   └── admin.py             # コメント管理
│
├── locale/                  # i18n 翻訳ファイル
│   ├── zh_Hans/LC_MESSAGES/ # 中国語翻訳
│   ├── en/LC_MESSAGES/      # 英語翻訳
│   └── ja/LC_MESSAGES/      # 日本語翻訳
│
├── static/                  # グローバル静的ファイル
├── staticfiles/             # collectstatic 出力ディレクトリ
├── media/                   # ユーザーアップロード
├── db.sqlite3               # SQLite データベース
│
├── requirements.txt         # Python 依存関係
└── README.md                # 本ファイル
```

---

## ローカル開発環境のセットアップ

### 前提条件

- Python 3.10+
- pip
- Git

### クローン

```bash
git clone https://github.com/your-username/your-blog-repo.git
cd your-blog-repo
```

### 仮想環境

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 依存関係のインストール

```bash
pip install -r requirements.txt
```

### データベース設定

デフォルトでは SQLite を使用します。別途データベースサーバーは不要です。

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 初期データ

```bash
# About ページの作成
python manage.py shell -c "
from blog.models import SitePage
SitePage.objects.get_or_create(slug='about', defaults={'title': 'About', 'content': '<p>Welcome to my blog.</p>'})
"

# ホームページ内容の作成
python manage.py shell -c "
from blog.models import HomePage
HomePage.objects.get_or_create(slogan='「探索 · 創造 · 共有」', defaults={})
"
```

### 静的ファイルの収集

```bash
python manage.py collectstatic --noinput
```

### 翻訳ファイルのコンパイル

```bash
python manage.py makemessages -l zh-hans
python manage.py makemessages -l en
python manage.py makemessages -l ja
python manage.py compilemessages
```

### 開発サーバーの起動

```bash
python manage.py runserver 0.0.0.0:8000
```

`http://localhost:8000/` にアクセス。

---

## 本番環境デプロイ

### オプション1: Gunicorn + Nginx（VPS推奨）

#### 1. システムセットアップ

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx git
git clone https://github.com/your-username/your-blog-repo.git
cd your-blog-repo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

#### 2. プロダクション設定

`myblog/settings.py` を編集：

```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
```

または環境変数 `DJANGO_DEBUG=False` を設定。

#### 3. データベースと静的ファイル

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py compilemessages
```

#### 4〜6. Gunicorn + Nginx + SSL

中国語版と同じ手順で Systemd サービス、Nginx 設定、Let's Encrypt SSL を構成してください。

### オプション2: PythonAnywhere

中国語版と同じ手順でデプロイ可能です。

---

## よくある問題と解決方法

### 1. 500 エラー：データベーステーブルが見つからない

```bash
python manage.py migrate
```

### 2. 404 エラー：About ページ

```bash
python manage.py shell -c "
from blog.models import SitePage
SitePage.objects.get_or_create(slug='about', defaults={'title': 'About', 'content': '<p>Welcome to my blog.</p>'})
"
```

### 3. 静的ファイル 404

```bash
python manage.py collectstatic --noinput
```

### 4. 文字化け

```python
# settings.py の確認：
LANGUAGE_CODE = 'zh-hans'
# locale ディレクトリに .mo ファイルが存在することを確認
```

### 5. 画像アップロード失敗

- `media/` ディレクトリが存在し書き込み可能か確認
- `CKEDITOR_5_MAX_FILE_SIZE`（デフォルト10MB）を確認
- ファイルタイプが許可リストに含まれているか確認

### 6. i18n が動作しない

```bash
python manage.py compilemessages
# URL に ?language=en を追加して言語を強制切り替え
```

### 7. Gunicorn 起動失敗

```bash
sudo journalctl -u myblog
# 手動テスト: /path/to/.venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 myblog.wsgi:application
```

### 8. パーミッションエラー

```bash
sudo chown -R www-data:www-data /path/to/myblog/staticfiles/
sudo chown -R www-data:www-data /path/to/myblog/media/
```

---

## ライセンス

MIT License
