# Bem-vindo ao meu repositório! 👋

## Aviso Importante

O objetivo deste repositório é puramente acadêmico e todas as informações e códigos aqui fornecidos devem ser usados apenas para fins educacionais e de aprendizado. É crucial ressaltar que qualquer uso inadequado e/ou ilícito dessas informações é estritamente proibido. Portanto, algumas funcionalidades estão sendo mascaradas para evitar o uso indevido e/ou malicioso desse material.

## Sobre mim
🔒🔍📊🔑🌐🛡️🔬🚀⛓️🕵️‍♂️

Meu nome é Efraim Lima e sou um entusiasta da cibersegurança, mergulhando em um campo fascinante que é amplamente discutido devido às inúmeras situações em que a falta de medidas de segurança adequadas tem causado complicações significativas tanto para indivíduos quanto para empresas. Meu foco de estudo está voltado para a inteligência em segurança cibernética, resposta a incidentes e espionagem.

## Como me encontrar

Se você está interessado em saber mais sobre os conceitos, trocar ideias ou contribuir com o projeto, sinta-se à vontade para entrar em contato comigo através do [LinkedIn](https://www.linkedin.com.br/in/efraimlima). Acredito que o compartilhamento de conhecimento é essencial para o avanço da segurança cibernética. 👥

🔒🔍📊🔑🌐🛡️🔬🚀⛓️🕵️‍♂️
## Experiência e Conhecimentos

- 👨‍💼 Embora eu não tenha experiência direta na área de cibersegurança, adquiri conhecimentos sobre diversas técnicas, especialmente na área de inteligência em segurança cibernética e resposta a incidentes;
- 🚀 Estou constantemente buscando aprender novas tecnologias e práticas relacionadas à segurança cibernética;
- 🔍 Tenho interesse particular no estudo do desenvolvimento de malwares, como Trojans, Spywares e Worms, bem como nos processos de Command & Control (C&C) que permitem o controle desses malwares;
- ⛓️ Tenho conhecimento sobre a Kill Chain, uma estrutura que descreve as etapas pelas quais um ataque cibernético passa, desde o reconhecimento inicial até a exfiltração de dados e o impacto no alvo.

## Projetos

Este repositório contém alguns projetos e scripts relacionados à segurança cibernética, incluindo:

- 📁 `instalação`: O projeto procura automatizar todo processo de instalação em um host para minimizar o trabalho durante o momento de infecção do alvo. Dessa forma o tempo para início da ação de reconhecimento é reduzido;

- ⚙️ `command & control (C2)`: O objetivo dessa etapa é estabelecer uma porta aberta e sempre disponível para que o atacante possa enviar comandos via CLI de maneira remota para a máquina alvo, proporcionando maior flexibilidade para um reconhecimento mais estruturado e pleno;

- 🖥️ `screen`: O pretexto da existencia dessa ferramenta é capturar a tela do usuário e armazenar pequenos volumes de vídeo dessa captura em um banco de dados para analisar posteriormete; junto a função de capturar a tela temos outra que pretende capturar o audio que sairia do device, mas ainda não foi completamente testado.

- 🕵️‍♂️ `spyware`: Todo o projeto funciona como um spyware, capturando informações do alvo e armazenando em um banco de dados;

- ⌨️ `keylogger`: Este projeto mostra a implementação de um keylogger, uma ferramenta que registra todas as teclas pressionadas em um sistema. Em minha funcionalidade do keylogger também implementei uma função de analise das palavras que será muito útil posteriormente para analisar palavras repetidas capturadas e elencar por prioridade.

- 📷 `captura de imagens`: Exploro também a captura de fotos e vídeos da câmera, com o objetivo de compilar informações visuais para analise posterior. Este módulo ainda não comporta inibição da ativação do led das câmeras;

- 🎤 `audio`: Aqui estudo como poderia capturar o audio da máquina, de maneira a compreender que este tipo de funcionalidade poderia passar desapercebida pelo sistema por não acionar funcionalidades extras, mas digo isso apenas neste projeto e em analises preeliminares. Caso venha disfarçado de um trojan seria de difícil detecção;

- 📊 `logs`: Na parte de analise de logs procuro catalogar todo e qualquer tipo de alteração no sistema, assim como: arquivos alterados, aplicações (iniciação, fechamento e suspensão), eventos de inicialização e modificação de aplicações;

- 🌐 `rede`: No quesito redes temos um módulo chamado "network" que analisa todas portas abertas na rede local, avalia qual serviçõ está em execução naquela interface, procura sua pasta origem e analisa cada arquivo nesse diretório gerando o hash dao arquivo e comparando com provedores de antivirus através da conexão de uma API;

- 🗑️ `trash`: Concluo limpando automaticamente todos arquivos que foram deletados durante as varreduras para não sobrecarregar ainda mais o host alvo. Futuramente a meta é conseguir apagar rastros no sistema assim como logs, portas abertas e históricos;


## Estrutura do Código

A estrutura do código neste repositório é organizada da seguinte maneira:

- root
│   C2.py
│   commandandcontrol.py
│   duckyscript.sh
│   encryption_key.txt
│   play.py
│   start.service
│   start.sh
│
└───modules
    │   analysis.py
    │   audio.py
    │   camera.py
    │   config.txt
    │   cpu.py
    │   database.py
    │   data_collecrion.py
    │   images.py
    │   installer.py
    │   keyboards.py
    │   logs.py
    │   network.py
    │   packets.py
    │   screens.py
    │   system.py
    │   trash.py
    │   videos.py
    │
    └───logs
           file_logs.txt
           system_logs.txt

            



<!-- 

CASO ERRO COM GPG:

I recently found the same secret key not available error and a few more along the way, like GPG agent not found for instance.

In my case I wanted to get commits signed and showing as verified on GitHub.

Below are the complete steps to get it working on Windows 10 x64:

Install GPG
I installed GPG 2.3.1 with winget like so:

C:\> winget install GnuPG.GnuPG
Verify it with:

C:\> gpg --version
Generate GPG key
C:\> gpg --full-generate-key
Add your real name and e-mail, the same as used in the GitHub account.

The key must be at least 4096 bits.

Export the key in ASCII armor format
First list the key:

C:\> gpg --list-secret-keys --keyid-format=long
sec rsa4096/[short-key] 2021-06-14 [SC]

Then export it:

C:\> gpg --armor --export [short-key]
Copy the key including the BEGIN/END text.

-----BEGIN PGP PUBLIC KEY BLOCK-----
[huge-ascii-key]
-----END PGP PUBLIC KEY BLOCK-----
Add the GPG armor ASCII key to the GitHub account
Go to Profile > Settings > SSH and GPG keys > New GPG key

Or please follow these visual instructions.

Configure Git to sign all commits by default
C:\> git config --global user.signingkey [short-key]
C:\> git config --global commit.gpgsign true
C:\> git config --global gpg.program "C:/Program Files (x86)/gnupg/bin/gpg"
Set GPG environment variable for the GPG Agent
Check for GPG agent:

gpg-agent --version
Set the environment variable:

GNUPGHOME=%USERPROFILE%\AppData\Roaming\gnupg
Done
The resulting .gitconfig would have the user section like so:

[user]
    name = Your Name
    email = your@email.com
    signingkey = [short-key]
[commit]
    gpgsign = true
[gpg]
    program = C:/Program Files (x86)/gnupg/bin/gpg






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