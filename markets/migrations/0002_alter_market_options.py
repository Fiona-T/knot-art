# Generated by Django 3.2 on 2022-03-31 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='market',
            options={'ordering': ['-date']},
        ),
    ]
