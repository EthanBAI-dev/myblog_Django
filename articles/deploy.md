# PythonAnywhere 部署指南

## 部署脚本

`~/deploy-full.sh` — GitHub Actions 自动部署时执行。

> ⚠️ 脚本在本项目根目录 `deploy-full.sh` 维护；PA 上的是独立副本，不会随 `git pull` 自动更新。更新脚本后需手动复制到 PA。

---

## 标准手动部署

```bash
cd ~/myblog_Django

# 1. 丢弃本地 .mo 避免 git 冲突
git checkout -- locale/*/LC_MESSAGES/django.mo 2>/dev/null || true
git clean -fd locale/ 2>/dev/null || true
git pull origin personal-website-redesign

# 2. 激活环境
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt -q

# 4. 数据库迁移
python manage.py migrate --noinput

# 5. 编译翻译
python manage.py compilemessages

# 6. 收集静态文件
python manage.py collectstatic --noinput

# 7. 重载
touch /var/www/ethanbai_pythonanywhere_com_wsgi.py
```

## 首次部署（需导入数据）

完成上述步骤后多两步：

```bash
python manage.py flush --noinput              # 清空旧数据
python manage.py loaddata data.json           # 导入本地导出的数据
```

## 仅重载

```bash
touch /var/www/ethanbai_pythonanywhere_com_wsgi.py
```

或浏览器 → PythonAnywhere **Web** → **Reload**。

## 查看错误日志

PythonAnywhere **Web** → **Error log**

## 常见问题

| 问题 | 原因 | 解决 |
|:----|:-----|:-----|
| `git pull` 冲突 | 服务器本地修改了 `.mo`/`.po` | `git checkout -- locale/*/*.mo` + `git clean -fd locale/` 后再 pull |
| `compilemessages` 报错 | `msgid` 和 `msgstr` 的 `%%` 数量不匹配 | 检查 `.po` 中 `#, python-format` 条目，确保两者一致 |
| 页面 500 · Manifest 错误 | `{% static %}` 引用了不存在的文件 | 检查模板中的静态文件路径，或改用 inline SVG |
| 页面 500 · 未知原因 | 代码 bug | 查看 **Error log** 获取具体 traceback |
| 页面 404 | 数据库无数据 | `flush` + `loaddata data.json` |
| 翻译不生效 | `#, fuzzy` 标记未删除 | 删掉 `#, fuzzy` 行 |
| 样式错乱 | 静态文件未更新 | `collectstatic --noinput --clear` + Reload |
