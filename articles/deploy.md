# PythonAnywhere 部署指南

## 部署脚本位置

`~/deploy-full.sh` — GitHub Actions 自动部署时执行。

> ⚠️ 脚本在本项目根目录 `deploy-full.sh` 维护；**PA 上的是独立副本**，不会随 `git pull` 自动更新。
>
> 更新脚本后需手动复制到 PA：登录 PA Bash → 打开 https://raw.githubusercontent.com/EthanBAI-dev/myblog_Django/personal-website-redesign/deploy-full.sh → 复制内容粘贴到 `~/deploy-full.sh`

---

## 完整手动部署

```bash
cd ~/myblog_Django

# 1. 拉取最新代码（先丢弃本地 .mo 避免冲突）
git checkout -- locale/*/LC_MESSAGES/django.mo 2>/dev/null || true
git clean -fd locale/ 2>/dev/null || true
git pull origin personal-website-redesign

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt -q

# 4. 数据库迁移
python manage.py migrate --noinput

# 5. 编译翻译文件
python manage.py compilemessages

# 6. 收集静态文件
python manage.py collectstatic --noinput

# 7. 重载 Web 服务
touch /var/www/ethanbai_pythonanywhere_com_wsgi.py
```

## 仅拉代码 + 重载（小更新）

```bash
cd ~/myblog_Django
git checkout -- locale/*/LC_MESSAGES/django.mo 2>/dev/null || true
git clean -fd locale/ 2>/dev/null || true
git pull origin personal-website-redesign
python manage.py compilemessages
touch /var/www/ethanbai_pythonanywhere_com_wsgi.py
```

## 首次部署（刷新数据库）

```bash
cd ~/myblog_Django
git pull origin personal-website-redesign
source venv/bin/activate
pip install -r requirements.txt -q
python manage.py migrate --noinput
python manage.py flush --noinput           # 清空旧数据
python manage.py loaddata data.json        # 导入新数据
python manage.py compilemessages
python manage.py collectstatic --noinput
touch /var/www/ethanbai_pythonanywhere_com_wsgi.py
```

## 仅重载网站

- 浏览器打开 PythonAnywhere → **Web** → 点 **Reload**
- 或命令行：`touch /var/www/ethanbai_pythonanywhere_com_wsgi.py`

## 查看错误日志

PythonAnywhere → **Web** → **Error log**

## 常见问题

| 问题 | 解决方案 |
|:----:|:---------|
| `git pull` 冲突 | `git checkout -- locale/*/LC_MESSAGES/django.mo` + `git clean -fd locale/` 后再拉取 |
| `compilemessages` 报错 | 检查 `.po` 中 `%%` 数量是否与 `msgstr` 匹配 |
| 页面 500/样式错乱 | `collectstatic --noinput` 后 **Reload** |
| 页面 404（about/博客） | 数据库无数据 → `flush` + `loaddata data.json` |
