# Generated by Django 3.1.4 on 2021-02-02 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0008_auto_20210202_0210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis',
            name='limit',
            field=models.IntegerField(verbose_name='Count of "Top Posts" to be searched in Reddit.Default value=all'),
        ),
    ]