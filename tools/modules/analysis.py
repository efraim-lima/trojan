import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# Certifique-se de que o diretório do projeto esteja no sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import platform
import winreg
import subprocess
import requests
import hashlib
import glob
from modules.database import collection_apps, collection_event, collection_networks, collection_hashes, today, hour

def get_application_details(application):
    application_path = application.get("path")
    process_name = application.get("process_name")

    if application_path:
        return {"path": application_path, "date": application.get("date")}

    current_os = platform.system()
    if current_os == "Windows":
        application_path = find_application_path_windows(process_name)
    elif current_os == "Linux":
        application_path = find_application_path_linux(process_name)
    elif current_os == "Darwin":
        application_path = find_application_path_mac(process_name)
    elif current_os == "Chrome OS":
        application_path = find_application_path_chromeos(process_name)
    else:
        print("Sistema operacional não suportado.")

    if application_path:
        return {"path": application_path, "date": application.get("date")}

    return {}


def get_top_applications(dates, collections, limit=4):
    top_applications = []

    for collection_name in collections:
        for date in dates:
            pipeline = [
                {"$match": {"date": date}},
                {"$group": {"_id": "$process_name", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": limit}
            ]
            result = collection_name.aggregate(pipeline)

            for entry in result:
                top_applications.append(entry["_id"])

    return top_applications

def find_application_path_windows(process_name):
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths")
        for i in range(winreg.QueryInfoKey(key)[0]):
            subkey_name = winreg.EnumKey(key, i)
            subkey = winreg.OpenKey(key, subkey_name)
            if process_name.lower() in subkey_name.lower():
                return winreg.QueryValue(subkey, "").split('"')[0]  # Retorna apenas o caminho do aplicativo
    except:
        pass

    return None

def find_application_path_linux(process_name):
    try:
        output = subprocess.check_output(["which", process_name])
        if output:
            return output.decode().strip()
    except:
        pass

    return None


def find_application_path_mac(process_name):
    try:
        output = subprocess.check_output(["mdfind", "kMDItemCFBundleIdentifier == " + process_name])
        if output:
            paths = output.decode().strip().split("\n")
            return paths[0]  # Retorna o primeiro caminho encontrado
    except:
        pass

    return None


def find_application_path_chromeos(process_name):
    try:
        output = subprocess.check_output(["which", process_name])
        if output:
            return output.decode().strip()
    except:
        pass

    return None


def calculate_file_hash(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
        file_hash = hashlib.sha256(content).hexdigest()
    return file_hash


def check_file_hash(file_path):
    file_hash = calculate_file_hash(file_path)
    print(f"Arquivo: {file_path}")
    print(f"Hash: {file_hash}")

    # Chave de API da VirusTotal
<<<<<<< HEAD
    with open('tapingII.txt', 'rb') as api_key:
        api_key = api_key.read()

=======
    api_key = ""
>>>>>>> 9653173a8100978d09a6e2504ef0fdc5f00f4a3f
    # aqui criariamos uma variavel de ambiente antes de subir a API KEY
    # api_key = os.environ.get("NOME_DA_VARIAVEL")

    # URL da API da VirusTotal para verificar o hash
    api_url = f"https://www.virustotal.com/api/v3/files/{file_hash}"

    # Cabeçalho da requisição com a chave de API
    headers = {"x-apikey": api_key}

    # Envia a requisição GET para a API da VirusTotal
    response = requests.get(api_url, headers=headers)

    # Verifica o código de status da resposta
    if response.status_code == 200:
        result = response.json()
        if result.get("data", {}).get("attributes", {}).get("last_analysis_stats", {}).get("malicious") > 0:
            print("O arquivo é considerado malicioso.")
            # Cria o dicionário com as informações do arquivo
            file_info = {
                "absolute_path": os.path.abspath(file_path),
                "relative_path": os.path.relpath(file_path),
                "hash": file_hash,
                "date": today,
                "hour": hour,
                "id": os.path.relpath(file_path).replace(os.path.sep, "_")  # Cria um ID único baseado no caminho relativo
            }

            # Insere o documento na coleção "collection_hashes"
            collection_hashes.insert_one(file_info)
        else:
            print("O arquivo não é considerado malicioso.")
    else:
        print("Não foi possível verificar o arquivo.")



def get_application_path(application):
    application_details = get_application_details(application)

    if application_details and "path" in application_details:
        return application_details["path"]

    return None


def find_application_path_fallback(process_name):
    # Padrão de busca baseado no nome do aplicativo
    search_pattern = f"**/{process_name}*"

    # Realiza a busca no sistema de arquivos
    matching_paths = glob.glob(search_pattern, recursive=True)

    # Verifica se foram encontrados resultados
    if matching_paths:
        return matching_paths[0]  # Retorna o primeiro caminho encontrado

    return None


def perform_analysis_for_top_applications(dates, collections):
    top_applications = get_top_applications(dates, collections)

    for application_name in top_applications:
        found = False

        for collection in collections:
            application = collection.find_one({"process_name": application_name, "date": today})

            if application:
                found = True
                application_path = get_application_path(application)
                if not application_path:
                    application_path = find_application_path_windows(application_name)
                if not application_path:
                    application_path = find_application_path_linux(application_name)
                if not application_path:
                    application_path = find_application_path_mac(application_name)
                if not application_path:
                    application_path = find_application_path_chromeos(application_name)
                if not application_path:
                    application_path = find_application_path_fallback(application_name)

                if application_path:
                    folder_path = os.path.dirname(application_path)  # Obtém o caminho da pasta do arquivo
                    if not os.path.exists(folder_path):
                        print(f"Caminho da pasta do aplicativo '{application_name}' ({folder_path}) não encontrado no sistema.")
                    else:
                        file_paths = glob.glob(os.path.join(folder_path, "*"))  # Obtém todos os caminhos dos arquivos na pasta
                        if not file_paths:
                            print(f"Nenhum arquivo encontrado na pasta do aplicativo '{application_name}'.")
                        else:
                            for file_path in file_paths:
                                if os.path.isfile(file_path):  # Verifica se é um arquivo válido
                                    check_file_hash(file_path)
                else:
                    print(f"Caminho do aplicativo '{application_name}' não encontrado.")
                break

        if not found:
            print(f"Aplicativo '{application_name}' não encontrado para a data de hoje ({today}).")

if __name__ == "__main__":
    collections = [collection_apps, collection_event, collection_networks]
    dates = [today]

    perform_analysis_for_top_applications(dates, collections)
