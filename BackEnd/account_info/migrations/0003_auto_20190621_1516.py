# Generated by Django 2.1.4 on 2019-06-21 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_info', '0002_auto_20190621_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(max_length=30),
        ),
    ]