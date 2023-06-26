import os
import sys

# Adicione o diretório raiz do seu projeto ao PYTHONPATH
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

# Defina o DJANGO_SETTINGS_MODULE antes de importar qualquer coisa do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Certifique-se de que o diretório do projeto esteja no sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import win32evtlog
import time
from datetime import date
import pymongo
import psutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorama import init, Fore, Style
import json

init()

def logs_task():
    for _ in range(10):
        # Simulação de tarefa de áudio
        time.sleep(1)
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        print(f"Uso de CPU: {cpu_percent}%")
        print(f"Uso de memória: {memory_percent}%")

# Configurações do MongoDB
mongodb_url = "mongodb://localhost:27017"
database_name = "mydatabase"
collection_file_name = "file_logs"
collection_system_name = "system_logs"
collection_apps_name = "apps_logs"

# Configuração do diretório raiz a ser monitorado (substitua pelo diretório de sua escolha)
root_directory = "C:\\"

# Caminhos dos arquivos de log
logs_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(logs_directory, exist_ok=True)

file_log_path = os.path.join(logs_directory, "file_logs.txt")
system_log_path = os.path.join(logs_directory, "system_logs.txt")

# Criação dos arquivos de log se não existirem
if not os.path.isfile(file_log_path):
    with open(file_log_path, "w") as file:
        pass

if not os.path.isfile(system_log_path):
    with open(system_log_path, "w") as file:
        pass

# Verificar se o diretório de logs existe, caso contrário, criá-lo
if not os.path.isdir(logs_directory):
    os.makedirs(logs_directory)

# Inicialização do cliente MongoDB e das coleções
client = pymongo.MongoClient(mongodb_url)
db = client[database_name]
collection_file = db.get_collection(collection_file_name)
collection_system = db.get_collection(collection_system_name)
collection_apps = db.get_collection(collection_apps_name)

# Variáveis para armazenar o conteúdo inicial dos arquivos de log
initial_file_log_content = ""
initial_system_log_content = ""

class SystemEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        # Ignorar a pasta atual e todas as subpastas a partir do caminho ".."
        if os.path.abspath(event.src_path).startswith(os.path.abspath("..")):
            return
        # Imprimir informações sobre o evento
        print(f"{Fore.GREEN}Event Type:{Style.RESET_ALL}", event.event_type)
        print(f"{Fore.GREEN}Event Path:{Style.RESET_ALL}", event.src_path)
        print(f"{Fore.GREEN}Event Time:{Style.RESET_ALL}", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
        print("---")

        # Registrar a alteração no arquivo de log
        with open(system_log_path, "a") as file:
            file.write(f"Event Type: {event.event_type}\n")
            file.write(f"Event Path: {event.src_path}\n")
            file.write(f"Event Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}\n")
            file.write("---\n")

        if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            # Registrar a alteração no log do sistema (somente para sistemas Linux e macOS)
            import syslog
            syslog.syslog(f"Event Type: {event.event_type}\nEvent Path: {event.src_path}\nEvent Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}\n---")
                
        file_handler = FileLog(
            day=date.today().isoformat(),
            event_type=event.event_type,
            event_path=event.src_path,
            event_time=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        )
        file_handler.save()

class FileEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        # Ignorar a pasta atual e todas as subpastas a partir do caminho ".."
        if os.path.abspath(event.src_path).startswith(os.path.abspath("..")):
            return
        # Imprimir informações sobre o evento
        print(f"{Fore.BLUE}{Style.BRIGHT}Event Type:{Style.RESET_ALL}", event.event_type)
        print(f"{Fore.BLUE}{Style.BRIGHT}Event Path:{Style.RESET_ALL}", event.src_path)
        print(f"{Fore.BLUE}{Style.BRIGHT}Event Time:{Style.RESET_ALL}", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
        print("---")

        # Registrar a alteração no arquivo de log
        with open(file_log_path, "a") as file:
            file.write(f"Event Type: {event.event_type}\n")
            file.write(f"Event Path: {event.src_path}\n")
            file.write(f"Event Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}\n")
        
        file_handler = FileLog(
            day=day_db,
            event_type=event.event_type,
            event_path=event.src_path,
            event_time=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        )
        file_handler.save()

def monitor_system_events_linux_macos():
    import syslog
    # Definir a máscara de prioridade do syslog
    syslog.setlogmask(syslog.LOG_MASK(syslog.LOG_INFO) | syslog.LOG_MASK(syslog.LOG_ERR))

    # Abrir uma conexão com o syslog
    syslog.openlog(logoption=syslog.LOG_PID)

    # Definir a identificação do programa
    syslog.setlogmask(syslog.LOG_UPTO(syslog.LOG_NOTICE))

    # Monitorar os eventos do sistema
    syslog.syslog(syslog.LOG_NOTICE, "Iniciando monitoramento de eventos do sistema...")

    # Exemplo de registro de eventos
    syslog.syslog(syslog.LOG_INFO, "Evento de informação")
    syslog.syslog(syslog.LOG_WARNING, "Evento de aviso")
    syslog.syslog(syslog.LOG_ERR, "Evento de erro")
    
    while True:
        # Obter a lista atualizada de processos em execução
        current_processes = psutil.process_iter()

        # Comparar as listas de processos para encontrar novos processos iniciados ou encerrados
        new_processes = [p for p in current_processes if p not in initial_processes]
        terminated_processes = [p for p in initial_processes if p not in current_processes]

        # Processar os novos processos iniciados
        for process in new_processes:
            process_name = process.name()
            print(f"\033[1m\033[92mNew process started:\033[0m {process_name}")

            # Criar variáveis com os dados do processo
            event_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
            event_source = "Process"
            event_category = "New Process"
            event_description = f"Process started: {process_name}"


            
            # Obter informações adicionais do processo
            pid = process.pid
            ppid = process.ppid()
            # exe = process.exe()
            # cwd = process.cwd()
            status = process.status()
            memory_info = process.memory_info()
            cpu_times = process.cpu_times()
            memory_info = process.memory_info()._asdict()
            cpu_times = process.cpu_times()._asdict()

            # Criar um dicionário chave-valor com os dados do evento
            event_data = {
                "Event Time": event_time,
                "Event Source": event_source,
                "Event Category": event_category,
                "Event Description": event_description,
                "Process Name": process_name,
                "PID": pid,
                "PPID": ppid,
                # "Executable Path": exe,
                # "Working Directory": cwd,
                "Status": status,
                "Memory Info": memory_info,
                "CPU Times": cpu_times
            }
                        # Adicionar a tag com o dia ao dicionário `event_data`
            event_data["Day"] = date.today().isoformat()
            
            # Criar um objeto SystemLog com os dados do evento
            system_log = AppsLog(
                day=day_db,
                event_time=event_time,
                event_source=event_source,
                event_category=event_category,
                event_description=event_description,
                process_name=process_name,
                pid=pid,
                ppid=ppid,
                status=status,
                memory_info=memory_info,
                cpu_times=cpu_times,                
            )
            # Salvar o objeto no MongoDB
            system_log.save()
            
            print(event_data)

            # Converter o dicionário em formato JSON
            json_data = json.dumps(event_data)

            # Enviar os eventos para o MongoDB
            collection_system.insert_one(json.loads(json_data))

        # Processar os processos encerrados
        for process in terminated_processes:
            process_name = process.name()
            print(f"\033[1m\033[91mProcess terminated:\033[0m {process_name}")

            # Criar variáveis com os dados do processo
            event_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
            event_source = "Process"
            event_category = "Terminated Process"
            event_description = f"Process terminated: {process_name}"

            # Obter informações adicionais do processo
            pid = process.pid
            ppid = process.ppid()
            # exe = process.exe()
            # cwd = process.cwd()
            status = process.status()
            memory_info = process.memory_info()
            cpu_times = process.cpu_times()
            memory_info = process.memory_info()._asdict()
            cpu_times = process.cpu_times()._asdict()

            # Criar um dicionário chave-valor com os dados do evento
            event_data = {
                "Event Time": event_time,
                "Event Source": event_source,
                "Event Category": event_category,
                "Event Description": event_description,
                "Process Name": process_name,
                "PID": pid,
                "PPID": ppid,
                # "Executable Path": exe,
                # "Working Directory": cwd,
                "Status": status,
                "Memory Info": memory_info,
                "CPU Times": cpu_times
            }

            # Criar um objeto SystemLog com os dados do evento
            system_log = AppsLog(
                day=day_db,
                event_time=event_time,
                event_source=event_source,
                event_category=event_category,
                event_description=event_description,
                process_name=process_name,
                pid=pid,
                ppid=ppid,
                status=status,
                memory_info=memory_info,
                cpu_times=cpu_times,                
            )
            # Salvar o objeto no MongoDB
            system_log.save()
            
            print(event_data)
            
            # Converter o dicionário em formato JSON
            json_data = json.dumps(event_data)

            # Enviar os eventos para o MongoDB
            collection_apps.insert_one(json.loads(json_data))

        # Atualizar a lista inicial de processos
        initial_processes = current_processes

        # Aguardar um intervalo de tempo antes de verificar novamente
        time.sleep(30)  # Verificar a cada 30 segundos


        # Fechar a conexão com o syslog
        syslog.closelog()

def monitor_system_events_windows():
    # Definir o nome do log do evento que você deseja acessar
    event_log_name = 'System'

    # Abrir o log do evento
    hand = win32evtlog.OpenEventLog(None, event_log_name)

    # Ler os eventos do log
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    total_events = win32evtlog.GetNumberOfEventLogRecords(hand)
    events = win32evtlog.ReadEventLog(hand, flags, 0)

    # Inicializar a lista para armazenar os eventos
    event_list = []

    # Processar os eventos
    for event in events:
        event_time = event.TimeGenerated.Format()  # Data e hora do evento
        event_source = event.SourceName  # Nome da origem do evento
        event_category = event.EventCategory  # Categoria do evento
        event_description = event.StringInserts  # Descrição do evento

        # Imprimir os detalhes do evento
        print(f"\033[1m\033[92mEvent Time:\033[0m {event_time}")
        print(f"\033[1m\033[92mEvent Source:\033[0m {event_source}")
        print(f"\033[1m\033[92mEvent Category:\033[0m {event_category}")
        print(f"\033[1m\033[92mEvent Description:\033[0m {event_description}")
        print('---')

        # Adicionar o evento à lista
        event_data = {
            "Total Events": total_events,
            "Event Time": event_time,
            "Event Source": event_source,
            "Event Category": event_category,
            "Event Description": event_description
        }
        event_list.append(event_data)

    # Converter a lista de eventos para formato JSON
    json_data = json.dumps(event_list)

    # Enviar os eventos para o MongoDB
    collection_system.insert_many(json.loads(json_data))
    
    initial_processes = list(psutil.process_iter())

    while True:
        # Obter a lista atualizada de processos em execução
        current_processes = psutil.process_iter()

        # Comparar as listas de processos para encontrar novos processos iniciados ou encerrados
        new_processes = [p for p in current_processes if p not in initial_processes]
        terminated_processes = [p for p in initial_processes if p not in current_processes]

        # Processar os novos processos iniciados
        for process in new_processes:
            process_name = process.name()
            print(f"\033[1m\033[92mNew process started:\033[0m {process_name}")

            # Criar variáveis com os dados do processo
            event_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
            event_source = "Process"
            event_category = "New Process"
            event_description = f"Process started: {process_name}"

            # Obter informações adicionais do processo
            pid = process.pid
            ppid = process.ppid()
            # exe = process.exe()
            # cwd = process.cwd()
            status = process.status()
            memory_info = process.memory_info()
            cpu_times = process.cpu_times()
            memory_info = process.memory_info()._asdict()
            cpu_times = process.cpu_times()._asdict()

            # Criar um dicionário chave-valor com os dados do evento
            event_data = {
                "Event Time": event_time,
                "Event Source": event_source,
                "Event Category": event_category,
                "Event Description": event_description,
                "Process Name": process_name,
                "PID": pid,
                "PPID": ppid,
                # "Executable Path": exe,
                # "Working Directory": cwd,
                "Status": status,
                "Memory Info": memory_info,
                "CPU Times": cpu_times,
                "Total Events": total_events,
            }
                        
            # Criar um objeto SystemLog com os dados do evento
            system_log = AppsLog(
                day=day_db,
                event_time=event_time,
                event_source=event_source,
                event_category=event_category,
                event_description=event_description,
                process_name=process_name,
                pid=pid,
                ppid=ppid,
                status=status,
                memory_info=memory_info,
                cpu_times=cpu_times,
                total_events=total_events,           
            )
            # Salvar o objeto no MongoDB
            system_log.save()
            
            print(event_data)

            # Converter o dicionário em formato JSON
            json_data = json.dumps(event_data)

            # Enviar os eventos para o MongoDB
            collection_apps.insert_one(json.loads(json_data))

        # Processar os processos encerrados
        for process in terminated_processes:
            process_name = process.name()
            print(f"\033[1m\033[91mProcess terminated:\033[0m {process_name}")

            # Criar variáveis com os dados do processo
            event_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
            event_source = "Process"
            event_category = "Terminated Process"
            event_description = f"Process terminated: {process_name}"

            # Obter informações adicionais do processo
            # pid = process.pid
            ppid = process.ppid()
            # exe = process.exe()
            # cwd = process.cwd()
            status = process.status()
            memory_info = process.memory_info()
            cpu_times = process.cpu_times()
            memory_info = process.memory_info()._asdict()
            cpu_times = process.cpu_times()._asdict()


            # Criar um dicionário chave-valor com os dados do evento
            event_data = {
                "Event Time": event_time,
                "Event Source": event_source,
                "Event Category": event_category,
                "Event Description": event_description,
                "Process Name": process_name,
                # "PID": pid,
                "PPID": ppid,
                # "Executable Path": exe,
                # "Working Directory": cwd,
                "Status": status,
                "Memory Info": memory_info,
                "CPU Times": cpu_times
            }
            
            # Criar um objeto SystemLog com os dados do evento
            system_log = AppsLog(
                day=day_db,
                event_time=event_time,
                event_source=event_source,
                event_category=event_category,
                event_description=event_description,
                process_name=process_name,
                pid=pid,
                ppid=ppid,
                status=status,
                memory_info=memory_info,
                cpu_times=cpu_times,                
            )
            # Salvar o objeto no MongoDB
            system_log.save()
            
            print(event_data)
            
            # Converter o dicionário em formato JSON
            json_data = json.dumps(event_data)

            # Enviar os eventos para o MongoDB
            collection_system.insert_one(json.loads(json_data))

        # Atualizar a lista inicial de processos
        initial_processes = current_processes

        # Aguardar um intervalo de tempo antes de verificar novamente
        time.sleep(30)  # Verificar a cada 30 segundos

def monitor_file_changes():
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=root_directory, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(30)  # Verificar as alterações a cada 30 segundos
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def main():
    # Realizar a tarefa de logs
    logs_task()

    # Registrar o conteúdo inicial dos arquivos de log
    global initial_file_log_content
    global initial_system_log_content

    with open(file_log_path, "r") as file:
        initial_file_log_content = file.read()

    with open(system_log_path, "r") as file:
        initial_system_log_content = file.read()

    # Monitorar os eventos do sistema (apenas para sistemas Linux e macOS)
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        monitor_system_events_linux_macos()

    # Monitorar os eventos do sistema (apenas para Windows)
    if sys.platform.startswith('win'):
        monitor_system_events_windows()

    # Monitorar as alterações de arquivo no diretório especificado
    monitor_file_changes()

    # Após encerrar a monitoração, processar os logs
    process_logs()


def process_logs():
    # Ler o conteúdo atual dos arquivos de log
    current_file_log_content = ""
    current_system_log_content = ""

    with open(file_log_path, "r") as file:
        current_file_log_content = file.read()

    with open(system_log_path, "r") as file:
        current_system_log_content = file.read()

    # Verificar se houve alteração nos logs de arquivo
    if current_file_log_content != initial_file_log_content:
        # Processar o log de arquivo
        print("Processando log de arquivo...")
        # Implemente o código necessário para processar o log de arquivo de acordo com suas necessidades

    # Verificar se houve alteração nos logs do sistema
    if current_system_log_content != initial_system_log_content:
        # Processar o log do sistema
        print("Processando log do sistema...")
        # Implemente o código necessário para processar o log do sistema de acordo com suas necessidades

    # Atualizar o conteúdo inicial dos arquivos de log para o conteúdo atual
    initial_file_log_content = current_file_log_content
    initial_system_log_content = current_system_log_content

if __name__ == "__main__":
    main()