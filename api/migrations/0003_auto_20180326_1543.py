# Generated by Django 2.0.2 on 2018-03-26 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20180325_0456'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='id',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='election',
            name='date',
            field=models.DateField(verbose_name='date of the election'),
        ),
    ]
