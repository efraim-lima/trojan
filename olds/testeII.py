import win32evtlog
import ctypes
import psutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SystemEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        # Imprimir informações sobre o evento
        print("Event Type:", event.event_type)
        print("Event Path:", event.src_path)
        print("Event Time:", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))

def monitor_system_events():
    # Definir o nome do log do evento que você deseja acessar
    event_log_name = 'System'

    # Abrir o log do evento
    hand = win32evtlog.OpenEventLog(None, event_log_name)

    # Ler os eventos do log
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    total_events = win32evtlog.GetNumberOfEventLogRecords(hand)
    events = win32evtlog.ReadEventLog(hand, flags, 0)

    # Processar e imprimir os eventos
    for event in events:
        event_time = event.TimeGenerated.Format()  # Data e hora do evento
        event_source = event.SourceName  # Nome da origem do evento
        event_category = event.EventCategory  # Categoria do evento
        event_description = event.StringInserts  # Descrição do evento
        
        # Imprimir os detalhes do evento
        print(f"Event Time: {event_time}")
        print(f"Event Source: {event_source}")
        print(f"Event Category: {event_category}")
        print(f"Event Description: {event_description}")
        print('---')

    # Enumerar as janelas e processos ativos
    user32 = ctypes.WinDLL('user32')
    kernel32 = ctypes.WinDLL('kernel32')

    def enum_windows(hwnd, data):
        if user32.IsWindowVisible(hwnd):
            process_id = ctypes.c_ulong(0)
            thread_id = user32.GetWindowThreadProcessId(hwnd, ctypes.byref(process_id))
            process = psutil.Process(process_id.value)
            window_title_length = user32.GetWindowTextLengthW(hwnd) + 1
            window_title = ctypes.create_unicode_buffer(window_title_length)
            user32.GetWindowTextW(hwnd, window_title, window_title_length)
            process_name = process.name()
            process_path = process.exe()
            process_create_time = process.create_time()

            # Imprimir informações da janela e do processo
            print("Window Title:", window_title.value)
            print("Process ID:", process_id.value)
            print("Process Name:", process_name)
            print("Process Path:", process_path)
            print("Process Create Time:", process_create_time)
            print("---")

        return True

    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))

    def enum_windows_callback(hwnd, lParam):
        enum_windows(hwnd, lParam)
        return True

    user32.EnumWindows(EnumWindowsProc(enum_windows_callback), 0)

def monitor_file_changes():
    class FileEventHandler(FileSystemEventHandler):
        def on_any_event(self, event):
            # Imprimir informações sobre o evento
            print("File Event Type:", event.event_type)
            print("File Event Path:", event.src_path)
            print("File Event Time:", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))

    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(30)  # Aguarda 30 segundos
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

def monitor_system_events_loop():
    while True:
        monitor_system_events()
        monitor_file_changes()

monitor_system_events_loop()