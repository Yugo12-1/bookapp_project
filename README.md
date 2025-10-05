# 📚 BookApp - Django CRUD Sample

DjangoのFunction-Based Viewで実装したシンプルな本棚アプリです。  
本の登録・編集・削除・一覧表示（CRUD）を行うことができます。

---

## 🚀 Features
- 本のタイトル・著者・概要を登録可能
- Function-Based View でシンプルに実装
- DjangoのFormとModelを連携
- 管理画面でBookの管理が可能

---

## 🧩 Tech Stack
- Python 3.10.12
- Django 5.2.6
- HTML / CSS（templates使用）
- SQLite（開発用DB）

---

## ⚙️ Setup

1. 仮想環境を作成して有効化：
   ```bash
   python -m venv venv
   source venv/Scripts/activate   # Windowsの場合

2. 依存パッケージをインストール:
pip install django

3. マイグレーションを実行
python3 manage.py makemigrations
python3 manage.py migrate

4. スーパーユーザーの作成(DB)
python manage.py createsuperuser

5. 開発サーバーの起動
python manage.py runserver

6. ブラウザアクセス
http://127.0.0.1:8000/


