# Generated by Django 4.0.3 on 2022-03-31 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_identifiers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='language',
            old_name='code',
            new_name='alpha2',
        ),
        migrations.AddField(
            model_name='language',
            name='alpha3',
            field=models.CharField(max_length=3, null=True),
        ),
    ]
