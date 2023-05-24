import speech_recognition as sr

def audio_para_texto(nome_arquivo):
    # Inicializa o reconhecedor de fala
    r = sr.Recognizer()

    # Lê o arquivo de áudio em partes para evitar problemas de memória
    with sr.AudioFile(nome_arquivo) as arquivo:
        # Inicializa a variável para armazenar o texto reconhecido
        texto_reconhecido = ""

        # Define a duração máxima de cada parte em segundos
        duracao_maxima_parte = 30  # 30 segundos

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
                # Ajusta o ruído ambiente antes de gravar a parte do áudio
                r.adjust_for_ambient_noise(fonte)

                # Grava a parte do áudio
                audio = r.record(fonte, duration=fim - inicio, offset=inicio)

            # Realiza a conversão de áudio para texto
            texto_parte = r.recognize_google(audio, language='pt-BR')

            # Adiciona o texto da parte atual ao texto reconhecido
            texto_reconhecido += texto_parte + " "

        # Retorna o texto reconhecido
        return texto_reconhecido

# Nome do arquivo de áudio
nome_arquivo_audio = 'audioText_v2.wav'

# Chama a função de conversão de áudio para texto
texto_reconhecido = audio_para_texto(nome_arquivo_audio)

# Imprime o texto reconhecido
print('O texto reconhecido foi:', texto_reconhecido)
