import os
import subprocess
import venv
from functions import logs, audio, images, screens, keyboards
import threading
import psutil

cpu_percent_logs = 0
cpu_percent_audio = 0
cpu_percent_images = 0
cpu_percent_screens = 0
cpu_percent_keyboards = 0
cpu_percent_trash = 0

def start_logs():
    global cpu_percent_logs  # Variável global para armazenar o consumo de CPU da função start_logs
    cpu_percent_logs = 0

    logs_output = logs.run_module()
    cpu_percent_logs = psutil.cpu_percent(interval=1)  # Atualiza a variável global com o consumo de CPU
    print("\033[1mLogs module:\033[0m", logs_output)
    print("CPU percent (logs):", cpu_percent_logs)

def start_logs():
    global cpu_percent_logs  # Variável global para armazenar o consumo de CPU da função start_logs
    cpu_percent_logs = 0

    logs_output = logs.run_module()
    cpu_percent_logs = psutil.cpu_percent(interval=1)  # Atualiza a variável global com o consumo de CPU
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

def start_trash():
    pass
    # from functions.system import way
    # os_name, _, _ = way()
    # trash_output = None
    # if os_name == "Windows":
    #     from functions.trash import windows
    #     trash_output = windows()
    # elif os_name == "Linux":
    #     from functions.trash import linux
    #     trash_output = linux()
    # else:
    #     trash_output = "Unsupported operating system."
    # print("Trash module:", trash_output)

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
    threads.append(threading.Thread(target=start_trash))

    # Inicie as threads
    for thread in threads:
        thread.start()

    # Aguarde até que todas as threads terminem
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    run_application()