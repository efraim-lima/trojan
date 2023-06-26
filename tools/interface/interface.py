import os
import sys
import importlib

# Obtenha o caminho absoluto da pasta 'functions' dois níveis acima do diretório deste arquivo
functions_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Adicione o diretório ao caminho de busca do Python
sys.path.insert(0, functions_path)

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from interface_logs import LogsAppGUI
from interface_cpu import generate_cpu_graph

# Crie a instância do aplicativo Dash
app = dash.Dash(__name__)

# Defina o layout da página principal
app.layout = html.Div([
    html.H1("Dashboard"),
    dcc.Graph(id="cpu-graph"),
    dcc.Textarea(
        id="logs-textarea",
        rows=10,
        readOnly=True
    )
])

# Crie a instância da classe LogsAppGUI para atualizar o componente de textarea com os logs em tempo real
logs_app = LogsAppGUI(app)

# Defina a callback para atualizar o gráfico de uso da CPU
@app.callback(
    Output("cpu-graph", "figure"),
    Input("logs-textarea", "value")  # Pode usar o valor do textarea como input se necessário
)
def update_cpu_graph(logs_value):
    # Aqui você pode chamar a função generate_cpu_graph() do módulo cpu.py para atualizar o gráfico de uso da CPU
    cpu_figure = generate_cpu_graph()
    return cpu_figure

# Execute o aplicativo Dash
if __name__ == "__main__":
    app.run_server(debug=True)