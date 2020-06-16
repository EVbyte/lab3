from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.template.defaultfilters import slugify as django_slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True,verbose_name="Статус")
    location = models.CharField(max_length=30, blank=True, verbose_name="Местоположение")

    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата Рождения")
    profile_avatar = models.ImageField(null=True, blank=True, upload_to='media/avatar', default='media/avatar/default_img.png',verbose_name="Аватар Профиля")

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Articles(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор Статьи', blank=True, null=True)
    objects = models.Manager()
    writer = models.CharField(max_length=120, verbose_name="Автор книги")
    title = models.CharField(max_length=120, verbose_name="Заголовок")
    post = models.TextField(verbose_name="Текст статьи")
    date = models.DateTimeField(auto_now=True)
    image_p = models.ImageField(null=True, blank=True, upload_to='media/articles', verbose_name="Картинка")
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')

    def __str__(self):
        return self.title


alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya', ' ': ''}


def slugify(s):
    s = s.lower()
    return django_slugify(''.join(alphabet.get(w, w) for w in s))


class Tag(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор Статьи', blank=True, null=True)
    tittle = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('tag_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update', kwargs={'slug': self.slug})

    def __str__(self):
        return '{}'.format(self.tittle)

    def save(self, *args, **kwargs):
        self.author_id = 1
        self.slug = slugify(self.tittle)
        super(Tag, self).save(*args, **kwargs)


class Comments(models.Model):
    article = models.ForeignKey(Articles, on_delete = models.CASCADE, verbose_name='Статья', blank = True, null = True,related_name='comments_articles' )
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name='Автор комментария', blank = True, null = True )
    create_date = models.DateTimeField(auto_now=True)
    text = models.TextField(verbose_name='Текст комментария')
    status = models.BooleanField(verbose_name='Видимость статьи', default=False)


