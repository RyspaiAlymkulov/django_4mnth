import uuid

from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=100)


class Film(models.Model):
    class Meta:
        verbose_name = 'фильм'
        verbose_name_plural = 'фильмы'
    image = models.ImageField(null=True, upload_to='film', verbose_name='Картинка')
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    link = models.URLField(verbose_name='Ссылка')
    producer = models.TextField(null=True, verbose_name='Режиссер')
    rating = models.FloatField(default=0, verbose_name='Рейтинг')
    duration = models.DurationField(null=True, verbose_name='Длительность')

    def __str__(self):
        return self.title


class Review(models.Model):
    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
    text = models.TextField(verbose_name='Текст')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, null=True, verbose_name='Название фильма')
    id = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.text
