import os
import sys

# Defina o DJANGO_SETTINGS_MODULE antes de importar qualquer coisa do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Certifique-se de que o diretório do projeto esteja no sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from pymongo import MongoClient
from django.db import models
import datetime
import uuid


client = MongoClient('localhost', 27017)
db = client['trojany']  # Substitua 'your_database_name' pelo nome do seu banco de dados MongoDB


from django.db import models

# # Create your models here.
# class Admin(models.Model):
# 	# employee_id = models.CharField(max_length=20)
# 	employee_name = models.CharField(max_length=20)
# 	# mobile_number = models.PositiveIntegerField()
# 	employee_title = models.CharField(max_length=10)
 
class Day(models.Model):
    id = models.IntegerField(primary_key=True)  # Ensure id is defined as IntegerField
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.CharField(max_length=100,unique=True,)
    # _id = models.ObjectIdField(auto_created=True, serialize=False)
    
    class Meta:
        app_label = 'models_day'  # Nome do aplicativo que contém o modelo
        db_table = 'models_day'
        # ordering = ['published_date', 'author']
        # get_latest_by = ""
        verbose_name = 'day'
        verbose_name_plural = 'days'
        
    def __str__(self):
        return self.date

    def get_pass_event(self):
        today = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        event = self.event_date.strftime('%Y-%m-%dT%H:%M:%S')

        if event < today:
            return True
        else:
            return False

class AppsLog(models.Model):
    day = models.ForeignKey(
        Day, 
        on_delete=models.PROTECT,
        related_name='appslog',
        unique=False,
        to_field='date',
        )
    event_time = models.DateTimeField()
    event_source = models.CharField(max_length=1000)
    event_category = models.CharField(max_length=1000)
    event_description = models.CharField(max_length=1000)
    process_name = models.CharField(max_length=1000)
    pid = models.IntegerField()
    ppid = models.IntegerField()
    status = models.CharField(max_length=1000)
    memory_info = models.JSONField()
    cpu_times = models.JSONField()
    total_events = models.CharField(max_length=100)

    class Meta:
        app_label = 'models_appslog'  # Nome do aplicativo que contém o modelo

    def __str__(self):
        return str(self.date)

class FileLog(models.Model):
    day = models.ForeignKey(
        Day, 
        on_delete=models.PROTECT,
        related_name='filelog',
        unique=False,
        to_field='date',  # Update the to_field parameter to 'date'
    )
    file_name = models.CharField(max_length=1000)
    file_size = models.CharField(max_length=1000)
    event_type = models.CharField(max_length=1000)
    event_path = models.CharField(max_length=1000)
    event_time = models.DateTimeField()

    class Meta:
        app_label = 'models_filelog'
        db_table = 'file'
        verbose_name = 'file'
        verbose_name_plural = 'files'

    def __str__(self):
        return str(self.date)

    
class KeywordsData(models.Model):
    day = models.ForeignKey(Day, on_delete=models.PROTECT)
    filename = models.CharField(max_length=1000)
    timestamp = models.DateTimeField()
    keys_list = models.CharField(max_length=1000, blank=True, null=True)
    keys_str = models.CharField(max_length=1000)
    words = models.IntegerField()

    class Meta:
        app_label = 'models_keywords'  # Nome do aplicativo que contém o modelo

class ImageData(models.Model):
    name = models.CharField(max_length=1000)
    day = models.ForeignKey(Day, on_delete=models.PROTECT)
    image = models.BinaryField()

    class Meta:
        app_label = 'models_imagedata'  # Nome do aplicativo que contém o modelo

class VideoData(models.Model):
    name = models.CharField(max_length=1000)
    day = models.ForeignKey(Day, on_delete=models.PROTECT)
    video = models.BinaryField()

    class Meta:
        app_label = 'models_video'  # Nome do aplicativo que contém o modelo

class AudioData(models.Model):
    name = models.CharField(max_length=1000)
    day = models.ForeignKey(Day, on_delete=models.PROTECT)
    audio = models.BinaryField()

    class Meta:
        app_label = 'models_audio'  # Nome do aplicativo que contém o modelo

class ScreenImageData(models.Model):
    name = models.CharField(max_length=1000)
    day = models.ForeignKey(Day, on_delete=models.PROTECT)
    screen_image = models.BinaryField()

    class Meta:
        app_label = 'models_screen_image'  # Nome do aplicativo que contém o modelo

class ScreenVideoData(models.Model):
    name = models.CharField(max_length=1000)
    day = models.ForeignKey(Day, on_delete=models.PROTECT)
    screen_video = models.BinaryField()

    class Meta:
        app_label = 'models_screen_video'  # Nome do aplicativo que contém o modelo

class ScreenAudioData(models.Model):
    name = models.CharField(max_length=1000)
    day = models.ForeignKey(Day, on_delete=models.PROTECT)
    screen_audio = models.BinaryField()

    class Meta:
        app_label = 'models_screen_audio'  # Nome do aplicativo que contém o modelo