# Django Blog Deployment Guide: From Zero to Auto-Updates

> Applies to: myblog_Django (Django 6.0 + Python 3.13)

---

## 1. What We're Doing

### Goal

Take a locally developed Django blog project and put it online so others can access it. On top of that, whenever you push code updates to GitHub, the live site should update automatically.

### Breaking It Down

```
Final goal: Site live + auto-updates
 ├─ Step 1: Put code on GitHub (code hosting)
 ├─ Step 2: Create a site on PythonAnywhere (server)
 ├─ Step 3: Configure GitHub Actions for auto-deployment (automatic updates)
 └─ Done
```

---

## 2. What You'll Need (and What They Are)

### 1. A Working Django Blog Project

That's the Django blog project you're developing, with articles, comments, user accounts, and so on.

> If you don't have a project yet, check out my Django blog tutorial: \[link\]

### 2. GitHub — Where Your Code Lives

![](images/github-logo-placeholder.png)

- **What it is**: A code hosting platform — think of it as a cloud backup of your code
- **What it does**: Stores your project code and keeps a history of every change
- **What you need**: A GitHub account (free)

### 3. PythonAnywhere — Where Your Site Runs

![](images/pythonanywhere-logo-placeholder.png)

- **What it is**: A cloud server built specifically for running Python web apps
- **What it does**: Keeps your Django project running 24/7
- **What you need**: A PythonAnywhere account (the free tier is enough)

### 4. GitHub Actions — The Auto-Deploy Tool

![](images/github-actions-placeholder.png)

- **What it is**: GitHub's built-in automation tool
- **What it does**: Automatically notifies PythonAnywhere to update your site whenever you push code
- **What you need**: Comes free with your GitHub account

---

## 3. Preparation

### Check Your Project Structure

Make sure your project root has these key files:

```
myblog_Django/
├── manage.py              # Django management script
├── requirements.txt        # Python dependency list
├── myblog/
│   ├── settings.py         # Django configuration
│   ├── wsgi.py             # Site entry point
│   └── urls.py             # URL routing
├── blog/                   # Blog app
├── users/                  # User app
├── comments/               # Comments app
└── .github/workflows/      # GitHub Actions config (for auto-deploy)
```

> If you don't have a `requirements.txt` file, run this in your local terminal:
> ```bash
> pip install django django-ckeditor-5 pillow gunicorn whitenoise
> pip freeze > requirements.txt
> ```

---

## 4. Step One: Push Code to GitHub

### 4.1 Create a Repository on GitHub

