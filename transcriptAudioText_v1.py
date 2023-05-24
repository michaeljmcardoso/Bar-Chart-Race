import speech_recognition as sr

def audio_para_texto(nome_arquivo):
    # Inicializa o reconhecedor de fala
    r = sr.Recognizer()

    # Lê o arquivo de áudio
    with sr.AudioFile(nome_arquivo) as arquivo:
        # Lê o áudio usando o reconhecedor de fala
        audio = r.record(arquivo)

        # Realiza a conversão de áudio para texto
        texto = r.recognize_google(audio, language='pt-BR')

        # Retorna o texto reconhecido
        return texto

# Nome do arquivo de áudio
nome_arquivo_audio = 'audioTest_v1.wav'

# Chama a função de conversão de áudio para texto
texto_reconhecido = audio_para_texto(nome_arquivo_audio)

# Imprime o texto reconhecido
print('O texto reconhecido foi:', texto_reconhecido)
