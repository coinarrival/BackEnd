# Generated by Django 2.1.4 on 2019-06-11 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='account_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200, unique=True)),
                ('email', models.CharField(max_length=200, unique=True)),
                ('phone', models.CharField(max_length=200, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('avatar', models.CharField(default='', max_length=200)),
            ],
        ),
    ]
