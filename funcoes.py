import PySimpleGUI as sg
import speech_recognition as sr
from datetime import datetime
import datetime
import sys

ano_atual = datetime.datetime.now().year

def audio_to_text(audio_file, progress_bar):
    r = sr.Recognizer()
    r.energy_threshold = 100

    audio = sr.AudioFile(audio_file)

    with audio as source:
        r.adjust_for_ambient_noise(source)
        audio_data = r.record(source)

    return r.recognize_google(audio_data, language='pt-BR')

def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60

    return f"{minutes:.0f}min {seconds:.0f}s"


def check_license():
    today = datetime.datetime.now().date()

    expiration_date = datetime.datetime.strptime("2024-12-31", "%Y-%m-%d").date()  # prazo da licença

    if today > expiration_date:
        sg.popup_error("Entre em contato para renovar:", "Whatsapp => (98) 98895-7452", "Email => michaeljmc@outlook.com.br", "Prazo da licença: 90 Dias", "Início: 0000-00-00", 
                       title="Licença expirada", 
                       font=("Helvetica", 11, "bold"))
        
        sys.exit(1)

    warning_date_15 = expiration_date - datetime.timedelta(days=15)
    warning_date = expiration_date - datetime.timedelta(days=3)

    if today == expiration_date:
        sg.popup("Entre em contato para renovar:", "Whatsapp => (98) 98895-7452", "Email => michaeljmc@outlook.com.br", 
                 title="Sua licença expira hoje", 
                 font=("Helvetica", 11, "bold"))
        
    elif today >= warning_date:
        remaining_days = (expiration_date - today).days

        if remaining_days == 1:
            sg.popup("Entre em contato para renovar:", "Whatsapp => (98) 98895-7452", "Email => michaeljmc@outlook.com.br", 
                     title="Sua licença expira amanhã", 
                     font=("Helvetica", 11, "bold"))
            
        else:
            sg.popup(f"Sua licença expirará em {remaining_days} dias.", "Entre em contato para renovar:",
                       f"Whatsapp - (98) 98895-7452", "Email - michaeljmc@outlook.com.br", 
                       title="Aviso", 
                       font=("Helvetica", 11, "bold"))
            
    elif today == warning_date_15:
        remaining_days = (expiration_date - today).days

        sg.popup(f"Sua licença expirará em {remaining_days} dias.", "Entre em contato para renovar:",
                   f"Whatsapp - (98) 98895-7452", "Email - michaeljmc@outlook.com.br", 
                   title="Aviso", 
                   font=("Helvetica", 11, "bold"))
        
    else:
        None