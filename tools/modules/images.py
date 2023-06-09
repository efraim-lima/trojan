import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# Certifique-se de que o diretório do projeto esteja no sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import cv2
import datetime
from modules.database import collection_image, hour, today
import time
import atexit
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
    
# Função para capturar e salvar imagens
def save_image(frame):
    # Gerar o nome do arquivo com base na data e hora atual
    capture_time = datetime.datetime.now()
    filename = f"image_{capture_time.strftime('%Y%m%d_%H%M%S')}.jpg"
    
    # Salvar a imagem no formato JPEG para avaliação posterior
    # cv2.imwrite(filename, frame)
    
# Função para capturar imagens da câmera
def images():
    # Criação do objeto VideoCapture com a flag CAP_DSHOW
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    # Configurações da câmera
    camera.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
    camera.set(cv2.CAP_PROP_EXPOSURE, -6)
    
    # Inicializar o tempo atual
    current_time = time.time()
    
    # Definir uma função de saída para lidar com o desligamento do sistema
    def exit_handler():
        nonlocal camera
        
        if camera is not None:
            camera.release()
    
    # Registrar a função de saída para ser chamada no desligamento do sistema
    atexit.register(exit_handler)
    
    while True:
        ret, frame = camera.read()
        if not ret:
            break

        # Obter o tempo atual
        now = time.time()
        
        # Verificar se passaram 30 segundos
        if now - current_time >= 30:
            # Salvar a imagem no banco de dados
            # Gerar o nome do arquivo e a tag para identificar o dia
            capture_time = datetime.datetime.now()
            name = capture_time.strftime("%Y%m%d_%H%M%S")
            tag = capture_time.strftime("%Y%m%d")

            # Lógica para salvar as imagens no banco de dados
            # Aqui está um exemplo de como salvar as imagens em uma coleção específica
            # Criar um nome de arquivo com a data e hora da captura
            filename = f"image_{name}.jpg"
            
            # Salvar a imagem no MongoDB
            _, jpeg_image = cv2.imencode(".jpg", frame)
            jpeg_image_data = jpeg_image.tobytes()
            
            image_data = {
                "date":today,
                "hour":hour,
                "filename": filename, 
                "image": jpeg_image_data, 
                "tag": tag
                }
            collection_image.insert_one(image_data)
            
            # Salvar a imagem localmente para visualização
            save_image(frame)
            
            # Atualizar o tempo atual para a próxima captura
            current_time = now
        
    camera.release()
# Iniciar a captura de imagens
images()

if __name__ == "__main__":
    logs_task()
