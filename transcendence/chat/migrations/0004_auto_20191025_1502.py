# Generated by Django 2.2.3 on 2019-10-25 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20191025_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='body',
            field=models.TextField(blank=True, default='', verbose_name='body'),
        ),
    ]
