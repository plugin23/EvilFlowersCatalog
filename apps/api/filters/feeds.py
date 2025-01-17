import django_filters

from apps.core.models import Feed, UserCatalog


class FeedFilter(django_filters.FilterSet):
    creator_id = django_filters.UUIDFilter()
    catalog_id = django_filters.UUIDFilter()
    title = django_filters.CharFilter(lookup_expr='unaccent__icontains')
    kind = django_filters.ChoiceFilter(choices=Feed.FeedKind.choices)

    class Meta:
        model = Feed
        fields = []

    @property
    def qs(self):
        qs = super().qs

        if not self.request.user.is_authenticated:
            return qs.filter(catalog__is_public=True)

        if not self.request.user.is_superuser:
            qs = qs.filter(
                catalog__user_catalogs__user=self.request.user,
                catalog__user_catalogs__mode=UserCatalog.Mode.MANAGE
            )

        return qs
