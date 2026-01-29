import sqlite3
import pandas as pd
import boto3
from datetime import date
import os
from email.message import EmailMessage
import smtplib

SES_REGION = "us-east-1"
EMAIL_ORIGEM = os.environ["EMAIL_ORIGEM"]
EMAIL_DESTINO = os.environ["EMAIL_DESTINO"]

DB_PATH = "/tmp/atendimentos.db"
ARQUIVO = "/tmp/atendimentos.xlsx"

def lambda_handler(event, context):
    conn = sqlite3.connect(DB_PATH)

    hoje = date.today().isoformat()
    df = pd.read_sql_query(
        "SELECT * FROM atendimentos WHERE criado_em LIKE ?",
        conn,
        params=(f"{hoje}%",)
    )

    if df.empty:
        return {"status": "sem dados"}

    df.to_excel(ARQUIVO, index=False)

    msg = EmailMessage()
    msg["Subject"] = "Atendimentos do dia"
    msg["From"] = EMAIL_ORIGEM
    msg["To"] = EMAIL_DESTINO
    msg.set_content("Segue planilha dos atendimentos de hoje.")

    with open(ARQUIVO, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename="atendimentos.xlsx"
        )

    ses = boto3.client("ses", region_name=SES_REGION)
    ses.send_raw_email(
        Source=EMAIL_ORIGEM,
        Destinations=[EMAIL_DESTINO],
        RawMessage={"Data": msg.as_bytes()}
    )

    # Apaga os dados do dia
    conn.execute(
        "DELETE FROM atendimentos WHERE criado_em LIKE ?",
        (f"{hoje}%",)
    )
    conn.commit()
    conn.close()

    return {"status": "email enviado"}
