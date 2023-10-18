from django.db import models
from django.contrib.postgres.fields import ArrayField


class MlModel(models.Model):
    """
    Обученная модель МО (путь к ней на диске) с названием, описанием и списком входных параметров
    """
    title = models.CharField(max_length=80, blank=False, verbose_name='Название модели')
    tags = models.ManyToManyField('ModelTag', blank=True, related_name='models_with_tag', verbose_name='Тэги модели')
    description = models.CharField(max_length=255, blank=True, verbose_name='Описание модели')
    ml_model = models.FileField(upload_to='ml_models/', blank=True, verbose_name='Файл модели МО')
    inputs = ArrayField(models.CharField(max_length=25, blank=True, db_index=True, verbose_name='Имена принимаемых входных данных'))

    def __str__(self):
        return self.title


class ModelTag(models.Model):
    """
    Тэг модели МО - сфера применения модели
    """
    tag = models.CharField(max_length=80, blank=False, unique=True, verbose_name='Тэг модели')

    def __str__(self):
        return self.tag
