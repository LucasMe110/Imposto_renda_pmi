# src/send_verification_email.py

from services.email_service import criar_mensagem_email
import smtplib

def send_verification_email(email, codigo_aleatorio):
    msg = criar_mensagem_email(email, codigo_aleatorio)

    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'lucasmellomo@gmail.com'
        smtp_password = 'xazg ocoq ywil ropc'  # Senha de aplicativo

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            print("Conectando ao servidor SMTP...")
            server.starttls()
            print("Iniciando TLS...")
            server.login(smtp_username, smtp_password)
            print("Autenticado com sucesso...")
            server.send_message(msg)
            print(f'E-mail enviado para {email} com sucesso.')

    except Exception as e:
        print(f'Erro ao enviar e-mail: {e}')
