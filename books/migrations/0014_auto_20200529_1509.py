# Generated by Django 3.0.5 on 2020-05-29 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0013_auto_20200529_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_avatar',
            field=models.ImageField(blank=True, null=True, upload_to='media/avatar'),
        ),
    ]
