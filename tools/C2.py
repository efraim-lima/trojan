import subprocess
import os

def create_user(username, password):
    # Cria o usuário com a senha especificada
    subprocess.run(['sudo', 'useradd', '-m', '-p', password, username])

def generate_ssh_key(username):
    # Gera um par de chaves SSH para o usuário especificado
    ssh_dir = f"/home/{username}/.ssh"
    os.makedirs(ssh_dir, exist_ok=True)
    subprocess.run(['sudo', '-u', username, 'ssh-keygen', '-t', 'rsa', '-N', '', '-f', f"{ssh_dir}/id_rsa"])

def enable_ssh_service():
    # Instala o servidor SSH e inicia o serviço
    subprocess.run(['sudo', 'apt-get', 'install', '-y', 'openssh-server'])
    subprocess.run(['sudo', 'systemctl', 'enable', 'ssh'])
    subprocess.run(['sudo', 'systemctl', 'start', 'ssh'])

def save_users_to_file(users):
    # Salva a lista de usuários e chaves SSH em um arquivo
    with open('users.txt', 'w') as file:
        for user in users:
            file.write(f"{user['username']} {user['ssh_key']}\n")

def main():
    # Lista de usuários e suas respectivas senhas
    users = [
        {'username': 'missa-vespertina-20230401@gmail.com', 'password': 'senha1'},
        # Adicione mais usuários, se necessário
    ]

    for user in users:
        create_user(user['username'], user['password'])
        generate_ssh_key(user['username'])

    enable_ssh_service()
    save_users_to_file(users)

if __name__ == '__main__':
    main()
