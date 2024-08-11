from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import logging
import sqlite3
from pathlib import Path

app = FastAPI()
templates = Jinja2Templates(directory="./templates/")

DB_NAME = "contacts.db"
DATABASE_PATH = Path(DB_NAME)

def init_db():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    # (存在しない場合のみ)テーブルの作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            description TEXT
        )
    ''')
    # 初期データの挿入 (必要に応じて)
    cursor.execute('''
        INSERT INTO contacts (name, phone) VALUES
        ('test user', '000-1111-2222')
    ''')
    connection.commit()
    connection.close()

@app.on_event("startup")
async def startup():
    # DB初期化
    init_db()

@app.on_event("shutdown")
async def shutdown():
    pass

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

    

@app.post("/addContact")
async def addContact(request: Request, name: str=Form(...), phone: str=Form(...)):
    with sqlite3.connect(DB_NAME) as conn:
        logging.debug("addRecord")
        cursor = conn.cursor()
        cursor.execute('''
            insert into contacts (name, phone) values
            (?, ?)
        ''', (name, phone))
        conn.commit()
    return RedirectResponse(url='/', status_code=303)

@app.post("/resetContactList")
async def resetContactList(request: Request):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("delete from contacts")
        conn.commit()
    return RedirectResponse(url='/', status_code=303)

@app.get('/showContactList', response_class=HTMLResponse)
async def showContactList(request: Request):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        items = cursor.execute('''
            select * from contacts
        '''
        ).fetchall()
        param = {'request': request, 'items': items}
    return templates.TemplateResponse('contactList.html', param)
