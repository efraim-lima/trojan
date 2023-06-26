import pyaudio
import datetime
import pymongo
import gridfs
import io
import signal
import time

import time
import psutil

def logs_task():
    for _ in range(10):
        # Simulação de tarefa de áudio
        time.sleep(1)
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        print(f"Uso de CPU: {cpu_percent}%")
        print(f"Uso de memória: {memory_percent}%")

# Configurações de gravação
CHUNK = 1024  # Tamanho do buffer de gravação
FORMAT = pyaudio.paInt16  # Formato de áudio
CHANNELS = 1  # Número de canais de áudio (mono)
RATE = 44100  # Taxa de amostragem (sample rate)
DURATION = 30  # Duração da gravação em segundos
SAVE_INTERVAL = 30  # Intervalo de salvamento em segundos

# Conectar ao banco de dados MongoDB
try:
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["mydatabase"]
    collection = db.get_collection("audio_data")
    if collection is None:
        collection = db.create_collection("audio_data")
except pymongo.errors.ConnectionError as e:
    print("Erro ao conectar ao MongoDB:", e)
    # Lógica para lidar com o erro de conexão, se necessário
fs = gridfs.GridFS(db, collection="audio_data")

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
        fs.put(audio_data, filename=name, encoding='utf-8', tag=tag)

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