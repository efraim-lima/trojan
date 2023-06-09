import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# Certifique-se de que o diretório do projeto esteja no sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ctypes
from ctypes import wintypes

def windows():
    # Definir o caminho completo para a pasta Lixeira
    recycle_bin_path = os.path.join(os.environ["USERPROFILE"], "RecycleBin")

    # Chamar a função SHEmptyRecycleBin da API do Windows
    SHEmptyRecycleBin = ctypes.windll.shell32.SHEmptyRecycleBinW
    SHEmptyRecycleBin.argtypes = [wintypes.HWND, wintypes.LPCWSTR, wintypes.DWORD]
    SHEmptyRecycleBin.restype = wintypes.LONG

    # Passar o caminho completo para a pasta Lixeira para a função SHEmptyRecycleBin
    result = SHEmptyRecycleBin(0, recycle_bin_path, 0)

    if result == 0:
        print("A lixeira foi esvaziada com sucesso.")
    else:
        print("Ocorreu um erro ao esvaziar a lixeira.")

# Chamar a função para esvaziar a lixeira no Windows
# windows()

def linux():
    # Definir o caminho completo para a pasta Lixeira
    recycle_bin_path = os.path.join(os.environ["HOME"], ".local/share/Trash")

    # Executar o comando 'rm -rf' para excluir permanentemente os arquivos da Lixeira
    os.system(f"rm -rf {recycle_bin_path}/*")

    print("A lixeira foi esvaziada com sucesso.")

# Chamar a função para esvaziar a lixeira no Linux
# linux()