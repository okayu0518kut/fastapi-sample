from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import sqlite3
from pathlib import Path
from db import init_db, getConnection # 自分で定義

app = FastAPI()
templates = Jinja2Templates(directory="./templates/")

@app.on_event("startup")
async def startup():
    # DB初期化
    init_db()
    # データベースの接続を開く
    app.state.db = getConnection()

@app.on_event("shutdown")
async def shutdown():
    # データベースの接続を閉じる
    app.state.db.close()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
#    cursor = app.state.db.cursor()
#    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#    tables = cursor.fetchall()
#    return {"tables": tables}
    return templates.TemplateResponse("top.html", {"request": request})

@app.get('/list')
async def showList(request: Request):
    cursor = app.state.db.cursor()
    items = cursor.execute('''
        select * from item
    '''
    ).fetchall()
    param = {'request': request, 'items': items}
    return templates.TemplateResponse('list.html', param)
    

@app.get("/addRecord")
async def addItem(request: Request):
    logging.debug("addRecord")
    cursor = app.state.db.cursor()
    cursor.execute('''
        insert into items (name, description) values
        'test', 'this is a test')
    ''')
    return RedirectResponse(url='/', status_code=303)

@app.get('/list')
async def resetList(request: Request):
    cursor = app.state.db.cursor()
    items = cursor.execute('''
        select * from item
    '''
    ).fetchall()
    param = {'request': request, 'items': items}
    return templates.TemplateResponse('list.html', param)