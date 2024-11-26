import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def send_email(subject, body, to_email, file_path=None):
    from_email = os.getenv('EMAIL_ADDRESS') 
    password = os.getenv('EMAIL_PASSWORD') 
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Agregar el cuerpo del correo
    msg.attach(MIMEText(body, 'plain'))

    if file_path:
        # Adjuntar el archivo de video
        with open(file_path, 'rb') as file:
            part = MIMEBase('application', 'octet-stream')  # Tipo MIME genérico para archivos binarios
            part.set_payload(file.read())
            encoders.encode_base64(part)  # Codificación del archivo en base64 para enviarlo por email
            part.add_header('Content-Disposition', f'attachment; filename="{file_path}"')
            msg.attach(part)

    # Configurar el servidor SMTP de Gmail
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Correo enviado con éxito")
    except Exception as e:
        print(f"Error enviando correo: {e}")
