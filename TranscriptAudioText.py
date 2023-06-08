import PySimpleGUI as sg
import speech_recognition as sr
from pydub import AudioSegment
from docx import Document
import time

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
        #r.adjust_for_ambient_noise(source)
        audio_data = r.record(source)

    return r.recognize_google(audio_data, language='pt-BR')

def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:.0f}min {seconds:.0f}s"

def main():
    sg.theme("LightGreen1")

    layout = [
        [sg.Text("Selecione um arquivo de áudio no 'Browse':")],
        [sg.Input(key="-ARQUIVO-"), sg.FileBrowse(file_types=(("Arquivos de Áudio", "*.wav"),))],
        [sg.Button("Converter"), sg.Button("Cancelar")],
        [sg.ProgressBar(100, orientation='h', size=(20, 20), key="-PROGRESSO-")],
        [sg.Text("Tempo decorrido: 0s", key="-TEMPO-")],
        [sg.Text("")],
        [sg.Text("© 2023 Ararajuba Transcrições. Todos os direitos reservados.")]
    ]

    janela = sg.Window("Transcript_Audio_Texto", layout, size=(450, 200), location=(450, 300))

    while True:
        event, values = janela.read()

        if event == sg.WINDOW_CLOSED or event == "Cancelar":
            break

        if event == "Converter":
            audio_file = values["-ARQUIVO-"]
            progress_bar = janela["-PROGRESSO-"]
            tempo_label = janela["-TEMPO-"]


            progress_bar.update(0)
            tempo_label.update("Tempo decorrido: 0min 0s")

            try:
                # Carrega o áudio
                audio = AudioSegment.from_file(audio_file)

                # Divide o áudio em partes de 30 segundos
                audio_chunks = split_audio(audio, 30)

                # Obtém o total de partes
                total_chunks = len(audio_chunks)

                # Variável para armazenar o texto reconhecido
                converted_text = ""

                start_time = time.time()

                for i, chunk in enumerate(audio_chunks, start=1):
                    # Exporta a parte atual como um arquivo WAV
                    chunk.export("temp.wav", format="wav")

                    # Realiza a conversão de áudio para texto
                    text = audio_to_text("temp.wav", progress_bar)

                    # Adiciona o texto reconhecido à variável
                    converted_text += text + " "

                    # Atualiza a barra de progresso
                    progress = int((i / total_chunks) * 100)
                    progress_bar.update(progress)

                    # Atualiza o tempo decorrido
                    elapsed_time = time.time() - start_time
                    elapsed_minutes = elapsed_time /60
                    tempo_label.update(f"Tempo decorrido: {format_time(elapsed_time)}")
                
                # Cria um documento .docx
                document = Document()
                document.add_paragraph(converted_text)
                #document.save("texto_reconhecido.docx")  # salvamento automático ou direto

                sg.popup("Conversão concluída com sucesso!", "Clique em OK para salvar o arquivo de texto.")

                # Janela para definir o diretório e o nome do arquivo antes de salvar
                save_layout = [
                    [sg.Text("Escolha uma pasta no 'Browse' para salvar:")],
                    [sg.Input(key="-DIRETORIO-"), sg.FolderBrowse(target="-DIRETORIO-")],
                    [sg.Text("Forneça um nome para o arquivo:")],
                    [sg.Input(key="-NOME-"), sg.Text(".docx")],
                    [sg.Button("Salvar")],
                    [sg.Text("")],  # cria espaçamento
                    [sg.Text("© 2023 Ararajuba Transcrições. Todos os direitos reservados.")]
                ]

                save_window = sg.Window("Salvar Arquivo", save_layout, size=(450, 200), location=(485, 345))

                while True:
                    save_event, save_values = save_window.read()

                    if save_event == sg.WINDOW_CLOSED or save_event == "Cancelar":
                        break

                    if save_event == "Salvar":
                        directory = save_values["-DIRETORIO-"]
                        filename = save_values["-NOME-"]

                        # Verifica se o diretório e o nome do arquivo foram fornecidos
                        if directory and filename:
                            document.save(f"{directory}/{filename}.docx")
                            elapsed_time = time.time() - start_time
                            elapsed_minutes = elapsed_time / 60
                            sg.popup("Arquivo salvo com sucesso! Tempo decorrido: {format_time(elapsed_minutes)}")
                            break
                        else:
                            sg.popup("Por favor, selecione um diretório e forneça um nome para o arquivo.")

                save_window.close()

            except Exception as e:
                sg.popup("Ocorreu um erro durante a conversão de áudio para texto.", str(e))

    janela.close()

if __name__ == "__main__":
    main()
