# Generated by Django 2.1.7 on 2019-04-18 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20190418_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='src/%Y//%m/%d/'),
        ),
    ]