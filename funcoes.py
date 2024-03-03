import PySimpleGUI as sg
import speech_recognition as sr
from datetime import datetime
import datetime
import sys

ano_atual = datetime.datetime.now().year

def audio_to_text(audio_file, progress_bar):
    r = sr.Recognizer()
    # Definir o limiar de energia antes de iniciar o reconhecimento
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
    # Obtém a data atual
    today = datetime.datetime.now().date()

    # Obtém a data de expiração da licença
    expiration_date = datetime.datetime.strptime("2024-12-31", "%Y-%m-%d").date()  # prazo da licença

    # Verifica se a licença está expirada
    if today > expiration_date:
        sg.popup_error("Licença expirada. Entre em contato para renovar: "
                       "(98)98895-7452"
                       "\nPrazo da licença: 90 Dias\nInício: 0000-00-00")
        sys.exit(1)

    # Verifica se a licença está próxima da expiração (3 dias de antecedência)
    warning_date_15 = expiration_date - datetime.timedelta(days=15)
    warning_date = expiration_date - datetime.timedelta(days=3)

    if today == expiration_date:
        message = ("Hoje é o último dia da sua licença. Entre em contato para renovar: "
                   "(98)98895-7452")
    elif today >= warning_date:
        remaining_days = (expiration_date - today).days
        if remaining_days == 1:
            message = ("Amanhã é o último dia da sua licença. Entre em contato para renovar: "
                       "(98)98895-7452")
        else:
            message = (f"Sua licença expirará em {remaining_days} dias. Entre em contato para renovar: "
                       f"(98)98895-7452")
    elif today == warning_date_15:
        remaining_days = (expiration_date - today).days
        message = (f"Sua licença expirará em {remaining_days} dias. Entre em contato para renovar: "
                   f"(98)98895-7452")
    else:
        message = None

    if message:
        sg.popup(message)
