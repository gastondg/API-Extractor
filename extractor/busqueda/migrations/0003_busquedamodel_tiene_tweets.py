# Generated by Django 2.2.4 on 2019-09-04 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('busqueda', '0002_auto_20190824_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='busquedamodel',
            name='tiene_tweets',
            field=models.BooleanField(default=False),
        ),
    ]