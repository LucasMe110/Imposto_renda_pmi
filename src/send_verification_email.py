import smtplib
from email.message import EmailMessage

def send_verification_email(email, codigo_aleatorio):
    msg = EmailMessage()
    msg['Subject'] = 'Código de Verificação'
    msg['From'] = 'lucasmellomo@gmail.com'
    msg['To'] = email

    html_content = f"""
    <html>
        <body>
            <p>Oi! Seu código de verificação é: <b style="font-size: 24px;">{codigo_aleatorio}</b></p>
        </body>
    </html>
    """
    msg.add_alternative(html_content, subtype='html')

    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'lucasmellomo@gmail.com'
        smtp_password = 'xazg ocoq ywil ropc'  # Senha de aplicativo

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()

        print(f'E-mail enviado para {email} com sucesso.')

    except Exception as e:
        print(f'Erro ao enviar e-mail: {e}')
