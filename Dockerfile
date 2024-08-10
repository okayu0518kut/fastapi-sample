# ベースイメージを指定
FROM python:3.11-slim

# 作業ディレクトリを作成
WORKDIR /myapp

# 必要なファイルをコンテナ内にコピー
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

## アプリケーションのコードをコピー
#COPY . .

# アプリケーションのエントリーポイントを指定
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]

