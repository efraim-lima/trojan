import cv2
import gridfs
import pymongo
import datetime
import os
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

def videos():
    # Configurações do vídeo
    WIDTH = 640
    HEIGHT = 480
    FPS = 30
    DURATION = 30  # Captura de vídeo a cada 30 segundos

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

    while True:
        start_time = datetime.datetime.now()

        # Nome do arquivo de vídeo com data e hora da captura
        video_filename = start_time.strftime("%Y-%m-%d_%H-%M-%S.mp4")

        out = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*"mp4v"), FPS, (WIDTH, HEIGHT))

        while (datetime.datetime.now() - start_time).total_seconds() < DURATION:
            ret, frame = camera.read()
            if not ret:
                break

            # Salva o frame no arquivo de vídeo
            out.write(frame)

            if cv2.waitKey(1) == ord('q'):
                break

        out.release()

        # Salva o vídeo no GridFS
        with open(video_filename, "rb") as video_file:
            fs.put(video_file, filename=video_filename)

        # Remove o arquivo de vídeo local
        os.remove(video_filename)

        if cv2.waitKey(1) == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

# Iniciar a captura de vídeo
# videos()

if __name__ == "__main__":
    logs_task()