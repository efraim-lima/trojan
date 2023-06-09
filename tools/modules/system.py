import os
import platform
import getpass
# from video_path import linux, windows, chromeos, macos

def way():
    # Obter o nome do sistema operacional
    operating_system = platform.system()
    
    # Obter o diretório de trabalho atual
    pasta_atual = os.getcwd()
    # Obter o nome de usuário atualmente logado
    usuario = getpass.getuser()
    
    # Verificar o sistema operacional e chamar a função apropriada
    if operating_system == 'Linux':
        os_name = "Linux"

    elif operating_system == 'Windows':
        os_name = "Windows"
        
    elif operating_system == 'ChromeOS':
        os_name = "ChromeOS"
        
    elif operating_system == 'Darwin':
        os_name = "Darwin" #macOS
        
    else:
        print("Sistema operacional não suportado.")
        return
    
    

    # Continue com o processamento usando o nome do sistema operacional

    # Exemplo de uso
    print("Sistema operacional:", os_name)

    # Exemplo de uso
    return os_name, pasta_atual, usuario