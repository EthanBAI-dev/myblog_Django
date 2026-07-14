# Quiet Cosmos — 個人テクノロジーブログ

[![中文](https://img.shields.io/badge/README-中文-blue?style=flat-square)](README.zh-CN.md)
[![English](https://img.shields.io/badge/README-English-blue?style=flat-square)](README.en-US.md)

**Django 6** ベースの個人テクノロジーブログ。Three.js によるインタラクティブな銀河背景と、中国語・英語・日本語の 3 言語に対応しています。

---

## 主な機能

- **ブログ記事** — CKEditor 5 リッチテキスト編集、カテゴリ/タグ管理、言語フィルター、読了時間推定、閲覧数
- **ポートフォリオ** — タブフィルター＋カードグリッド、プロジェクト詳細モーダル、スキルタグ
- **コメント** — 汎用外部キー、ゲスト/登録ユーザーコメント、ネスト返信、管理画面承認
- **ユーザー管理** — 登録/ログイン/パスワードリセット、メール認証、プロフィール編集
- **多言語対応** — 中文 / English / 日本語、Django i18n 完全実装
- **インタラクティブ背景** — Three.js 3D 銀河パーティクルアニメーション
- **レスポンシブ** — デスクトップ 3 列 → タブレット 2 列 → モバイル 1 列
- **管理パネル** — Django Admin で記事・コメント・ユーザーを管理

## 技術スタック

| カテゴリ | 技術 |
|----------|------|
| バックエンド | Django 6.0 + SQLite |
| フロントエンド | HTML/CSS/JavaScript + Three.js |
| エディター | CKEditor 5 |
| 静的ファイル | WhiteNoise |
| デプロイ | Gunicorn + Nginx / PythonAnywhere |
| CI/CD | GitHub Actions |
| 国際化 | Django i18n (gettext + .po/.mo) |
| 認証 | Django Auth + カスタムメールログイン |

## クイックスタート

```bash
# クローン
git clone https://github.com/EthanBAI-dev/myblog_Django.git
cd myblog_Django

# 仮想環境
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# 依存関係のインストール
pip install -r requirements.txt

# マイグレーションと初期データ
python manage.py migrate
python manage.py shell -c "
from blog.models import SitePage, HomePage
SitePage.objects.get_or_create(slug='about', defaults={'title': 'About', 'content': '<p>Welcome.</p>'})
HomePage.objects.get_or_create(defaults={})
"

# 静的ファイルの収集
python manage.py collectstatic --noinput

# 翻訳のコンパイル
python manage.py compilemessages

# サーバー起動
python manage.py runserver
```

http://localhost:8000/ にアクセス。

## 多言語メンテナンス

```bash
# 新しい文字列の抽出
python manage.py makemessages -l zh-hans -l en -l ja

# コンパイル
python manage.py compilemessages
```

注意点：
- `#, fuzzy` マーカーがあると翻訳がスキップされるため、行を削除してください
- `#, python-format` エントリでは `%%` の数を `msgstr` と一致させる必要があります

## デプロイ

### PythonAnywhere

詳細な手順は [deploy.md](articles/deploy.md) を参照。

### GitHub Actions 自動デプロイ

`personal-website-redesign` ブランチへのプッシュで自動実行：
1. `~/deploy-full.sh` を実行（プル、マイグレーション、翻訳コンパイル、静的ファイル収集）
2. Web サービスをリロード

GitHub Secrets の設定が必要：`PA_API_TOKEN`、`PA_USERNAME`。

## プロジェクト構造

```
myblog/
├── myblog/               # Django プロジェクト設定
│   ├── settings.py       # 全体設定
│   ├── urls.py           # ルートルーティング
│   └── wsgi.py           # WSGI エントリー
├── blog/                 # ブログアプリ（コア）
│   ├── models.py         # データモデル
│   ├── views.py          # ビュー関数
│   └── templates/blog/   # テンプレート
├── users/                # ユーザーアプリ
├── comments/             # コメントアプリ
├── locale/               # i18n 翻訳ファイル
│   ├── zh_Hans/          # 中国語
│   ├── en/               # 英語
│   └── ja/               # 日本語
├── static/               # 静的ファイル
├── requirements.txt      # Python 依存関係
└── .github/workflows/    # CI/CD 設定
```

## ライセンス

MIT
