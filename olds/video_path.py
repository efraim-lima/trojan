import pypower
import pyudev
import objc
import wmi

# Obter o caminho do dispositivo de vídeo no Linux
def linux():
    context = pyudev.Context()
    devices = context.list_devices(subsystem='video4linux')
    
    for device in devices:
        if 'video' in device.sys_path:
            return device.device_node

    return None

# Exemplo de uso
video_device_path = linux()
print("Caminho do dispositivo de vídeo no Linux:", video_device_path)

# Obter o caminho do dispositivo de vídeo no Windows
def windows():
    c = wmi.WMI()
    devices = c.Win32_PnPEntity(ConfigManagerErrorCode=0)
    
    for device in devices:
        if 'video' in device.Description.lower():
            return device.DeviceID.split('\\')[-1]

    return None

# Exemplo de uso
video_device_path = windows()
print("Caminho do dispositivo de vídeo no Windows:", video_device_path)


# Obter o caminho do dispositivo de vídeo no ChromeOS
def chromeos():
    power = pypower.Power()
    devices = power.GetPowerState().device
    
    for device in devices:
        if 'video' in device:
            return device

    return None

# Exemplo de uso
video_device_path = chromeos()
print("Caminho do dispositivo de vídeo no ChromeOS:", video_device_path)


# Obter o caminho do dispositivo de vídeo no macOS
def macos():
    io_service = objc.CFRunLoopSourceCreate(None, 0)
    devices = objc.IOServiceGetMatchingServices(
        objc.kIOMasterPortDefault,
        objc.IOServiceMatching('IOVideo'),
    )

    while True:
        device = objc.IOIteratorNext(devices)
        if not device:
            break

        path = objc.IORegistryEntryGetPath(device, 'IOService')
        if 'video' in path.lower():
            return path

    return None

# Exemplo de uso
video_device_path = macos()
print("Caminho do dispositivo de vídeo no macOS:", video_device_path)
