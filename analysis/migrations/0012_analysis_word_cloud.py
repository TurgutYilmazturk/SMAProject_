# Generated by Django 3.1.4 on 2021-02-02 01:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0011_auto_20210202_0319'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='word_cloud',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='media'),
            preserve_default=False,
        ),
    ]
