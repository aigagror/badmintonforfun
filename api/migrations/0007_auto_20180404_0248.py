# Generated by Django 2.0.2 on 2018-04-04 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20180404_0232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='date',
            field=models.DateField(verbose_name='date of announcement'),
        ),
    ]
