import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# Certifique-se de que o diretório do projeto esteja no sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import threading
from modules.database import collection_apps, collection_event, collection_files, collection_event, today, hour
import psutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorama import Fore, Style

# Importação específica para cada plataforma
if sys.platform.startswith('win32'):
    import win32evtlog
elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
    import syslog

def clear_terminal():
    """Limpa o terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def logs_task():
    for _ in range(10):
        # Simulação de tarefa de áudio
        time.sleep(1)
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        print(f"Uso de CPU: {cpu_percent}%")
        print(f"Uso de memória: {memory_percent}%")
        clear_terminal()

# Configuração do diretório raiz a ser monitorado (substitua pelo diretório de sua escolha)
root_directory = "C:\\"

# Caminhos dos arquivos de log
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logs_directory = os.path.join(ROOT_DIR, "modules/logs")
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

def convert_size(size_bytes):
    # Size conversion thresholds
    thresholds = {
        'KB': 1024,
        'MB': 1024 ** 2,
        'GB': 1024 ** 3,
        'TB': 1024 ** 4
    }
    
    # Find the appropriate threshold
    for unit in thresholds:
        if size_bytes < thresholds[unit]:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= thresholds[unit]
    
    return f"{size_bytes:.2f} PB"  # Petabytes or larger

class FileEventHandler(FileSystemEventHandler):
    
    def on_any_event(self, event):
        try:
            # Ignorar a pasta atual e todas as subpastas a partir do caminho ".."
            if os.path.abspath(event.src_path).startswith(os.path.abspath("..")):
                return
            
            event_type = event.event_type
            event_path = event.src_path
            file_name = os.path.basename(event_path)

            # Verificar se o arquivo existe
            if os.path.exists(event_path):
                file_size = convert_size(os.path.getsize(event_path))
            else:
                # O arquivo não existe, faça algo adequado ao seu caso
                file_size = 0  # Ou qualquer outro valor padrão que faça sentido

            # Imprimir informações sobre o evento
            print(f"{Fore.BLUE}{Style.BRIGHT}Event Type:{Style.RESET_ALL}", event_type)
            print(f"{Fore.BLUE}{Style.BRIGHT}Event Path:{Style.RESET_ALL}", event_path)
            print(f"{Fore.BLUE}{Style.BRIGHT}Event Time:{Style.RESET_ALL}", hour)
            print(f"{Fore.BLUE}{Style.BRIGHT}Event Name:{Style.RESET_ALL}", file_name)
            print(f"{Fore.BLUE}{Style.BRIGHT}Event Size:{Style.RESET_ALL}", file_size)
            print("---")

            # Registrar a alteração no arquivo de log
            with open(file_log_path, "a") as file:
                file.write(f"Event Type: {event_type}\n")
                file.write(f"Event Path: {event_path}\n")
                file.write(f"Event Time: {hour}\n")
                file.write(f"Event Name: {file_name}\n")
                file.write(f"Event Size: {file_size}\n")

            
            file_log = {
                "date":today,
                "hour":hour,
                "file_name":file_name,
                "file_size":file_size,
                "event_type":event_type,
                "event_path":event_path,
            }
            # Inserir documento na coleção
            collection_files.insert_one(file_log)
        except:
            pass
 

def monitor_file_events():
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, root_directory, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


def monitor_system_events():
    while True:
        # Monitorar eventos do sistema específicos para cada plataforma
        if sys.platform.startswith('win32'):
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
                        "date":today,
                        "hour":hour,
                        "total_events": total_events,
                        "event_time": event_time,
                        "event_source": event_source,
                        "event_category": event_category,
                        "event_description": event_description
                    }
                    collection_event.insert_one(event_data)  
                    event_list.append(event_data)               
                   

                # Converter a lista de eventos para formato JSON
                # json_data = json.dumps(event_list)

                # Enviar os eventos para o MongoDB
                # collection_system.insert_many(json.loads(json_data))
                
                initial_processes = list(psutil.process_iter())

                while True:
                    # Obter a lista atualizada de processos em execução
                    current_processes = psutil.process_iter()
                    new_processes = [p for p in current_processes if p not in initial_processes]
                    terminated_processes = [p for p in initial_processes if p not in current_processes]

                    # Processar os novos processos iniciados
                    for process in new_processes:
                        process_name = process.name()

                        # Criar variáveis com os dados do processo
                        event_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
                        event_source = "Process"
                        event_category = "New Process"
                        event_description = f"Process started: {process_name}"

                        try:
                            pid = process.pid
                        except:
                            pid = None

                        # Obter informações adicionais do processo
                        try:
                            ppid = process.ppid()
                        except psutil.Error as e:
                            ppid = None
                        except psutil.AccessDenied as e:
                            ppid = None
                        except:
                            ppid = None
                            pass

                        try:
                            process = psutil.Process(pid)  # Replace `pid` with the actual process ID you're trying to access
                            exe = process.exe()
                        except (psutil.Error, psutil.NoSuchProcess) as e:
                            exe = None

                        try:
                            cwd = process.cwd()
                        except AttributeError as e:
                            cwd = None
                        except psutil.AccessDenied as e:
                            cwd = None
                        except:
                            cwd = None
                            pass

                        try:
                            status = process.status()
                        except psutil.Error as e:
                            status = None

                        try:
                            memory_info = process.memory_info()
                        except psutil.Error as e:
                            memory_info = None

                        try:
                            cpu_times = process.cpu_times()
                        except psutil.Error as e:
                            cpu_times = None

                        try:
                            memory_info = process.memory_info()._asdict()
                        except psutil.Error as e:
                            memory_info = None

                        try:
                            cpu_times = process.cpu_times()._asdict()
                        except psutil.Error as e:
                            cpu_times = None


                        # Criar um dicionário chave-valor com os dados do evento
                        event_data = {
                            "date": today,
                            "hour": hour,
                            "event_source": event_source,
                            "event_category": event_category,
                            "event_description": event_description,
                            "process_name": process_name,
                            "PID": pid,
                            "PPID": ppid,
                            "path": exe,
                            "working_directory": cwd,
                            "status": status,
                            "memory_info": memory_info,
                            "CPU": cpu_times,
                            "total": total_events,
                        }
                        collection_apps.insert_one(event_data)
                        print(f"\n\n \033[1m\033[91mProcess started:\033[0m {process_name}\n\n{event_source}{event_description}{pid}")

                    # Processar os processos encerrados
                    for process in terminated_processes:
                        process_name = process.name()

                        # Criar variáveis com os dados do processo
                        event_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
                        event_source = "Process"
                        event_category = "Terminated Process"
                        event_description = f"Process terminated: {process_name}"

                        try:
                            pid = process.pid
                        except:
                            pid = None

                        # Obter informações adicionais do processo
                        try:
                            ppid = process.ppid()
                        except psutil.Error as e:
                            ppid = None
                        except psutil.AccessDenied as e:
                            ppid = None
                        except:
                            ppid = None
                            pass

                        try:
                            process = psutil.Process(pid)  # Replace `pid` with the actual process ID you're trying to access
                            exe = process.exe()
                        except (psutil.Error, psutil.NoSuchProcess) as e:
                            exe = None

                        try:
                            cwd = process.cwd()
                        except AttributeError as e:
                            cwd = None
                        except psutil.AccessDenied as e:
                            cwd = None
                        except:
                            cwd = None
                            pass

                        try:
                            status = process.status()
                        except psutil.Error as e:
                            status = None

                        try:
                            memory_info = process.memory_info()
                        except psutil.Error as e:
                            memory_info = None

                        try:
                            cpu_times = process.cpu_times()
                        except psutil.Error as e:
                            cpu_times = None

                        try:
                            memory_info = process.memory_info()._asdict()
                        except psutil.Error as e:
                            memory_info = None

                        try:
                            cpu_times = process.cpu_times()._asdict()
                        except psutil.Error as e:
                            cpu_times = None


                        # Criar um dicionário chave-valor com os dados do evento
                        event_data = {
                            "date":today,
                            "hour":hour,
                            "event_source": event_source,
                            "event_category": event_category,
                            "event_description": event_description,
                            "process_name": process_name,
                            "PID": pid,
                            "PPID": ppid,
                            "path": exe,
                            "working_directory": cwd,
                            "status": status,
                            "memory_info": memory_info,
                            "CPU": cpu_times,
                            "total": total_events,
                        }
                        collection_apps.insert_one(event_data)
                        print(f"\n\n \033[1m\033[91mProcess terminated:\033[0m {process_name}\n\n{event_source}{event_description}{pid}")
                        
                    # Atualizar a lista inicial de processos
                    initial_processes = current_processes

                    # Aguardar um intervalo de tempo antes de verificar novamente
                    time.sleep(30)  # Verificar a cada X5 segundos
        elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            syslog.openlog("SystemMonitor")
            try:
                for line in syslog.syslog():
                    log_entry = line.strip()

                    with open(system_log_path, "a") as file:
                        file.write(log_entry + "\n")
                
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

                        # Criar variáveis com os dados do processo
                        event_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
                        event_source = "Process"
                        event_category = "New Process"
                        event_description = f"Process started: {process_name}"

                        try:
                            pid = process.pid
                        except:
                            pid = None

                        # Obter informações adicionais do processo
                        try:
                            ppid = process.ppid()
                        except psutil.Error as e:
                            ppid = None
                        except psutil.AccessDenied as e:
                            ppid = None
                        except:
                            ppid = None
                            pass

                        try:
                            process = psutil.Process(pid)  # Replace `pid` with the actual process ID you're trying to access
                            exe = process.exe()
                        except (psutil.Error, psutil.NoSuchProcess) as e:
                            exe = None

                        try:
                            cwd = process.cwd()
                        except AttributeError as e:
                            cwd = None

                        try:
                            status = process.status()
                        except psutil.Error as e:
                            status = None

                        try:
                            memory_info = process.memory_info()
                        except psutil.Error as e:
                            memory_info = None

                        try:
                            cpu_times = process.cpu_times()
                        except psutil.Error as e:
                            cpu_times = None

                        try:
                            memory_info = process.memory_info()._asdict()
                        except psutil.Error as e:
                            memory_info = None

                        try:
                            cpu_times = process.cpu_times()._asdict()
                        except psutil.Error as e:
                            cpu_times = None

                        # Criar um dicionário chave-valor com os dados do evento
                        event_data = {
                            "date":today,
                            "hour":hour,                            
                            "event_source": event_source,
                            "event_category": event_category,
                            "event_description": event_description,
                            "process_name": process_name,
                            "PID": pid,
                            "PPID": ppid,
                            "path": exe,
                            "working_directory": cwd,
                            "status": status,
                            "memory_info": memory_info,
                            "CPU": cpu_times,
                            "total": total_events,
                        }
                        collection_apps.insert_one(event_data)
                        print(f"\033[1m\033[92mNew process started:\033[0m {process_name}\n\n{event_source}\n{event_description}\n{pid}")
                        

                    # Processar os processos encerrados
                    for process in terminated_processes:
                        process_name = process.name()

                        # Criar variáveis com os dados do processo
                        event_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
                        event_source = "Process"
                        event_category = "Terminated Process"
                        event_description = f"Process terminated: {process_name}"

                        try:
                            pid = process.pid
                        except:
                            pid = None

                        # Obter informações adicionais do processo
                        try:
                            ppid = process.ppid()
                        except psutil.Error as e:
                            ppid = None
                        except psutil.AccessDenied as e:
                            ppid = None
                        except:
                            ppid = None
                            pass

                        try:
                            process = psutil.Process(pid)  # Replace `pid` with the actual process ID you're trying to access
                            exe = process.exe()
                        except (psutil.Error, psutil.NoSuchProcess) as e:
                            exe = None

                        try:
                            cwd = process.cwd()
                        except AttributeError as e:
                            cwd = None

                        try:
                            status = process.status()
                        except psutil.Error as e:
                            status = None

                        try:
                            memory_info = process.memory_info()
                        except psutil.Error as e:
                            memory_info = None

                        try:
                            cpu_times = process.cpu_times()
                        except psutil.Error as e:
                            cpu_times = None

                        try:
                            memory_info = process.memory_info()._asdict()
                        except psutil.Error as e:
                            memory_info = None

                        try:
                            cpu_times = process.cpu_times()._asdict()
                        except psutil.Error as e:
                            cpu_times = None


                        # Criar um dicionário chave-valor com os dados do evento
                        event_data = {
                            "date":today,
                            "hour":hour,
                            "event_source": event_source,
                            "event_category": event_category,
                            "event_description": event_description,
                            "process_name": process_name,
                            "PID": pid,
                            "PPID": ppid,
                            "path": exe,
                            "working_directory": cwd,
                            "status": status,
                            "memory_info": memory_info,
                            "CPU": cpu_times,
                            "total": total_events,
                        }
                        collection_apps.insert_one(event_data)
                        print(f"\033[1m\033[91mProcess terminated:\033[0m {process_name}\n\n{event_source}\n{event_description}\n{pid}")

                        # Criar um objeto SystemLog com os dados do evento
                        collection_apps.insert_one(event_data)
                        

                    # Atualizar a lista inicial de processos
                    initial_processes = current_processes

                    # Aguardar um intervalo de tempo antes de verificar novamente
                    time.sleep(30)  # Verificar a cada 30 segundos


                    # Fechar a conexão com o syslog
                    syslog.closelog()
            finally:
                syslog.closelog()

        time.sleep(1)

if __name__ == "__main__":
    logs_task()
    file_monitoring_thread = threading.Thread(target=monitor_file_events)
    file_monitoring_thread.daemon = True
    file_monitoring_thread.start()

    system_monitoring_thread = threading.Thread(target=monitor_system_events)
    system_monitoring_thread.daemon = True
    system_monitoring_thread.start()

    file_monitoring_thread.join()
    system_monitoring_thread.join()