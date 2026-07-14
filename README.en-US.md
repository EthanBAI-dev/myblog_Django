# Quiet Cosmos — Personal Tech Blog

[![中文](https://img.shields.io/badge/README-中文-blue?style=flat-square)](README.zh-CN.md)
[![日本語](https://img.shields.io/badge/README-日本語-blue?style=flat-square)](README.ja-JP.md)

A personal tech blog built with **Django 6**, featuring an interactive Three.js galaxy background and trilingual interface (Chinese, English, Japanese).

---

## Features

- **Blog System** — CKEditor 5 rich text editing, category/tag management, language filtering, estimated reading time, view counter
- **Portfolio** — Tab filtering + card grid layout, project detail modals, skill tags
- **Comments** — Generic foreign key, guest/registered user comments, nested replies, admin review
- **User System** — Registration/login/password reset, email verification, profile editing
- **i18n** — Chinese / English / Japanese, full Django i18n implementation
- **Interactive Background** — Three.js 3D galaxy particle animation, auto-adapts to page
- **Responsive** — 3 columns (desktop) → 2 (tablet) → 1 (mobile)
- **Admin Panel** — Django Admin for posts, comments, users, homepage content

## Tech Stack

| Category | Technology |
|----------|------------|
| Backend | Django 6.0 + SQLite |
| Frontend | HTML/CSS/JavaScript + Three.js |
| Editor | CKEditor 5 |
| Static Files | WhiteNoise |
| Deployment | Gunicorn + Nginx / PythonAnywhere |
| CI/CD | GitHub Actions |
| i18n | Django i18n (gettext + .po/.mo) |
| Auth | Django Auth + custom email login |

## Quick Start

```bash
# Clone
git clone https://github.com/EthanBAI-dev/myblog_Django.git
cd myblog_Django

# Virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Migrate & init data
python manage.py migrate
python manage.py shell -c "
from blog.models import SitePage, HomePage
SitePage.objects.get_or_create(slug='about', defaults={'title': 'About', 'content': '<p>Welcome.</p>'})
HomePage.objects.get_or_create(defaults={})
"

# Collect static files
python manage.py collectstatic --noinput

# Compile translations
python manage.py compilemessages

# Run
python manage.py runserver
```

Open http://localhost:8000/

## i18n Maintenance

```bash
# Extract new strings
python manage.py makemessages -l zh-hans -l en -l ja

# Compile
python manage.py compilemessages
```

Common pitfalls:
- `#, fuzzy` markers cause translations to be skipped — delete the line
- `#, python-format` entries must use matching `%%` count in `msgstr`

## Deployment

### PythonAnywhere

See [deploy.md](articles/deploy.md) for step-by-step manual deployment.

### GitHub Actions Auto-deploy

Triggered on push to `personal-website-redesign`:
1. Runs `~/deploy-full.sh` (pull, migrate, compilemessages, collectstatic)
2. Reloads web service

Configure GitHub Secrets: `PA_API_TOKEN`, `PA_USERNAME`.

## Project Structure

```
myblog/
├── myblog/               # Django project config
│   ├── settings.py       # Global settings
│   ├── urls.py           # Root routing
│   └── wsgi.py           # WSGI entry
├── blog/                 # Core blog app
│   ├── models.py         # Data models
│   ├── views.py          # View functions
│   └── templates/blog/   # Templates
├── users/                # User app
├── comments/             # Comment app
├── locale/               # i18n translations
│   ├── zh_Hans/          # Chinese
│   ├── en/               # English
│   └── ja/               # Japanese
├── static/               # Static files
├── requirements.txt      # Python deps
└── .github/workflows/    # CI/CD config
```

## License

MIT
