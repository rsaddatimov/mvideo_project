# Модули для непосредственной отправки сообщений
import smtplib
import ssl

# Модуль для email-объектов
from email.message import EmailMessage

def notify_manager(smtp_server, manager_email, sender_email, sender_password, cam_id):
    notification = "На кассе " + str(cam_id) + " образовалась очередь!"
    
    message = EmailMessage()
    message.set_content(notification)
    message["Subject"] = "Обнаружена очередь на кассе " + str(cam_id)
    message["From"] = sender_email
    message["To"] = manager_email
    
    port = 465 # Для SSL
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as smtp_server:
        smtp_server.login(sender_email, password)
        smtp_server.send_message(message)
        smtp_server.quit()
