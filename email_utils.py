import smtplib
from email.mime.text import MIMEText

def send_email(subject, body, to):
    sender_email = "TUCORREO"
    password = " TUCONTRASEÑA"

    try:
        # Configura el mensaje
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = to

        # Conecta al servidor SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, to, msg.as_string())

        print("Correo enviado!")
    except Exception as e:
        print(f"Error enviando correo: {e}")
