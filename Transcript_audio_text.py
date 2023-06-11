import PySimpleGUI as sg
import speech_recognition as sr
from pydub import AudioSegment
from docx import Document
import nltk
from nltk.tokenize import sent_tokenize
# nltk.download('punkt') # baixar os recursos necessários na primeira execução

import time
import datetime

ano_atual = datetime.datetime.now().year

def split_audio(audio, duration):
    chunks = []
    for i in range(0, len(audio), duration * 1000):
        chunk = audio[i:i + duration * 1000]
        chunks.append(chunk)
    return chunks

def audio_to_text(audio_file, progress_bar):
    r = sr.Recognizer()
    audio = sr.AudioFile(audio_file)

    with audio as source:
        audio_data = r.record(source)

    return r.recognize_google(audio_data, language='pt-BR')

def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:.0f}min {seconds:.0f}s"

def main():
    sg.theme('DarkGreen')
    sg.popup("Olá, bem-vindo ao conversor de áudio para texto.", "Vamos começar!")

    layout = [
        [sg.Text("Digite o nome do arquivo de áudio (.wav) ou selecione no 'Browse':", font=("Helvetica", 11))],
        [sg.Input(key="-ARQUIVO-"), sg.FileBrowse(file_types=(("Arquivos de Áudio", "*.wav"), ))],
        [sg.Button("Converter", button_color=("white", "green")), sg.Button("Cancelar", button_color=("white", "green"))],
        [sg.ProgressBar(100, orientation='h', size=(20, 20), key="-PROGRESSO-")],
        [sg.Text("Tempo decorrido: 0s", font=("Helvetica", 11), key="-TEMPO-")],
        [sg.Text("_" * 65)],
        [sg.Text(f"© {ano_atual} Ararajuba Transcrições. Todos os direitos reservados.", font=("Helvetica", 8))]
    ]

    janela = sg.Window("Transcript_Audio_Texto", layout, size=(462, 200), location=(450, 300),
                       icon="/home/import_michael/PycharmProjects/interface_programas/icon3.png")

    while True:
        event, values = janela.read(timeout=100)
        if event == sg.WINDOW_CLOSED or event == "Cancelar":
            janela.close()
            return

        if event == "Converter":
            audio_file = values["-ARQUIVO-"]
            progress_bar = janela["-PROGRESSO-"]
            tempo_label = janela["-TEMPO-"]
            if not audio_file:
                sg.popup("Por favor, selecione um arquivo (.wav).")
            else:
                sg.popup('Isso pode levar alguns minutos.', 'Aguarde enquanto convertemos seu arquivo.', auto_close=(True))

            progress_bar.update(0)
            tempo_label.update("Tempo decorrido: 0s")

            try:
                audio = AudioSegment.from_file(audio_file)
                audio_chunks = split_audio(audio, 30)
                total_chunks = len(audio_chunks)
                converted_text = ""

                start_time = time.time()

                for i, chunk in enumerate(audio_chunks, start=1):

                    chunk.export("temp.wav", format="wav")
                    text = audio_to_text("temp.wav", progress_bar)
                    converted_text += text + " "

                    # Adiciona pontuação ao texto
                    converted_text = converted_text.strip() + "."

                    # Adiciona pontuação ao texto
                    converted_text = converted_text.strip() + "."

                    # Divide o texto em sentenças
                    sentences = sent_tokenize(converted_text)

                    # Separa as sentenças em parágrafos
                    paragraphs = []
                    current_paragraph = []
                    for sentence in sentences:
                        if sentence.strip():  # Ignora sentenças vazias
                            current_paragraph.append(sentence)
                        elif current_paragraph:  # Cria um novo parágrafo quando encontra uma sentença vazia
                            paragraphs.append(" ".join(current_paragraph))
                            current_paragraph = []
                    if current_paragraph:  # Adiciona o último parágrafo, se existir
                        paragraphs.append(" ".join(current_paragraph))

                    progress = int((i / total_chunks) * 100)
                    progress_bar.update(progress)

                    elapsed_time = time.time() - start_time
                    tempo_label.update(f"Tempo decorrido: {format_time(elapsed_time)}")

                    event, values = janela.read(timeout=100)
                    if event == sg.WINDOW_CLOSED or event == "Cancelar":
                        janela.close()
                        return

                    janela.refresh()

                document = Document()
                document.add_paragraph(converted_text)

                sg.popup("Conversão concluída com sucesso!", "Clique em OK para salvar o arquivo de texto.")

                save_layout = [
                    [sg.Text("Escolha uma pasta no 'Browse' para salvar:", font=("Helvetica", 11))],
                    [sg.Input(key="-DIRETORIO-"), sg.FolderBrowse(target="-DIRETORIO-")],
                    [sg.Text("Forneça um nome para o arquivo:", font=("Helvetica", 11))],
                    [sg.Input(key="-NOME-"), sg.Text(".docx")],
                    [sg.Button("Salvar")],
                    [sg.Text("_" * 60)],
                    [sg.Text(f"© {ano_atual} Ararajuba Transcrições. Todos os direitos reservados.", font=("Helvetica", 8))]
                ]

                save_window = sg.Window("Salvar Arquivo", save_layout, size=(455, 200), location=(485, 345))

                while True:
                    save_event, save_values = save_window.read(timeout=100)

                    if save_event == sg.WINDOW_CLOSED or save_event == "Cancelar":
                        break

                    if save_event == "Salvar":
                        directory = save_values["-DIRETORIO-"]
                        filename = save_values["-NOME-"]

                        if directory and filename:
                            document.save(f"{directory}/{filename}.docx")
                            sg.popup("Arquivo salvo com sucesso!")
                            break
                        else:
                            sg.popup("Por favor, selecione um diretório e forneça um nome para o arquivo.")

                    save_window.refresh()

                save_window.close()

            except Exception as e:
                sg.popup("Ocorreu um erro durante a conversão de áudio para texto.", str(e))

    janela.close()

if __name__ == "__main__":
    main()
