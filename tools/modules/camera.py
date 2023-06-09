import subprocess

def linux():
    # Verificar se o pacote v4l-utils está instalado
    result = subprocess.run(['dpkg', '-s', 'v4l-utils'], capture_output=True, text=True)

    if result.returncode != 0:
        print('Pacote v4l-utils não encontrado. Instalando...')
        # Executar o comando de instalação do pacote v4l-utils
        subprocess.run(['sudo', 'apt', 'install', 'v4l-utils'])
    else:
        print('Pacote v4l-utils já está instalado')

# Instalar o pacote v4l-utils (se necessário)
# linux()

import win32com.client as com

def windows():
    wmi = com.GetObject('winmgmts:')
    devices = wmi.InstancesOf('Win32_PnPEntity')

    for device in devices:
        if 'camera' in device.Caption.lower():
            return device.DeviceID

    return None

def led_windows(device_id):
    wmi = com.GetObject('winmgmts:')
    devices = wmi.InstancesOf('Win32_PnPEntity')

    for device in devices:
        if device.DeviceID == device_id:
            device.Disable()

# Obtenha o identificador do dispositivo da câmera
device_id = windows()

if device_id:
    print('Identificador do dispositivo da câmera:', device_id)
    # Desabilite a câmera
    led_windows(device_id)
else:
    print('Dispositivo de câmera não encontrado')
