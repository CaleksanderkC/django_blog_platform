# Generated by Django 2.1.7 on 2019-04-18 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20190418_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='theme/static/theme/img/red_logo.png', upload_to='src'),
        ),
    ]
