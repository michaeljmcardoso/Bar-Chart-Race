from tkinter import *
from tkinter import filedialog
import speech_recognition as sr

texto_reconhecido = ""  # Variável global para armazenar o texto transcrito

def carregar_arquivo():
    nome_arquivo_audio = filedialog.askopenfilename(filetypes=[("Arquivos de Áudio", "*.wav")])
    if nome_arquivo_audio:
        nome_arquivo["text"] = nome_arquivo_audio

def converter_arquivo():
    global texto_reconhecido  # Utiliza a variável global
    nome_arquivo_audio = nome_arquivo["text"]
    texto_reconhecido = audio_para_texto(nome_arquivo_audio)
    mensagem["text"] = "Áudio convertido com sucesso!"

def salvar_texto_txt():
    nome_arquivo_txt = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivo de Texto", "*.txt")])
    if nome_arquivo_txt:
        with open(nome_arquivo_txt, 'w') as arquivo_txt:
            arquivo_txt.write(texto_reconhecido)
        mensagem["text"] = "Arquivo salvo com sucesso!"

def audio_para_texto(nome_arquivo):
    r = sr.Recognizer()  # Inicializa o reconhecedor de fala

    # Lê o arquivo de áudio em partes para evitar problemas de memória
    with sr.AudioFile(nome_arquivo) as arquivo:
        # Inicializa a variável para armazenar o texto reconhecido
        texto_reconhecido = ""

        # Define a duração máxima de cada parte em segundos
        duracao_maxima_parte = 30

        # Obtém a duração total do áudio
        duracao_total = arquivo.DURATION

        # Calcula o número de partes necessárias
        num_partes = int(duracao_total / duracao_maxima_parte) + 1

        # Realiza a conversão de áudio para texto em cada parte
        for parte in range(num_partes):
            # Define o tempo de início e fim para cada parte
            inicio = parte * duracao_maxima_parte
            fim = min((parte + 1) * duracao_maxima_parte, duracao_total)

            # Cria uma nova instância do AudioFile para cada parte
            parte_arquivo = sr.AudioFile(nome_arquivo)

            # Lê a parte do áudio usando o reconhecedor de fala
            with parte_arquivo as fonte:
                r.adjust_for_ambient_noise(fonte)
                audio = r.record(fonte, duration=fim - inicio, offset=inicio)

            # Realiza a conversão de áudio para texto
            texto_parte = r.recognize_google(audio, language='pt-BR')

            # Adiciona o texto da parte atual ao texto reconhecido
            texto_reconhecido += texto_parte + " "

        # Retorna o texto reconhecido
        return texto_reconhecido


janela = Tk()  # Cria a janela
janela.title("Audio para Texto")  # Título da janela
janela.geometry("500x350")  # Tamanho da janela

botao_carregar = Button(janela, text="Carregar Arquivo", command=carregar_arquivo)  # Cria botão Carregar Arquivo
botao_carregar.grid(column=0, row=0, padx=10, pady=10)  # Posição no grid e espaçamento

nome_arquivo = Label(janela, text="")
nome_arquivo.grid(column=0, row=1, padx=10, pady=10)  # Posição no grid e espaçamento

botao_converter = Button(janela, text="Converter Arquivo", command=converter_arquivo)  # Cria botão Converter Arquivo
botao_converter.grid(column=0, row=2, padx=10, pady=10)  # Posição no grid e espaçamento

mensagem = Label(janela, text="")
mensagem.grid(column=0, row=3, padx=10, pady=10)  # Posição no grid e espaçamento

botao_salvar = Button(janela, text="Salvar", command=salvar_texto_txt)  # Cria botão Salvar
botao_salvar.grid(column=0, row=4, padx=10, pady=10)  # Posição no grid e espaçamento

direitos_autorais = Label(janela, text="@ 2023 Ararajuba Transcrições. Todos os direitos reservados.", font=("Arial", 8))
direitos_autorais.grid(column=0, row=5, padx=10, pady=10)

# Cria a barra de menu
barra_menu = Menu(janela)
janela.config(menu=barra_menu)

# Cria o menu "Arquivo"
menu_arquivo = Menu(barra_menu)
barra_menu.add_cascade(label="Arquivo", menu=menu_arquivo)

# Adiciona as opções no menu "Arquivo"
menu_arquivo.add_separator()
menu_arquivo.add_command(label="Carregar Arquivo", command=carregar_arquivo)
menu_arquivo.add_command(label="Salvar", command=salvar_texto_txt)
menu_arquivo.add_command(label="Sair", command=janela.quit)

janela.mainloop()
