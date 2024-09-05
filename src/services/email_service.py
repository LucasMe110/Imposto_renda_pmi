import smtplib
from email.message import EmailMessage

def criar_mensagem_email(email, codigo_aleatorio):
    msg = EmailMessage()
    msg['Subject'] = 'Confirmar seu e-mail - Contabilize Bem'
    msg['From'] = 'equipe.contabilizebem@gmail.com'
    msg['To'] = email

    html_content = f"""
    <html>
        <body>
            <h2>Confirme seu e-mail da Contabilize Bem</h2>
            <p>Código de confirmação:</p>
            <div style="padding: 10px; font-size: 24px; font-weight: bold; border: 2px solid #000; display: inline-block;">
                {codigo_aleatorio}
            </div>
            <p>Para confirmar este e-mail para sua conta, por favor, insira o código acima no aplicativo.</p>
            <p>Se você não reconhece este e-mail, por favor, ignore-o.</p>
            <p>Obrigado,</p>
            <p><b>Equipe Contabilize Bem</b></p>
        </body>
    </html>
    """
    msg.add_alternative(html_content, subtype='html')
    return msg
