# src/services/email_service.py

import smtplib
from email.message import EmailMessage

def criar_mensagem_email(email, codigo_aleatorio):
    msg = EmailMessage()
    msg['Subject'] = 'Código de Verificação - Contabilize Bem'
    msg['From'] = 'lucasmellomo@gmail.com'
    msg['To'] = email

    html_content = f"""
    <html>
        <body>
            <p>Oi! Você recebeu este e-mail da <b>Contabilize Bem</b>.</p>
            <p>Seu código de verificação é: <b style="font-size: 24px;">{codigo_aleatorio}</b></p>
            <p>Se você não reconhece este e-mail, por favor, ignore-o.</p>
            <p>Obrigado,</p>
            <p><b>Contabilize Bem</b></p>
        </body>
    </html>
    """
    msg.add_alternative(html_content, subtype='html')
    return msg
