# Generated by Django 2.0.2 on 2018-04-04 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20180404_0131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='date',
            field=models.DateTimeField(verbose_name='date of announcement'),
        ),
    ]
