# Generated by Django 3.1.4 on 2021-01-21 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='per_page',
            field=models.IntegerField(null=True),
        ),
    ]