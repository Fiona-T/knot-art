# Generated by Django 3.2 on 2022-04-14 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0004_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='market',
            name='image_url',
        ),
    ]
