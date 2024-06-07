import PySimpleGUI as sg
import speech_recognition as sr
import time
import datetime
from pydub import AudioSegment
from docx import Document
from funcoes import check_license, audio_to_text, format_time, ano_atual


def split_audio(audio, duration):
    chunks = []

    for i in range(0, len(audio), duration * 1000):
        chunk = audio[i:i + duration * 1000]
        chunks.append(chunk)

    return chunks


def main():
    check_license()

    sg.theme('DarkBlack')
    #sg.popup("Olá. O que vamos transcrever hoje!", title="")

    layout = [
        [sg.Text("Digite o nome do arquivo de áudio (.wav) ou selecione no 'Browse':", font=("Helvetica", 11))],
        [sg.Input(key="-ARQUIVO-"), sg.FileBrowse(file_types=(("Arquivos de Áudio", "*.wav"), ))],
        [sg.Button("Converter", button_color=("white", "green")), sg.Button("Cancelar", button_color=("white", "green"))],
        [sg.ProgressBar(100, orientation='h', size=(20, 20), key="-PROGRESSO-")],
        [sg.Text("Tempo decorrido: 0s", font=("Helvetica", 11), key="-TEMPO-")],
        [sg.Text("_" * 65, font=("bold"))],
        [sg.Text(f"© {ano_atual} Desenvolvido por Michael JM Cardoso.", font=("Helvetica", 8, "bold"), text_color='white')]
    ]

    janela = sg.Window("Transcript_Audio_Texto", layout, size=(462, 200), location=(450, 300), icon='/home/import_michael/Imagens/icon3.png')

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
                sg.popup('Iniciando Transcrição.', title="Carregando...", auto_close=(True))

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

                    try:
                        text = audio_to_text("temp.wav", progress_bar)
                        converted_text += text + " "

                    except sr.UnknownValueError:
                        converted_text += f"<Erro: Não foi possível transcrever esta parte do áudio> "

                    except sr.RequestError as e:
                        converted_text += f"<Erro: Não foi possível conectar à API do Google: {e}> "

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

                sg.popup("Conversão concluída com sucesso!", "Clique em OK para salvar.", title="Sucesso", font=("Helvetica", 10, "bold"))

                save_layout = [
                    [sg.Text("Escolha uma pasta no 'Browse' para salvar:", font=("Helvetica", 11))],
                    [sg.Input(key="-DIRETORIO-"), sg.FolderBrowse(target="-DIRETORIO-")],
                    [sg.Text("Forneça um nome para o arquivo:", font=("Helvetica", 11))],
                    [sg.Input(key="-NOME-"), sg.Text(".docx")],
                    [sg.Button("Salvar")],
                    [sg.Text("_" * 60)],
                    [sg.Text(f"© {ano_atual} Desenvolvido por Michael JM Cardoso. Todos os direitos reservados.", font=("Helvetica", 8, "bold"))]
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

                            janela["-ARQUIVO-"].update("")

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