# Generated by Django 3.0.8 on 2020-11-22 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collect', '0002_auto_20201121_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participation',
            name='admission',
            field=models.BooleanField(default=False, verbose_name='승인 상태'),
        ),
    ]
