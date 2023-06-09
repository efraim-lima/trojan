import os
import sys
import re

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# Certifique-se de que o diretório do projeto esteja no sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import atexit
from pynput import keyboard
from modules.database import collection_keyboard, today, hour
import time
import datetime
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

def analyze_typing(text):
    pattern = r"\b\w{2,}\b"
    created_words = re.findall(pattern, text)
    return created_words

# Variáveis para o nome do arquivo e a tag do dia
name_list = []
words_list = []

def save_keyboards(keys):
    # Transformar a lista de teclas em uma string
    keys_str = ' '.join(keys)

    # Obter a data e hora atual
    current_time = datetime.datetime.now()

    # Obter o nome do arquivo
    global name_list
    if not name_list:
        name = current_time.strftime("%Y%m%d_%H%M%S")
        name_list.append(name)
    else:
        name = name_list[0]

    # Obter todas as palavras digitadas
    global words_list

    # Inserir o documento no banco de dados
    data = {
        "date":today,
        "hour":hour,
        'filename': name,
        'timestamp': current_time,
        'keys_list': keys,
        'keys_str': keys_str,
        'words': len(words_list)
    }
    collection_keyboard.insert_one(data)

def on_press(key):
    global keys
    if key == keyboard.Key.space:
        print(key)
        keys.append(" ")  # Adicionar espaço à lista de teclas
        words_list.append(" ")  # Adicionar espaço à lista de palavras
    elif hasattr(key, 'char'):
        print(key)
        keys.append(key.char)
        words_list.append(key.char)
    else:
        print(key)
        keys.append(str(key))
        words_list.append(str(key))

keys = []  # Lista para armazenar as teclas digitadas

# Configurar o intervalo de tempo para capturar as teclas
interval = 30  # Capturar as teclas a cada 30 segundos

# Iniciar a captura de eventos de teclado
keyboard_listener = keyboard.Listener(on_press=on_press)
keyboard_listener.start()

# Definir uma função de saída para lidar com o desligamento do sistema
def exit_handler():
    # Verificar se existem teclas capturadas
    if keys:
        # Salvar as teclas no banco de dados
        save_keyboards(keys)

    # Parar a captura de eventos de teclado
    keyboard_listener.stop()


# Registrar a função de saída para ser chamada no desligamento do sistema
atexit.register(exit_handler)


# Loop principal
try:
    while True:
        # Aguardar o intervalo de tempo
        time.sleep(interval)

        # Verificar se existem teclas capturadas
        if keys:
            # Salvar as teclas no banco de dados
            save_keyboards(keys)

            # Limpar a lista de teclas
            keys = []

except KeyboardInterrupt:
    # Ignorar a exceção KeyboardInterrupt e continuar o programa
    pass
