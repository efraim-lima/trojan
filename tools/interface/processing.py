import datetime
from pymongo import MongoClient

def process_logs(data):
    # Conectar ao banco de dados MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['time_series']
    collection = db['logs']

    # Obter data e hora atual
    current_time = datetime.datetime.now()

    # Processar os dados e inserir no banco de dados
    processed_data = {
        'timestamp': current_time,
        'volume': sum(data.values()),
        'details': data
    }

    collection.insert_one(processed_data)

    # Imprimir informações de volume e texto
    print("Volume Total:", sum(data.values()))
    print("Detalhes:")
    for module, volume in data.items():
        print(f"{module}: {volume}")

if __name__ == "__main__":
    data = {
        "audio": 10,
        "images": 20,
        "keyboards": 5,
        "logs": 15,
        "screens": 8,
        "videos": 12
    }
    process_logs(data)