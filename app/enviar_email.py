import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg["Subject"] = "Novo atendimento"
msg["From"] = "adriel@onenation.com.br"
msg["To"] = "rosalvo@onenation.com.br"
msg.set_content("Novo atendimento registrado")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login("adriel@onenation.com.br", "senha_app")
    smtp.send_message(msg)
