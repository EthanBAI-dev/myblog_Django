# PythonAnywhere 强制更新

## 完整部署（首次或大更新）

```bash
cd ~/myblog_Django
git pull origin personal-website-redesign
source venv/bin/activate
pip install -r requirements.txt -q
python manage.py migrate --noinput
python manage.py collectstatic --noinput
touch /var/www/ethanbai_pythonanywhere_com_wsgi.py
```

## 快速更新（仅拉代码 + 重载）

```bash
cd ~/myblog_Django
git pull origin personal-website-redesign
touch /var/www/ethanbai_pythonanywhere_com_wsgi.py
```

## 仅重载网站

浏览器打开 PythonAnywhere → **Web** → 点 **Reload**

或命令行：

```bash
touch /var/www/ethanbai_pythonanywhere_com_wsgi.py
```

## 查看错误日志

PythonAnywhere → **Web** → **Error log**
