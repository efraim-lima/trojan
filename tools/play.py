import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# Certifique-se de que o diretório do projeto esteja no sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import subprocess
import venv
from modules import logs, audio, images, screens, keyboards, network
from modules.database import today
import threading
import psutil

cpu_percent_logs = 0
cpu_percent_audio = 0
cpu_percent_images = 0
cpu_percent_screens = 0
cpu_percent_keyboards = 0
cpu_percent_network = 0
cpu_percent_trash = 0

def start_logs():
    global cpu_percent_logs
    cpu_percent_logs = 0

    logs_output = logs.run_module()
    cpu_percent_logs = psutil.cpu_percent(interval=1)
    print("\033[1mLogs module:\033[0m", logs_output)
    print("CPU percent (logs):", cpu_percent_logs)

def start_audio():
    global cpu_percent_audio
    cpu_percent_audio = 0

    audio_output = audio.audio()
    cpu_percent_audio = psutil.cpu_percent(interval=1)
    print("\033[1mAudio module:\033[0m", audio_output)
    print("CPU percent (audio):", cpu_percent_audio)

def start_images():
    global cpu_percent_images
    cpu_percent_images = 0

    images_output = images.images()
    cpu_percent_images = psutil.cpu_percent(interval=1)
    print("\033[1mImages module:\033[0m", images_output)
    print("CPU percent (images):", cpu_percent_images)

def start_screens():
    global cpu_percent_screens
    cpu_percent_screens = 0

    screens_output = screens.screens(duration=30, interval=0)
    cpu_percent_screens = psutil.cpu_percent(interval=1)
    print("\033[1mScreens module:\033[0m", screens_output)
    print("CPU percent (screens):", cpu_percent_screens)

def start_keyboards():
    global cpu_percent_keyboards
    cpu_percent_keyboards = 0

    keyboards_output = keyboards.run_module()
    cpu_percent_keyboards = psutil.cpu_percent(interval=1)
    print("\033[1mKeyboards module:\033[0m", keyboards_output)
    print("CPU percent (keyboards):", cpu_percent_keyboards)

def start_network():
    global cpu_percent_network
    cpu_percent_network = 0

    last_run_date = load_last_run_date()  # Carrega a última data de execução do arquivo ou variável

    if today != last_run_date:  # Verifica se a data atual é diferente da última data de execução
        network_output = network.check_ports("localhost", 1, 65535)
        cpu_percent_network = psutil.cpu_percent(interval=1)
        print("\033[1mNetwork module:\033[0m", network_output)
        print("CPU percent (network):", cpu_percent_network)

        save_last_run_date(today)  # Salva a data atual como a última data de execução

def save_last_run_date(date_str):
    with open("last_run_date.txt", "w") as file:
        file.write(date_str)

def load_last_run_date():
    if os.path.isfile("last_run_date.txt"):
        with open("last_run_date.txt", "r") as file:
            return file.read().strip()
    else:
        # Se o arquivo não existir, retorna uma data antiga para garantir que a função seja executada no primeiro dia
        return "2000-01-01"

def start_trash():
    # from system import way
    # os_name, _, _ = way()
    # trash_output = None
    # if os_name == "Windows":
    #     from trash import windows
    #     trash_output = windows()
    # elif os_name == "Linux":
    #     from trash import linux
    #     trash_output = linux()
    # else:
    #     trash_output = "Unsupported operating system."
    # print("Trash module:", trash_output)
    pass

def check_venv_exists():
    venv_dir = os.path.join(os.getcwd(), "venv")
    return os.path.exists(venv_dir)

def create_venv():
    venv_dir = os.path.join(os.getcwd(), "venv")
    os.makedirs(venv_dir, exist_ok=True)
    venv.create(venv_dir, with_pip=True)

def check_requirements_installed():
    installed_modules = subprocess.check_output(["venv/Scripts/pip", "freeze"]).decode().split("\n")
    with open("requirements.txt", "r") as requirements_file:
        required_modules = requirements_file.read().split("\n")
    return all(module in installed_modules for module in required_modules)

def install_requirements():
    subprocess.run(["venv/Scripts/pip", "install", "-r", "requirements.txt"])

def run_application():
    if not check_venv_exists():
        create_venv()

    if not check_requirements_installed():
        install_requirements()

    # Inicie as threads para cada módulo
    threads = []
    threads.append(threading.Thread(target=start_logs))
    threads.append(threading.Thread(target=start_audio))
    threads.append(threading.Thread(target=start_images))
    threads.append(threading.Thread(target=start_screens))
    threads.append(threading.Thread(target=start_keyboards))
    threads.append(threading.Thread(target=start_network))
    threads.append(threading.Thread(target=start_trash))

    # Inicie as threads
    for thread in threads:
        thread.start()

    # Aguarde até que todas as threads terminem
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    run_application()
