# Generated by Django 4.2.4 on 2023-10-18 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_alter_user_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, max_length=80),
        ),
    ]
