import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# Certifique-se de que o diretório do projeto esteja no sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pyaudio
import datetime
from modules.database import fs_audio as fs
from modules.database import today, hour
import io
import signal
import time
import time
import psutil

def clear_terminal():
    """Limpa o terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def logs_task():
    for _ in range(10):
        # Simulação de tarefa de áudio
        time.sleep(1)
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        print(f"Uso de CPU: {cpu_percent}%")
        print(f"Uso de memória: {memory_percent}%")
        clear_terminal()

# Configurações de gravação
CHUNK = 1024  # Tamanho do buffer de gravação
FORMAT = pyaudio.paInt16  # Formato de áudio
CHANNELS = 1  # Número de canais de áudio (mono)
RATE = 44100  # Taxa de amostragem (sample rate)
DURATION = 30  # Duração da gravação em segundos
SAVE_INTERVAL = 30  # Intervalo de salvamento em segundos

# Variáveis de controle
recording = False  # Flag para controlar a gravação contínua

# Função para gravar áudio do microfone por uma determinada duração
def audio():
    global recording

    while True:
        audio = pyaudio.PyAudio()

        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)

        frames = []
        num_frames = int(RATE / CHUNK * DURATION)

        for i in range(num_frames):
            if not recording:
                break
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Converter os frames de áudio em um objeto BytesIO
        audio_data = io.BytesIO(b''.join(frames))

        # Gerar o nome do arquivo e a tag para identificar o dia
        current_time = datetime.datetime.now()
        name = current_time.strftime("%Y%m%d_%H%M%S")
        tag = current_time.strftime("%Y%m%d")

        # Salvar os dados de áudio no MongoDB com o nome do arquivo e a tag
        fs.put(audio_data, filename=name, encoding='utf-8', tag=tag, date=today, hour=hour)

        print("Gravação concluída e salva no MongoDB!")

        # Verificar se a gravação deve continuar
        if not recording:
            break

        # Aguardar até o próximo intervalo de salvamento
        for _ in range(SAVE_INTERVAL):
            if not recording:
                break
            time.sleep(1)

def exit_handler(signal, frame):
    global recording
    if recording:
        recording = False
        print("Parando a gravação e salvando o áudio restante...")
        time.sleep(2)  # Aguardar um tempo para garantir a conclusão da gravação
    print("Saindo do programa")

# Definir o manipulador de sinal para lidar com o encerramento do programa
signal.signal(signal.SIGINT, exit_handler)
signal.signal(signal.SIGTERM, exit_handler)

# Iniciar a gravação contínua
recording = True
audio()

if __name__ == "__main__":
    logs_task()