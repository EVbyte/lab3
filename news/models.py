from django.contrib.auth.models import User
from django.db import models


class Articles(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='Автор Статьи', blank=True, null=True)

    objects = models.Manager()
    title = models.CharField(max_length=120)
    post = models.TextField()
    date = models.DateTimeField(auto_now=True)
    image_p = models.ImageField(null=True, blank=True, upload_to='media/articles', verbose_name="Картинка")

    def __str__(self):
        return self.title


class Comments(models.Model):
    article = models.ForeignKey(Articles, on_delete = models.CASCADE, verbose_name='Статья', blank = True, null = True,related_name='comments_articles' )
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name='Автор комментария', blank = True, null = True )
    create_date = models.DateTimeField(auto_now=True)
    text = models.TextField(verbose_name='Текст комментария')
    status = models.BooleanField(verbose_name='Видимость статьи', default=False)
