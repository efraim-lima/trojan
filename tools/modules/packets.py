import os
import sys
import ctypes
from ctypes import wintypes
import socket
from system import way
operational, folder, user = way()

def run_as_admin():
    if sys.platform != 'win32':
        raise RuntimeError('Este código só pode ser executado no Windows.')


    # Caminho completo para o script Python a ser executado com privilégios elevados
    script_path = os.path.join(folder, 'functions', 'logs_full.py')

    # Construir a linha de comando para a chamada ShellExecute
    command_line = f'python "{script_path}"'

    # Parâmetros da função ShellExecute
    show_cmd = wintypes.INT(1)  # SW_NORMAL = 1
    parameters = f'/user:{user} "{command_line}"'
    directory = None
    operation = 'runas'

    # Chamar a função ShellExecute para solicitar a elevação de privilégios
    shell32 = ctypes.windll.shell32
    hinstance = shell32.ShellExecuteW(None, operation, sys.executable, parameters, directory, show_cmd)

    if int(hinstance) <= 32:
        raise RuntimeError('Falha ao solicitar elevação de privilégios.')

    # Resto do seu código aqui

    def process_packet():
        # Crie um socket bruto
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)

        # Defina um tamanho máximo para os pacotes capturados
        MAX_PACKET_SIZE = 65536

        # Faça um loop infinito para capturar pacotes
        while True:
            # Capture um pacote
            packet_data, address = raw_socket.recvfrom(MAX_PACKET_SIZE)

            # Processar o pacote
            # Aqui você pode realizar análises e extrações de informações dos pacotes capturados

            # Exemplo de exibição do pacote em hexadecimal
            packet_hex = ':'.join('{:02x}'.format(byte) for byte in packet_data)
            print('Pacote capturado:', packet_hex)

    process_packet()
    # Encerrar a execução do script atual
    # sys.exit()

# Verificar se o script está sendo executado como administrador
if not ctypes.windll.shell32.IsUserAnAdmin():
    run_as_admin()
