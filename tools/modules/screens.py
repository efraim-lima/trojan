import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# Certifique-se de que o diretório do projeto esteja no sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import datetime
import cv2
import pyautogui
import numpy as np
import time
from modules.database import fs_imagesII, fs_videos, fs_audio, today, hour
from screeninfo import get_monitors
import pyaudio
import win32api
import wave
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
# Conectar ao banco de dados MongoDB

def capture_audio(output_filename, duration):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    frames = []
    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Salvar o áudio localmente
    os.rename(output_filename, os.path.join(".", output_filename))

    # Salvar o áudio no GridFS
    with open(output_filename, "rb") as audio_file:
        fs_audio.put(audio_file, filename=output_filename, date=today, hour=hour)

def capture_video(output_filename, duration):
    # Configurações do vídeo
    WIDTH = 1920
    HEIGHT = 1080
    FPS = 30

    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds=duration)

    video_writer = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc(*"mp4v"), FPS, (WIDTH, HEIGHT))

    while datetime.datetime.now() < end_time:
        screenshot = pyautogui.screenshot()
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        video_writer.write(frame)

        elapsed_time = datetime.datetime.now() - start_time
        if elapsed_time.total_seconds() >= duration:
            break

        time.sleep(1/FPS)  # Aguardar o intervalo correto entre os frames

    video_writer.release()

    # Salvar o vídeo no GridFS
    with open(output_filename, "rb") as video_file:
        fs_videos.put(video_file, filename=output_filename, date=today, hour=hour)

# Função para verificar o estado do monitor (standby ou ativo)
def is_monitor_active():
    power_info = win32api.GetSystemPowerStatus()
    if 'ACLineStatus' in power_info:
        return power_info['ACLineStatus'] == 0x00000000  # 0x00000000 significa em uso
    return False

# Função para capturar as telas do computador intermitentemente
def screens(duration, interval):
    while True:
        start_time = datetime.datetime.now()
        print("Iniciando captura:", start_time)

        # Definir o nome do arquivo com data e hora da captura
        base_filename = start_time.strftime("%Y-%m-%d_%H-%M-%S")

        # Capturar áudio
        audio_filename = base_filename + "_audio.wav"
        print("Capturando áudio:", audio_filename)
        capture_audio(audio_filename, duration)

        # Capturar vídeo
        video_filename = base_filename + "_video.mp4"
        print("Capturando vídeo:", video_filename)
        capture_video(video_filename, duration)

        # Capturar a tela em todos os monitores
        screenshots = []
        for monitor in get_monitors():
            screenshot = pyautogui.screenshot(region=(monitor.x, monitor.y, monitor.width, monitor.height))
            screenshots.append(screenshot)

        # Salvar as imagens localmente
        for i, screenshot in enumerate(screenshots):
            image_filename = base_filename + f"_screen_{i+1}.png"
            screenshot.save(image_filename)
            # Salvar as imagens no GridFS
            with open(image_filename, "rb") as image_file:
                fs_imagesII.put(image_file, filename=image_filename, date=today, hour=hour)
            # Remover as imagens locais
            os.remove(image_filename)

        elapsed_time = datetime.datetime.now() - start_time
        print("Tempo decorrido:", elapsed_time.total_seconds())
        if elapsed_time.total_seconds() < duration:
            time.sleep(duration - elapsed_time.total_seconds())

# Iniciar a captura de telas, vídeos e áudio intermitentemente
screens(duration=30, interval=0)

if __name__ == "__main__":
    logs_task()