1. Log in to [github.com](https://github.com)
2. Click the **+ → New repository** button in the top right
3. Name the repo `myblog_Django`, set it to **Public**
4. Don't check any boxes — just click **Create repository**

![](images/create-repo-placeholder.png)

### 4.2 Push Your Local Code to GitHub

In your local terminal (inside the project directory), run these commands in order:

```bash
# Initialize Git (if you haven't already)
git init

# Add all files to Git
git add .

# Commit
git commit -m "first commit"

# Link to the remote repo (replace with your actual GitHub username)
git remote add origin https://github.com/YourUsername/myblog_Django.git

# Push to GitHub
git push -u origin main
```

> If your default branch is `master` instead of `main`, replace `main` with `master` above.
> If you've already committed before, just run `git push`.

---

## 5. Step Two: Deploy the Site on PythonAnywhere

### 5.1 Sign Up and Log In

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Create an account (the free plan works fine)
3. After signing up, you'll get a domain: `YourUsername.pythonanywhere.com`

![](images/pa-signup-placeholder.png)

### 5.2 Open a Bash Console

After logging in, click **Consoles → Bash** in the top menu to open a command-line window.

![](images/pa-console-placeholder.png)

### 5.3 Clone the Code and Install Dependencies

In the Bash terminal, run these commands one by one:

```bash
# Clone the project from GitHub
git clone -b main https://github.com/YourUsername/myblog_Django.git

# Enter the project directory
cd myblog_Django

# Create a virtual environment (isolated Python runtime)
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

### 5.4 Prepare Static Files and the Database

Continue in the Bash terminal:

```bash
# Collect all static files (CSS, JS, images, etc.)
python manage.py collectstatic --noinput

# Create database tables
python manage.py migrate

# Create an admin account (follow the prompts for username, email, password)
python manage.py createsuperuser
```

### 5.5 Configure the Web App

Click **Web** in the top menu to open the web app management page.

![](images/pa-web-page-placeholder.png)

Click **Add a new web app**, then:

1. Click **Manual Configuration**
2. Select **Python 3.12**
3. Click **Next** to finish

### 5.6 Fill In the Configuration

After creating the web app, find the following settings on the Web page and update them:

| Setting | Value |
|---------|-------|
| **Code** (source code directory) | `/home/YourUsername/myblog_Django` |
| **Working directory** | `/home/YourUsername/myblog_Django` |
| **Virtualenv** (virtual environment) | `/home/YourUsername/myblog_Django/venv` |

![](images/pa-settings-placeholder.png)

### 5.7 Edit the WSGI File

On the Web page, find the **WSGI configuration file** link and click it to open the editor.

**Delete everything in the file** and replace it with this code:

```python
import os
import sys

# Project path
path = '/home/YourUsername/myblog_Django'
if path not in sys.path:
    sys.path.append(path)

# Specify Django's settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'myblog.settings'

# Disable debug mode in production
os.environ['DJANGO_DEBUG'] = 'False'

# Start Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

> **Note**: Replace `YourUsername` with your actual username, e.g., `EthanBAI`.

Click **Save** to save.

### 5.8 Add Static File Mappings

Scroll down on the same page to the **Static files** section:

![](images/pa-static-files-placeholder.png)

Add two entries:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/YourUsername/myblog_Django/staticfiles` |
| `/media/` | `/home/YourUsername/myblog_Django/media` |

### 5.9 Reload the Site

Click the green **Reload** button at the top of the page.

![](images/pa-reload-placeholder.png)

### 5.10 Visit Your Site

Open your browser and go to:

```
https://YourUsername.pythonanywhere.com
```

If everything is working, your blog should be live!

---

## 6. Step Three: Set Up Auto-Deployment

Manually logging into PythonAnywhere every time you update code gets old fast. Let's set up **GitHub Actions** for automatic deployments.

### 6.1 Create a Deployment Script on PythonAnywhere

Go back to the PythonAnywhere **Bash Console** and run:

```bash
cd ~
nano deploy.sh
```

Paste in the following content:

```bash
#!/bin/bash
# Auto-deploy script — pull latest code, update dependencies, run migrations
cd /home/YourUsername/myblog_Django

# Pull the latest code from GitHub
git pull origin main

# Activate the virtual environment
source venv/bin/activate

# Update dependencies
pip install -r requirements.txt -q

# Run database migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

echo "Code update complete!"
```

> **Note**: Replace `YourUsername` with your actual username.

Press `Ctrl+X`, then `Y`, then `Enter` to save.

Then run:

```bash
chmod +x deploy.sh
```

### 6.2 Create a Scheduled Task as a Fallback (Optional)

Scheduled tasks on PythonAnywhere are a paid feature. If you don't want to pay, skip this step — GitHub Actions will handle everything.

### 6.3 Add Secrets to Your GitHub Repository

Secrets are encrypted sensitive values that GitHub Actions uses to connect to PythonAnywhere.

#### Step 1: Generate a PythonAnywhere API Token

1. Log in to PythonAnywhere
2. Click your avatar in the top right → **Account**
3. Click the **API Token** tab
4. Click **Create new API token**
5. Copy the generated token (a long string)

![](images/pa-api-token-placeholder.png)

#### Step 2: Add the Secrets on GitHub

1. Open your GitHub repository: `https://github.com/YourUsername/myblog_Django`
2. Click the **Settings** tab
3. In the left sidebar, find **Secrets and variables → Actions**

![](images/github-secrets-placeholder.png)

4. Click **New repository secret** and add two secrets:

| Name | Value |
|------|-------|
| `PA_API_TOKEN` | The token you copied from PythonAnywhere |
| `PA_USERNAME` | Your PythonAnywhere username (e.g., `EthanBAI`) |

### 6.4 How GitHub Actions Works

The `.github/workflows/deploy.yml` file in your project is already configured with the auto-deploy workflow. Here's what happens:

```
You push code to GitHub
      ↓
GitHub Actions is triggered
      ↓
It notifies PythonAnywhere via API
      ↓
PythonAnywhere runs the deployment script
(pull code → install dependencies → migrate DB → collect static files)
      ↓
Site updates automatically 🎉
```

The config file looks like this (you generally don't need to modify it):

```yaml
name: Deploy to PythonAnywhere

on:
  push:
    branches: [main]          # Triggers when main branch gets a push

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger PythonAnywhere deployment
        run: |
          curl -H "Authorization: Token ${{ secrets.PA_API_TOKEN }}" \
               -H "Content-Type: application/json" \
               -X POST \
               "https://www.pythonanywhere.com/api/v0/user/${{ secrets.PA_USERNAME }}/webapps/${{ secrets.PA_USERNAME }}.pythonanywhere.com/reload/"
```

### 6.5 Test Auto-Deployment

1. Make any change to your local project (e.g., edit some text on a page)
2. Commit and push:

```bash
git add .
git commit -m "Test auto-deployment"
git push origin main
```

3. Go to your GitHub repository → **Actions** tab — you'll see the workflow running

![](images/github-actions-running-placeholder.png)

4. Wait for the workflow to turn into a green checkmark (about 30 seconds)
5. Refresh your site — the changes should be live

---

## 7. Common Issues

### Q: Site shows 502 Bad Gateway

**Cause**: WSGI configuration issue or missing dependencies.

**Fix**:
1. Click **Error log** on the PythonAnywhere Web page to check the error log
2. Common cause: `DEBUG = False` in `settings.py` without configuring `ALLOWED_HOSTS`
3. Add this to `settings.py`: `ALLOWED_HOSTS = ['YourUsername.pythonanywhere.com', 'localhost']`

### Q: Static files not loading (no CSS, images)

**Cause**: Static file paths are misconfigured.

**Fix**: Check the Static files section on the Web page:
- `/static/` → `/home/YourUsername/myblog_Django/staticfiles`
- Then re-run `python manage.py collectstatic`

### Q: Database errors

**Cause**: Database migrations haven't been run.

**Fix**: Run `python manage.py migrate` in the Bash console.

### Q: GitHub Actions failing

**Cause**: Secrets are misconfigured or a network issue.

**Fix**:
1. Check that `PA_API_TOKEN` and `PA_USERNAME` are set correctly in GitHub repo Settings → Secrets
2. Verify the token is valid on the PythonAnywhere Account → API Token page

---

## 8. Daily Workflow

After everything is configured, your daily routine becomes dead simple:

```
Write code → git add → git commit → git push
                                      ↓
                             Site auto-updates ✅
```

No more manually logging into PythonAnywhere to pull code or run migrations.

---

## Appendix: Key Commands to Remember

| Scenario | Command |
|----------|---------|
| Push code to GitHub | `git add . && git commit -m "message" && git push` |
| Manual deploy (if auto fails) | Log into PA Bash → `bash ~/deploy.sh` → Hit Reload on Web page |
| View error logs | PythonAnywhere Web page → Error log |
| Re-collect static files | `python manage.py collectstatic` |
| Check current branch | `git branch` |
| Switch branch | `git checkout branch-name` |

---

> **Tip**: Replace the image placeholders in this document with actual screenshots as needed.
