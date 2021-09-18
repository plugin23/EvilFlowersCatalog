import base64
from typing import Optional

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from apps.core.models.author import Author
from apps.core.models.language import Language
from apps.core.models.category import Category
from apps.core.models.user import User
from apps.core.models.catalog import Catalog
from apps.core.models.base import BaseModel, private_storage


class Entry(BaseModel):
    class Meta:
        app_label = 'core'
        db_table = 'entries'
        default_permissions = ()
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')

    def _upload_to_path(self, filename):
        return f"catalogs/{self.catalog.url_name}/{self.pk}/{filename}"

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, related_name='entries')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, related_name='entries')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='entries', null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='entries', null=True)
    identifiers = ArrayField(models.CharField(max_length=100), null=True)
    title = models.CharField(max_length=255)
    summary = models.TextField(null=True)
    content = models.TextField(null=True)
    contributors = models.ManyToManyField(
        Author, related_name='contribution_entries', db_table='contributors', verbose_name=_('Contributor'),
    )
    image = models.ImageField(upload_to=_upload_to_path, null=True, max_length=255, storage=private_storage)
    image_mime = models.CharField(max_length=100, null=True)
    thumbnail = models.ImageField(upload_to=_upload_to_path, null=True, max_length=255, storage=private_storage)

    @property
    def image_url(self) -> Optional[str]:
        if not self.image:
            return None
        return f"{settings.BASE_URL}{reverse('cover_download', kwargs={'entry_id': self.pk})}"

    @property
    def thumbnail_base64(self) -> Optional[str]:
        if not self.thumbnail:
            return None
        encoded = base64.b64encode(self.thumbnail.read()).decode('ascii')
        return f"data:{self.image_mime};base64,{encoded}"


__all__ = [
    'Entry'
]
