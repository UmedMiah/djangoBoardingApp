from django.shortcuts import resolve_url
import pytest
from django.test import TestCase
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest, HttpResponseRedirect, request
from django.test import RequestFactory
from django.urls import reverse
import urllib.parse

from boarding.views import RemoveAccess, Index
from django.test import TestCase, Client
from boarding.models import User, UserAccess, Products
from boarding.templatetags import access_check
from boarding.tests.factories import ProductsFactory, UserFactory
from boarding.views import (
    user_detail_view,
    remove_access,
    index
)

pytestmark = pytest.mark.django_db

class TestIndex(TestCase):

    def test_authenticated(self):
        self.client.login(username='username', password='password')
        response = self.client.get(reverse("index"))
        assert response.status_code == 200

class TestUserDetailView:

    def test_authenticated(self, user: User, rf: RequestFactory, user_factory):
        request = rf.get("/url/")
        request.user = user_factory.build()

        response = user_detail_view(request, username=user.username)

        assert response.status_code == 200

    def test_not_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/url/")
        request.user = AnonymousUser()

        response = user_detail_view(request, username=user.username)

        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == 302

class TestRemoveAccess():

    def test_delete_access(self, rf, client, django_user_model, access_factory):
        user_access = access_factory.create()

        test_user = django_user_model.objects.create(
                          username='username',
                          password='password',
                          is_superuser=True,
                          is_staff=True
                        )

        client.login(username='username', password='password')

        request = rf.post(
                            reverse(
                                    viewname='remove',
                                    kwargs={'pk': user_access.pk}
                                   )
                        )

        request.user = test_user
        response = RemoveAccess.as_view()(request, **{'pk': user_access.pk})

        assert response.status_code == 302

        assert not UserAccess.objects.filter(pk=user_access.pk).exists()

        assert '/user/' + user_access.user.username == urllib.parse.unquote(response.url)

class TestRegister():
    def test_register_pass(self, client):
        data = {
                'username': 'AUserName',
                'firstname': 'John',
                'surname': 'Doe',
                'email': 'email@email.com',
                'password': 'PaSsW0rD3',
                'repeatPassword': 'PaSsW0rD3',
                }
        
        url = reverse('register')

        response = client.post(url, data)

        assert response.status_code == 302     


class TestTeam(TestCase):

    def test_authenticated(self):
        self.client.login(username='username', password='password', is_superuser=True)
        response = self.client.get(reverse("team"))
        assert response.status_code == 200

class TestAddAccess():
    def test_add_access(user: User, admin_client):
        userChoosen = UserFactory.create()
        product = ProductsFactory.create()
        response = admin_client.post(reverse('addaccess', kwargs={'userPK': userChoosen.pk, 'productPK': product.pk}))
        assert response.status_code == 302
        assert access_check.checkAccess(product, UserAccess.objects.all())
