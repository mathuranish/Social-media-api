# Generated by Django 4.1.3 on 2022-11-27 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_userfollowing_userfollowing_unique_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfollowing',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
