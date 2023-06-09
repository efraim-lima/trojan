import pyaudio
import datetime
import pymongo
import gridfs
import wave
import os
import shutil
import atexit
import signal
import time

# Configurações de gravação
CHUNK = 1024  # Tamanho do buffer de gravação
FORMAT = pyaudio.paInt16  # Formato de áudio
CHANNELS = 1  # Número de canais de áudio (mono)
RATE = 44100  # Taxa de amostragem (sample rate)
DURATION = 30  # Duração da gravação em segundos
SAVE_INTERVAL = 30  # Intervalo de salvamento em segundos
CACHE_CLEAN_INTERVAL = 60  # Intervalo de limpeza do cache em segundos

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
cache_cleaned = False  # Flag para controlar a limpeza do cache

# Função para gravar áudio do microfone por uma determinada duração
def record_audio():
    global recording
    global cache_cleaned

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

        # Salvar o áudio em formato WAV
        current_time = datetime.datetime.now()
        filename = current_time.strftime("%Y%m%d_%H%M%S") + ".wav"
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        # Ler o arquivo WAV e salvar no MongoDB
        with open(filename, 'rb') as file:
            fs.put(file, filename=filename)

        print("Gravação concluída e salva no MongoDB!")

        # Limpar o cache a cada CACHE_CLEAN_INTERVAL segundos
        if not cache_cleaned:
            clean_cache()
            cache_cleaned = True

        # Verificar se a gravação deve continuar
        if not recording:
            break

        # Aguardar até o próximo intervalo de salvamento
        for _ in range(SAVE_INTERVAL):
            if not recording:
                break
            time.sleep(1)

def clean_cache():
    cache_dir = os.path.join(os.getcwd(), "__pycache__")
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
        print("Cache limpo")

def exit_handler():
    global recording
    if recording:
        recording = False
        print("Parando a gravação e salvando o áudio restante...")
        time.sleep(2)  # Aguardar um tempo para garantir a conclusão da gravação

    # Enviar o áudio imediatamente para o banco de dados
    clean_cache()
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".wav"):
            with open(filename, 'rb') as file:
                fs.put(file, filename=filename)
            os.remove(filename)
            print("Áudio", filename, "enviado para o MongoDB e excluído.")

    print("Saindo do programa")

# Definir o manipulador de sinal para lidar com o encerramento do programa
signal.signal(signal.SIGINT, exit_handler)
signal.signal(signal.SIGTERM, exit_handler)

# Registrar a função de limpeza do cache para ser chamada no final
atexit.register(clean_cache)

# Iniciar a gravação contínua
recording = True
record_audio()