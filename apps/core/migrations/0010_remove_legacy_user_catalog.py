# Generated by Django 4.0.2 on 2022-02-12 17:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_removed_native_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apikey',
            options={'default_permissions': ('add',), 'verbose_name': 'API key', 'verbose_name_plural': 'API keys'},
        ),
        migrations.RemoveField(
            model_name='catalog',
            name='users',
        ),
        migrations.CreateModel(
            name='UserCatalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.CharField(choices=[('read', 'Read'), ('write', 'Write'), ('manage', 'Manage')], max_length=10)),
                ('catalog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.catalog', related_name='user_catalogs')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, related_name='user_catalogs')),
            ],
            options={
                'verbose_name': 'User catalog',
                'verbose_name_plural': 'User catalogs',
                'db_table': 'user_catalogs',
                'default_permissions': (),
            },
        ),
    ]
