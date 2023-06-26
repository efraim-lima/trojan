import os
import sys
import time

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pymongo

# Obtenha o caminho absoluto da pasta 'functions' dois níveis acima do diretório deste arquivo
functions_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Adicione o diretório ao caminho de busca do Python
sys.path.insert(0, functions_dir)

from functions.cpu import calculate_total_memory_usage

# Configurações do MongoDB
mongodb_url = "mongodb://localhost:27017"
database_name = "mydatabase"
collection_file_name = "file_logs"
collection_system_name = "system_logs"

# Inicialização do aplicativo Dash
app = dash.Dash(__name__)

# Conectar ao banco de dados MongoDB
try:
    client = pymongo.MongoClient(mongodb_url)
    db = client[database_name]
    collection_file = db.get_collection(collection_file_name)
    if collection_file is None:
        collection_file = db.create_collection(collection_file_name)
    collection_system = db.get_collection(collection_system_name)
    if collection_system is None:
        collection_system = db.create_collection(collection_system_name)
except pymongo.errors.ConnectionError as e:
    print("Erro ao conectar ao MongoDB:", e)
    # Lógica para lidar com o erro de conexão, se necessário

# Layout do aplicativo
app.layout = html.Div(
    children=[
        html.Div(
            className="left-panel",
            children=[
                html.H1("Diagnóstico em Tempo Real"),
                html.H2("CPU:"),
                html.H2(id="cpu-output"),
                html.H2("Keylogger:"),
                html.Div(id="keylogger-output"),
                html.Div(id="keylogger-text-output"),
                html.Div(id="keylogs-text-output"),
                dcc.Interval(id="interval-1", interval=2000),  # Atualização a cada 2 segundos
                
            ]
        ),
        html.Div(
            className="right-panel",
            children=[
                html.H1("Análise de Logs"),
                html.H2("Keylogs:"),
                html.Div(id="keylogs-output"),
                html.Button("Dia Anterior", id="keylogs-previous-day"),
                html.Button("Próximo Dia", id="keylogs-next-day"),
                html.H2("Logs do Sistema:"),
                html.Div(id="system-logs-output"),
                html.Button("Dia Anterior", id="system-logs-previous-day"),
                html.Button("Próximo Dia", id="system-logs-next-day"),
                html.Div(id="system-logs-text-output"),
                dcc.Interval(id="logs-interval", interval=2000),  # Atualização a cada 2 segundos
                html.Div(id="logs-analysis-output"),
                dcc.Interval(id="interval-2", interval=2000),  # Atualização a cada 2 segundos
            ]
        ),
    ],
    className="main-container"
)

# Função para atualizar o output do uso de CPU
def update_cpu_output():
    total_memory_usage = calculate_total_memory_usage()
    total_cpu_usage = 100  # Considerando que 100% representa o uso total da CPU

    return f"{total_memory_usage:.2f}%"

# Função para buscar o texto no MongoDB
def fetch_logs_from_collection(collection, timestamp):
    entries = collection.find({"timestamp": {"$gt": timestamp}})
    text = ""
    for entry in entries:
        text += f"{entry['filename']} - {entry['keys_str']}<br>"

    if text == "":
        text = "Aguardando novas entradas..."

    return text

# Função para realizar a análise de logs
def analyze_logs():
    current_time = time.time()
    ten_seconds_ago = current_time - 10

    # Buscar novas entradas no MongoDB
    entries = collection_system.find({"timestamp": {"$gt": ten_seconds_ago}})

    # Analisar e destacar textos importantes
    analyzed_text = ""
    for entry in entries:
        event_name = entry["event_name"]
        event_description = entry["event_description"]

        # Realizar a análise de cada evento e destacar os textos importantes
        # Aqui você pode adicionar sua lógica de análise de logs personalizada

        # Exemplo: destacar eventos com nome "Erro"
        if "Erro" in event_name:
            analyzed_text += f"<b>{event_name}</b> - {event_description}<br>"
        else:
            analyzed_text += f"{event_name} - {event_description}<br>"

    if analyzed_text == "":
        analyzed_text = "Aguardando novas entradas..."

    return analyzed_text

# Callback para atualizar o output do uso de CPU
@app.callback(
    Output("cpu-output", "children"),
    [Input("interval", "n_intervals")]
)
def update_cpu_output_callback(n):
    return update_cpu_output()

# Callback para atualizar o output da análise de logs
@app.callback(
    Output("logs-analysis-output", "children"),
    [Input("logs-interval", "n_intervals")]
)
def update_logs_analysis_output(n):
    return analyze_logs()

# Execução do aplicativo
if __name__ == "__main__":
    app.run_server(debug=True)

# Callback para atualizar o output de texto do keylogger
@app.callback(
    Output("keylogger-text-output", "children"),
    [Input("interval-1", "n_intervals")]
)
def update_keylogger_text_output(n):
    logs_text = fetch_logs_from_collection(collection_file, time.time() - 10)
    return html.Div(logs_text)

# Callback para atualizar o output de texto dos keylogs
@app.callback(
    Output("keylogs-text-output", "children"),
    [Input("keylogs-previous-day", "n_clicks"),
     Input("keylogs-next-day", "n_clicks")]
)
def update_keylogs_text_output(n_previous, n_next):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "keylogs-previous-day" in changed_id:
        # Lógica para ir para o dia anterior
        pass
    elif "keylogs-next-day" in changed_id:
        # Lógica para ir para o próximo dia
        pass
    
    timestamp = time.time() - 24 * 60 * 60  # Exemplo: um dia atrás
    logs_text = fetch_logs_from_collection(collection_file, timestamp)
    return html.Div(logs_text)

# Callback para atualizar o output de texto dos logs do sistema
@app.callback(
    Output("system-logs-text-output", "children"),
    [Input("system-logs-previous-day", "n_clicks"),
     Input("system-logs-next-day", "n_clicks")]
)
def update_system_logs_text_output(n_previous, n_next):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "system-logs-previous-day" in changed_id:
        # Lógica para ir para o dia anterior
        pass
    elif "system-logs-next-day" in changed_id:
        # Lógica para ir para o próximo dia
        pass
    
    timestamp = time.time() - 24 * 60 * 60  # Exemplo: um dia atrás
    logs_text = fetch_logs_from_collection(collection_system, timestamp)
    return html.Div(logs_text)