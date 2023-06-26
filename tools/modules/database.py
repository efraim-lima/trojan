import pymongo
import gridfs
from datetime import datetime

# Obter a data e hora atual
now = datetime.now()
# Obter apenas a variável "dia"
today = now.date()
today =  today.isoformat()  # Converter para string
# Obter apenas a variável "horario"
hour = now.time()
hour = hour.isoformat()  # Converter para string

# Configurações do MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["outputs"]
fs = gridfs.GridFS(db, collection="video_data")
collection_files = db["file_logs"]
collection_apps = db["apps_logs"]
collection_event = db["system_logs"]
collection_cpu = db["cpu_usage"]
collection_keyboard = db["keyboard_data"]
collection_audio = db["audio_data"]
fs_audio = gridfs.GridFS(db, collection="audio_data")
collection_image = db["image_data"]
fs_imagesII = gridfs.GridFS(db, collection="screen_images_data")
fs_videos = gridfs.GridFS(db, collection="screen_videos_data")
fs_audio = gridfs.GridFS(db, collection="screen_audio_data")