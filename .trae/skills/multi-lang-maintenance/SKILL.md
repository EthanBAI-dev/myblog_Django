---
name: "multi-lang-maintenance"
description: "维护项目的中文/英文/日文三语同步。修改UI文字、博客内容、模板时，必须同步更新三种语言的翻译文件(.po)和博客内容。适用于本Django博客项目（Django i18n + .po文件）。"
---

# 多语言同步维护规则

本博客支持三种语言：**中文 (zh-hans)**、**English (en)**、**日本語 (ja)**

## 核心原则

> **改任何东西之前，先问自己：这个改动涉及几种语言？**
>
> 每次改动都要同步三份，漏掉一个就是 bug。

---

## 规则一：UI 文字改动

### 涉及文件

| 文件 | 说明 |
|------|------|
| Python 代码中的 `_('xxx')` 和 `gettext()` | 后端文字 |
| HTML 模板中的 `{% trans %}` 和 `{% blocktranslate %}` | 前端文字 |
| `locale/zh-hans/LC_MESSAGES/django.po` | 中文翻译 |
| `locale/en/LC_MESSAGES/django.po` | 英文翻译 |
| `locale/ja/LC_MESSAGES/django.po` | 日文翻译 |

### 改动步骤

```
1. 在代码或模板中添加/修改文字
    ↓
2. 运行翻译文件更新命令
    ↓
3. 编辑三个 .po 文件，填写对应的翻译
    ↓
4. 编译 .mo 文件
    ↓
5. 确认三种语言下显示都正常
```

### 常用命令

```bash
# 提取代码中所有待翻译文字，更新 .po 文件
python manage.py makemessages -l zh-hans
python manage.py makemessages -l en
python manage.py makemessages -l ja

# 编辑 .po 文件，填写翻译后，编译为 .mo
python manage.py compilemessages
```

### 举例

修改导航栏"About"为"About Me"时：

| .po 文件 | 修改方式 |
|----------|----------|
| `zh-hans` | 原来 `msgstr "关于"` → `msgstr "关于我"` |
| `en` | 原来 `msgstr "About"` → `msgstr "About Me"` |
| `ja` | 原来 `msgstr "について"` → `msgstr "私について"` |

---

## 规则二：博客内容改动

### 两种情况

**情况 A：修改已有文章**
- 找到该文章对应的三个语言版本
- 同步修改正文
- 如果只改了中文版，英文和日文版会显示旧内容

**情况 B：发布新文章**
- 至少发布中文版
- 英文和日文版可以先写简版或放占位提示，但不能空白

### 文件约定

```
blog/content/
├── zh-hans/
│   └── my-article.md          ← 中文原文
├── en/
│   └── my-article.md          ← 英文翻译
└── ja/
    └── my-article.md          ← 日文翻译
```

---

## 规则三：样式和模板改动

### 模板文字用翻译标签

```html
<!-- ❌ 错误：直接写死文字 -->
<h2>最新文章</h2>

<!-- ✅ 正确：用翻译标签 -->
{% load i18n %}
<h2>{% trans "最新文章" %}</h2>
```

样式中的硬编码文字（如 banner 标题、按钮文字）同样需要用 `{% trans %}` 包裹。

---

## 规则四：检查清单

每次改动后，依次检查：

- [ ] 代码中的 `_()` 是否全部提取（运行 `makemessages`）
- [ ] 三个 `.po` 文件是否都填写了翻译
- [ ] `.mo` 文件是否已编译（运行 `compilemessages`）
- [ ] 三种语言下 UI 显示是否正常
- [ ] 博客内容三种语言是否同步更新

---

## 陷阱一：`#, fuzzy` 标记

`makemessages` 自动生成的 `#, fuzzy` 标记表示"存疑翻译"，**Django 会跳过该条目**，显示原文而非翻译。

**修复方式：** 编辑 `.po` 文件，直接删掉 `#, fuzzy` 行和旧 `msgstr`，写入正确翻译。

```
# 原文（会被跳过，不生效）
#, fuzzy
msgid "全部"
msgstr "All Comments"

# 修复后（正常生效）
msgid "全部"
msgstr "All"
```

---

## 陷阱二：python-format 的 `%%` 转义

`msgid` 中如果有 `95%%`（Django 的 `%%` 表示一个 `%` 符号），
对应 `msgstr` 也必须用 `%%`，不能写成 `95%`，否则 `compilemessages` 报错：

```
msgid "开发自动化工具缩短 95%% 作业时间"
msgstr "Built automation tools cutting 95%% of work time"   # ✅ 正确（必须是 %%）
msgstr "Built automation tools cutting 95% of work time"    # ❌ 错误（格式不匹配）
```

---

## 陷阱三：数据库字段绕过翻译

如果模板中同时有数据库字段和 `{% trans %}`：

```html
{% if homepage and homepage.slogan %}
  {{ homepage.slogan }}          {# ← 数据库有值时走这里，绕过翻译 #}
{% else %}
  {% trans "默认文字" %}          {# ← 只有数据库为空时才走翻译 #}
{% endif %}
```

**解决方案：** 清空数据库字段让 `{% trans %}` 生效，或将数据库字段改为 JSON 存储多语言值。

---

## 陷阱四：部署时 .mo 文件冲突

`.po` 和 `.mo` 文件在服务器上被手动操作过，`git pull` 会报冲突。

**解决方案：** `git pull` 前先丢弃本地修改：

```bash
git checkout -- locale/*/LC_MESSAGES/django.mo 2>/dev/null || true
git clean -fd locale/ 2>/dev/null || true
git pull origin your-branch
```

---

## 快速对照表

| 操作 | 涉及文件数 |
|------|-----------|
| 新增一个按钮文字 | ≥ 5 (代码 + 3个.po + .mo) |
| 修改文章正文 | 3 (三个语言的正文文件) |
| 新增页面模板 | ≥ 5 (.html + 3个.po + 编译) |
| 新增语言支持 | 很多 (settings.py + 新locale + 全部翻译) |
