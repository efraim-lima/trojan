import os
import psutil
import time
from pymongo import MongoClient

def calculate_total_memory_usage():
    modules = ["audio", "video", "logs", "screens", "images", "keyboards"]  # Adicione aqui os nomes dos módulos que deseja monitorar

    client = MongoClient()
    db = client["time_series"]
    collection = db["cpu"]

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
        collection.insert_one({"modules": module_data, "total_memory_usage": total_memory_usage, "total_memory_usage_percent": total_memory_usage_percent})

        # Aguarde um intervalo de tempo entre as atualizações
        time.sleep(1)
        
        return total_memory_usage_percent

if __name__ == "__main__":
    calculate_total_memory_usage()
