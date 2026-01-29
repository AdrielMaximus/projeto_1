from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime, date
import sqlite3

app = FastAPI()
templates = Jinja2Templates(directory="templates")

DB = "atendimentos.db"

app.mount("/static", StaticFiles(directory="static"), name="static")


def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("""
      CREATE TABLE IF NOT EXISTS atendimentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        atendente TEXT,
        cliente TEXT,
        loja TEXT,
        cnpj TEXT,
        detalhe TEXT,
        solicitacao TEXT,
        demanda TEXT,
        mac_terminal TEXT,
        criado_em TEXT
      )
    """)
    return conn


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    conn = get_conn()
    hoje = date.today().isoformat()

    atendimentos = conn.execute(
        "SELECT * FROM atendimentos WHERE criado_em LIKE ?",
        (f"{hoje}%",)
    ).fetchall()

    conn.close()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "atendimentos": atendimentos
        }
    )


@app.post("/salvar")
def salvar(
    atendente: str = Form(...),
    cliente: str = Form(...),
    loja: str = Form(...),
    cnpj: str = Form(...),
    detalhe: str = Form(...),
    solicitacao: str = Form(...),
    demanda: str = Form(...),
    mac_terminal: str = Form(...)
):
    conn = get_conn()
    conn.execute("""
      INSERT INTO atendimentos
      (atendente, cliente, loja, cnpj, detalhe, solicitacao, demanda, mac_terminal, criado_em)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        atendente,
        cliente,
        loja,
        cnpj,
        detalhe,
        solicitacao,
        demanda,
        mac_terminal,
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

    return RedirectResponse("/", status_code=303)
