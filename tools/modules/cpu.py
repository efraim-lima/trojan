import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# Certifique-se de que o diretório do projeto esteja no sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psutil
import time
from database import collection_cpu, today, hour

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

def calculate_total_memory_usage():
    modules = ["audio", "video", "logs", "screens", "images", "keyboards"]  # Adicione aqui os nomes dos módulos que deseja monitorar

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        total_memory_usage = 0
        module_data = []

        for module in modules:
            module_memory = psutil.Process().memory_info().rss
            total_memory_usage += module_memory
            module_data.append({"module": module, "memory_usage": module_memory})

        total_system_memory = psutil.virtual_memory().total
        total_memory_usage_percent = (total_memory_usage / total_system_memory) * 100

        print(f"Uso total de memória do sistema: {total_memory_usage / (1024 * 1024)} MB")
        print(f"Porcentagem de uso de memória do sistema: {total_memory_usage_percent}%")

        # Atualize o MongoDB com os dados
        collection_cpu.insert_one({
            "date":today,
            "hour":hour,
            "modules": module_data, 
            "total_memory_usage": total_memory_usage, 
            "total_memory_usage_percent": total_memory_usage_percent}
                                  )

        # Aguarde um intervalo de tempo entre as atualizações
        time.sleep(1)
        
        return total_memory_usage_percent

if __name__ == "__main__":
    calculate_total_memory_usage()
