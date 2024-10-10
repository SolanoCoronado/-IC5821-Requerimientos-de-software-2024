import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_correo_gmail(subject, body, recipients):
    # Configuración del servidor SMTP
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = 'dummyonlymail@gmail.com'  # Reemplaza con tu correo de Gmail
    smtp_password = 'fjmt uses qjdw gqqg'  # Reemplaza con tu contraseña de aplicación (no la contraseña de Gmail)
    
    # Configurar el mensaje del correo electrónico
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Conexión al servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Inicia TLS para asegurar la conexión
        server.login(smtp_username, smtp_password)  # Inicia sesión en el servidor SMTP

        # Enviar el correo
        server.sendmail(smtp_username, recipients, msg.as_string())
        server.quit()

        print('Correo enviado con éxito')
        return True
    except Exception as e:
        print(f'Error al enviar el correo: {str(e)}')
        return False

if __name__ == "__main__":
    # Ejemplo de uso de la función para enviar un correo
    destinatario = ['**************']  # Reemplaza con el correo del destinatario
    asunto = 'Hola desde Python'
    cuerpo = 'Este es un mensaje de prueba enviado desde un script Python usando Gmail.'

    resultado = enviar_correo_gmail(asunto, cuerpo, destinatario)
    if resultado:
        print("Correo enviado exitosamente.")
    else:
        print("Error al enviar el correo.")
