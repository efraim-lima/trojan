# About
        # Neste repositório estou estudando malwares e trojans. Como desenvolver um cavalo de tróia e como aplicar "Command & Control" no processo. O objetivo aqui é completamente acadêmico e este arquivo não deve ser utilizado para fins maliciosos.

<!-- 
# Ative o Linux (Beta) no seu Chromebook. Siga as instruções do Google para habilitar o Linux (Beta): https://support.google.com/chromebook/answer/9145439

# Após habilitar o Linux (Beta), você poderá abrir um terminal Linux e instalar as ferramentas necessárias, como curl e o Python:

        # No terminal Linux, execute o seguinte comando para instalar o curl:

                # sudo apt-get install curl
        # Em seguida, instale o Python:
                # sudo apt-get install python3

# Com as ferramentas instaladas, você poderá executar o exemplo de código mencionado anteriormente no terminal Linux.

# Necessário colocar o script na pasta de inicialização do sistema, seguir as etapas:
        # Abra o aplicativo "Gerenciador de Arquivos" no seu Chromebook.
        # Navegue até a pasta "/etc/init.d/".
        # Mova o script de inicialização (as_init.sh) para essa pasta.

# Mova o script para a pasta de inicialização: Agora, você precisa mover o script de inicialização para a pasta de inicialização do sistema para que ele seja executado automaticamente. Siga as etapas abaixo:

        # Abra o aplicativo "Gerenciador de Arquivos" no seu Chromebook.
        # Navegue até a pasta "/etc/init.d/".
        # Mova o script de inicialização (script_inicializacao.sh) para essa pasta.
        # Dê permissões de execução ao script: Para garantir que o script seja executado corretamente, você precisa dar as permissões adequadas. Siga as etapas abaixo:

# Clique com o botão direito do mouse no script de inicialização (script_inicializacao.sh) na pasta "/etc/init.d/".
        # Selecione "Propriedades".
        # Na guia "Permissões", marque a opção "Permitir execução".

#####################################################################################################################################################################################################
#####################################################################################################################################################################################################
#####################################################################################################################################################################################################
#####################################################################################################################################################################################################
#####################################################################################################################################################################################################
#####################################################################################################################################################################################################
#####################################################################################################################################################################################################
#####################################################################################################################################################################################################

#####Para forlar inicialização do app no ChromeOS:
Abra um dos scripts de inicialização listados abaixo (dependendo da sua distribuição do Linux ou versão do Chrome OS) em um editor de texto:

/etc/rc.local
~/.bashrc
~/.profile
~/.xprofile

Adicione o comando para executar seu script Python no final do arquivo antes do comando exit 0. Por exemplo:
python3 /caminho/para/seu/script.py


##### Segunda abordagem para fazer com que o script rode em ChromeOS após inicialização do sistema:
Crie um arquivo de serviço para o seu script Python com a extensão .service. Por exemplo, meu_script.service.
Abra o arquivo de serviço em um editor de texto e adicione o seguinte conteúdo:

[Unit]
Description=Meu Script Python
After=network.target

[Service]
ExecStart=/usr/bin/python3 /caminho/para/seu/script.py

[Install]
WantedBy=default.target

Mova o arquivo de serviço para o diretório /etc/systemd/system/.
Em seguida, execute o seguinte comando para registrar o serviço:
sudo systemctl enable meu_script.service

#####################################################################################################################################################################################################
#####################################################################################################################################################################################################
#####################################################################################################################################################################################################
#####################################################################################################################################################################################################
#####################################################################################################################################################################################################
#####################################################################################################################################################################################################
#####################################################################################################################################################################################################
#####################################################################################################################################################################################################

Para configurar o dispositivo Digispark Attiny85 USB como um dispositivo Rubber Ducky, você pode seguir estas etapas:

Prepare o Digispark Attiny85: Certifique-se de ter o ambiente de desenvolvimento Arduino IDE configurado corretamente para programar o Digispark Attiny85. Você precisará instalar as bibliotecas e drivers necessários. Siga as instruções fornecidas pelo fabricante do Digispark ou procure tutoriais online para obter orientações detalhadas.

Carregue o script no Digispark Attiny85: Abra o Arduino IDE, crie um novo sketch e copie o script Rubber Ducky adaptado para o sketch. Verifique se o script está dentro dos limites de armazenamento do Digispark Attiny85. Você pode usar as funções setup() e loop() para dividir o script em partes menores, se necessário. Selecione a placa "Digispark (Default - 16.5MHz)" nas opções de placa e as configurações corretas de porta USB. Em seguida, clique em "Carregar" para carregar o sketch no Digispark Attiny85.

Teste o script: Conecte o Digispark Attiny85 a um computador e observe a execução do script. Verifique se todos os comandos são executados conforme o esperado. Faça os ajustes necessários para garantir que o script funcione corretamente.

Verifique a compatibilidade do Digispark Attiny85: Lembre-se de que o Digispark Attiny85 possui recursos limitados, incluindo armazenamento e processamento. Certifique-se de que o script se encaixa dentro dessas limitações. Além disso, verifique se o Digispark Attiny85 é compatível com o sistema operacional em que você deseja executar o script.

Revisão e teste: Antes de executar o script em um ambiente de produção, revise cuidadosamente o código para garantir que todos os comandos estejam corretos e não apresentem riscos. Faça testes adicionais em diferentes sistemas operacionais para verificar a compatibilidade e o funcionamento adequado do script.

#####################################################################################################################################################################################################
#####################################################################################################################################################################################################
#####################################################################################################################################################################################################
#####################################################################################################################################################################################################
#####################################################################################################################################################################################################
#####################################################################################################################################################################################################
#####################################################################################################################################################################################################
#####################################################################################################################################################################################################


        -->