import traceback
from http import HTTPStatus
from typing import Tuple

import sentry_sdk
from django.conf import settings
from django.utils.text import slugify
from django_api_forms.forms import Form

from django.utils.translation import gettext as _


class ProblemDetailException(Exception):
    def __init__(
        self,
        request,
        title: str,
        status: int = HTTPStatus.INTERNAL_SERVER_ERROR,
        previous: Exception = None,
        to_sentry: bool = False,
        additional_data: dict = None,
        detail_type: str = None,
        detail: str = None,
        extra_headers: Tuple[Tuple] = None
    ):
        super().__init__(title)

        self._request = request
        self._status_code = status
        self._title = title
        self._type = detail_type
        self._detail = detail
        self._previous = previous
        self._extra_headers = extra_headers

        if additional_data:
            self._additional_data = additional_data
        else:
            self._additional_data = {}

        if to_sentry:
            with sentry_sdk.push_scope() as scope:
                for key, value in self.__dict__.items():
                    scope.set_extra(key, value)
                sentry_sdk.capture_exception(self)

    @property
    def request(self):
        return self._request

    @property
    def status(self) -> int:
        return self._status_code

    @property
    def title(self) -> str:
        return self._title

    @property
    def detail(self) -> str:
        return self._detail

    @property
    def type(self) -> str:
        return self._type

    @property
    def previous(self) -> Exception:
        return self._previous

    @property
    def extra_headers(self) -> Tuple[Tuple]:
        return self._extra_headers

    @property
    def payload(self) -> dict:
        result = {
            'title': self.title
        }

        if settings.DEBUG:
            result['trace'] = traceback.format_exc().split("\n")

        return result


class UnauthorizedException(ProblemDetailException):
    def __init__(self, request):
        super().__init__(
            request,
            _("Unauthorized"),
            status=HTTPStatus.UNAUTHORIZED,
            extra_headers=(
                ('WWW-Authenticate', f'Bearer realm="{slugify(settings.INSTANCE_NAME)}"'),
            )
        )


class ValidationException(ProblemDetailException):
    def __init__(self, request, form: Form):
        super().__init__(request, _("Validation error!"), status=HTTPStatus.UNPROCESSABLE_ENTITY)
        self._form = form

    @property
    def payload(self) -> dict:
        payload = super(ValidationException, self).payload
        payload['validation_errors'] = self._form.errors
        return payload
