# Generated by Django 3.2.6 on 2021-08-28 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal_area', '0002_auto_20210822_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='unique_code',
            field=models.CharField(default='', max_length=20, verbose_name='Код задания'),
            preserve_default=False,
        ),
    ]