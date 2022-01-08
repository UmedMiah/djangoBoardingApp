import pytest
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest, HttpResponseRedirect
from django.test import RequestFactory
from django.urls import reverse

from boarding.models import User
from boarding.tests.factories import UserFactory
from boarding.views import (
    user_detail_view,
    remove_access,
    index
)

pytestmark = pytest.mark.django_db

