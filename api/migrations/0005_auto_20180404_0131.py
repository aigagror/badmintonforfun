# Generated by Django 2.0.2 on 2018-04-04 01:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20180404_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bracketnode',
            name='match',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Match'),
        ),
    ]
