# Generated by Django 2.2.4 on 2020-06-16 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zeroxpapp', '0003_auto_20200531_1830'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailLeads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('email', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'email_leads',
            },
        ),
    ]