import socket
import threading
import time
import pymongo
import nmap
import psutil

# Configurações do MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["outputs"]
collection = db["port_results"]

def get_application_name(port):
    for conn in psutil.net_connections():
        if conn.status == "ESTABLISHED" and conn.laddr.port == port:
            return psutil.Process(conn.pid).name()
    return "Desconhecido"

def get_service_info(port):
    try:
        nm = nmap.PortScanner()
        nm.scan("localhost", str(port))
        service_info = nm["localhost"]["tcp"][port]
        service_name = service_info["name"]
        last_seen = time.ctime(service_info["lasttime"])
        if service_name.lower() == "unknown":
            service_name = get_service_name_from_file(port)
    except:
        service_name = get_service_name_from_file(port)
        last_seen = ""

    return service_name, last_seen

def get_service_name_from_file(port):
    try:
        with open("/etc/services") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    parts = line.split()
                    if len(parts) > 1 and parts[1].isdigit() and int(parts[1]) == port:
                        return parts[0]
    except:
        pass

    return "Desconhecido"

def check_ports(host, start_port, end_port):
    open_ports = []

    def scan_port(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((host, port))
        if result == 0:
            service_name, last_seen = get_service_info(port)
            print(f"A porta {port} está aberta")
            print(f"Serviço: {service_name}")
            print(f"Última vez verificada: {last_seen}")
            application_name = get_application_name(port)
            print(f"Aplicação: {application_name}")
            open_ports.append((port, service_name, last_seen, application_name))

        sock.close()

    while True:
        open_ports.clear()  # Limpa a lista de portas abertas a cada iteração

        threads = []
        for port in range(start_port, end_port + 1):
            thread = threading.Thread(target=scan_port, args=(port,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        print("Lista de portas abertas:")
        for port, service_name, last_seen, application_name in open_ports:
            print(f"Porta {port}: {service_name}")
            print(f"Última vez verificada: {last_seen}")
            print(f"Aplicação: {application_name}")

        # Salva os resultados em um dicionário
        port_results = {
            "timestamp": time.time(),
            "open_ports": open_ports
        }

        # Insere o dicionário na coleção do MongoDB
        collection.insert_one(port_results)

        time.sleep(60)  # Aguarda 60 segundos antes de repetir a varredura

# Exemplo de uso
host = "localhost"
start_port = 1
end_port = 65535

check_ports(host, start_port, end_port)