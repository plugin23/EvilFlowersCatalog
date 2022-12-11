# Generated by Django 3.1.7 on 2021-02-21 20:21

import apps.core.managers.user
import apps.core.models.acquisition
import apps.core.models.base
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid

from apps.files.storage import get_storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=30)),
                ('surname', models.CharField(max_length=150)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'users',
                'default_permissions': ('add', 'delete'),
            },
            managers=[
                ('objects', apps.core.managers.user.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Acquisition',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('relation', models.CharField(choices=[('acquisition', 'acquisition'), ('open-access', 'open-access')], default='acquisition', max_length=20)),
                ('mime', models.CharField(choices=[('application/pdf', 'PDF'), ('application/epub+zip', 'EPUB'), ('application/x-mobipocket-ebook', 'MOBI')], max_length=100)),
                ('content', models.FileField(max_length=255, null=True, storage=get_storage, upload_to=apps.core.models.acquisition.Acquisition._upload_to_path)),
            ],
            options={
                'verbose_name': 'Acquisition',
                'verbose_name_plural': 'Acquisitions',
                'db_table': 'acquisitions',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
                'db_table': 'authors',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('url_name', models.SlugField(unique=True)),
                ('title', models.CharField(max_length=100)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='catalogs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Catalog',
                'verbose_name_plural': 'Catalogs',
                'db_table': 'catalogs',
                'default_permissions': (),
                'unique_together': {('creator_id', 'title')},
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('term', models.CharField(max_length=255)),
                ('label', models.CharField(max_length=255, null=True)),
                ('scheme', models.CharField(max_length=255, null=True)),
                ('catalog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.catalog')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'db_table': 'categories',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=3, unique=True)),
            ],
            options={
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currencies',
                'db_table': 'currencies',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('native_name', models.CharField(max_length=100, null=True)),
                ('code', models.CharField(max_length=2, unique=True)),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
                'db_table': 'languages',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('value', models.DecimalField(decimal_places=4, max_digits=12)),
                ('acquisition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='core.acquisition')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.currency')),
            ],
            options={
                'verbose_name': 'Price',
                'verbose_name_plural': 'Prices',
                'db_table': 'prices',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('identifiers', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), null=True, size=None)),
                ('title', models.CharField(max_length=255)),
                ('summary', models.TextField(null=True)),
                ('content', models.TextField(null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='core.author')),
                ('catalog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='core.catalog')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='core.category')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.language')),
            ],
            options={
                'verbose_name': 'Entry',
                'verbose_name_plural': 'Entries',
                'db_table': 'entries',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.author')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.entry')),
            ],
            options={
                'verbose_name': 'Contributor',
                'verbose_name_plural': 'Contributors',
                'db_table': 'contributors',
                'default_permissions': (),
            },
        ),
        migrations.AddField(
            model_name='author',
            name='catalog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.catalog'),
        ),
        migrations.CreateModel(
            name='ApiKey',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('platform', models.TextField(choices=[('debug', 'debug'), ('custom', 'custom'), ('user', 'user')], default='user', max_length=20)),
                ('secret', models.CharField(max_length=30)),
                ('is_active', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'API key',
                'verbose_name_plural': 'API keys',
                'db_table': 'api_keys',
                'default_permissions': (),
            },
        ),
        migrations.AddField(
            model_name='acquisition',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acquisitions', to='core.entry'),
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(max_length=100)),
                ('url_name', models.SlugField()),
                ('kind', models.CharField(choices=[('navigation', 'navigation'), ('acquisition', 'acquisition')], max_length=20)),
                ('source', models.CharField(choices=[('relation', 'relation')], max_length=20)),
                ('content', models.TextField()),
                ('per_page', models.IntegerField(null=True)),
                ('catalog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feeds', to='core.catalog')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('entries', models.ManyToManyField(related_name='feeds', to='core.Entry')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subsections', to='core.feed')),
            ],
            options={
                'verbose_name': 'Catalog',
                'verbose_name_plural': 'Catalogs',
                'db_table': 'feeds',
                'default_permissions': (),
                'unique_together': {('creator_id', 'title'), ('creator_id', 'url_name')},
            },
        ),
    ]
