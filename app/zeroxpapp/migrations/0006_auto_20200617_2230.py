# Generated by Django 2.2.4 on 2020-06-17 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zeroxpapp', '0005_auto_20200616_0010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joblistings',
            name='job_id',
            field=models.CharField(default='', max_length=100),
        ),
    ]
