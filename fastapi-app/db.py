import sqlite3
from pathlib import Path

DB_NAME = "main.db"
DATABASE_PATH = Path(DB_NAME)

def init_db():
    # データベースが存在しない場合のみ作成
    if not DATABASE_PATH.exists():
        connection = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # テーブルの作成
        cursor.execute('''
            CREATE TABLE items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            )
        ''')

        # 初期データの挿入 (必要に応じて)
        cursor.execute('''
            INSERT INTO items (name, description) VALUES
            ('Item1', 'This is the first item.'),
        ''')

        connection.commit()
        connection.close()

def getConnection():
    if Path(DB_NAME).exists():
        return sqlite3.connect(DB_NAME)
