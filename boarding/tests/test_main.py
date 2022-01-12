from django.contrib.messages.api import get_messages
import pytest
from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
from django.test import RequestFactory
from django.urls import reverse
import urllib.parse

from boarding.views import RemoveAccess
from boarding.models import User, UserAccess
from boarding.templatetags import access_check
from boarding.tests.factories import ProductsFactory, UserFactory
from boarding.views import user_detail_view

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

        request = rf.post(reverse(viewname='remove', kwargs={'pk': user_access.pk}))

        request.user = test_user
        response = RemoveAccess.as_view()(request, **{'pk': user_access.pk})

        assert response.status_code == 302

        assert not UserAccess.objects.filter(pk=user_access.pk).exists()

        assert '/user/' + user_access.user.username == urllib.parse.unquote(response.url)


def test_register(client):
    data = {
            'username': 'AUserName',
            'firstname': 'John',
            'surname': 'Doe',
            'email': 'email@email.com',
            'password': 'PaSsW0rD3!',
            'repeatPassword': 'PaSsW0rD3!',
            }
    url = reverse('register')

    response = client.post(url, data)

    assert response.status_code == 302

# The following tests also cover functions.py 
def test_register_bad_password(client):
    data = {
            'username': 'AUserName',
            'firstname': 'John',
            'surname': 'Doe',
            'email': 'email@email.com',
            'password': 'PaSw3',
            'repeatPassword': 'PaSw3',
            }
    url = reverse('register')

    response = client.post(url, data)

    messages = list(get_messages(response.wsgi_request))

    assert str(messages[0]) == "Password incorrect format, minimum 6 characters, 1 letter, 1 number and 1 special character"

    assert response.status_code == 302


def test_register_bad_username(client):
    data = {
            'username': '@@',
            'firstname': 'John',
            'surname': 'Doe',
            'email': 'email@email.com',
            'password': 'PaSsW0rD3!',
            'repeatPassword': 'PaSsW0rD3!',
            }
    url = reverse('register')

    response = client.post(url, data)

    messages = list(get_messages(response.wsgi_request))

    assert str(messages[0]) == "Username incorrect format, only letters, numbers and minimum 3 letters"

    assert response.status_code == 302


def test_register_bad_email(client):
    data = {
            'username': 'AUserName',
            'firstname': 'John',
            'surname': 'Doe',
            'email': 'emailemail.com',
            'password': 'PaSsW0rD3!',
            'repeatPassword': 'PaSsW0rD3!',
            }
    url = reverse('register')

    response = client.post(url, data)

    messages = list(get_messages(response.wsgi_request))

    assert str(messages[0]) == "Email incorrect format"

    assert response.status_code == 302


def test_register_name(client):
    data = {
            'username': '123',
            'firstname': '321',
            'surname': 'Doe',
            'email': 'emailemail.com',
            'password': 'PaSsW0rD3!',
            'repeatPassword': 'PaSsW0rD3!',
            }
    url = reverse('register')

    response = client.post(url, data)

    messages = list(get_messages(response.wsgi_request))

    assert str(messages[0]) == "Firstname or Surname is in the incorrect format, minimum 1 letters"

    assert response.status_code == 302


# Login tests
def test_login_with_real_user(client, django_user_model):
    username = "user1"
    password = "bar"
    django_user_model.objects.create_user(username=username, password=password)
    data = {
            'username': username,
            'password': password,
           }
    url = reverse('login')
    response = client.post(url, data)
    assert response.status_code == 302


def test_login_with_no_user(client):
    username = "user1"
    password = "bar"
    data = {
            'username': username,
            'password': password,
           }
    url = reverse('login')
    response = client.post(url, data)
    assert response.status_code == 200


class TestTeam():

    def test_admin_authenticated(user: User, admin_client):
        response = admin_client.get(reverse("team"))
        assert response.status_code == 200

    def test_not_admin_authenticated(user: User, client):
        response = client.get(reverse("team"))
        assert response.status_code == 302


class TestLogout(TestCase):

    def test_authenticated(self):
        self.client.login(username='username', password='password', is_superuser=True)
        response = self.client.get(reverse("logout"))
        assert response.status_code == 302

#The following tests also cover access_check.py
class TestAddAccess():
    def test_admin_add_access(user: User, admin_client):
        userChosen = UserFactory.create()
        product = ProductsFactory.create()
        response = admin_client.post(reverse('addaccess', kwargs={'userPK': userChosen.pk, 'productPK': product.pk}))
        assert response.status_code == 302
        assert access_check.checkAccess(product, UserAccess.objects.all())

    def test_admin_add_access_no_product(user: User, admin_client):
        userChosen = UserFactory.create()
        try:
            admin_client.post(reverse('addaccess', kwargs={'userPK': userChosen.pk, 'productPK': '280'}))
        except Exception as e:
            assert "didn't return an HttpResponse object" in str(e)

    def test_admin_add_access_no_user(user: User, admin_client):
        product = ProductsFactory.create()
        try:
            admin_client.post(reverse('addaccess', kwargs={'userPK': '1282', 'productPK': product.pk}))
        except Exception as e:
            assert "didn't return an HttpResponse object" in str(e)

    def test_not_admin_add_access(user: User, client):
        userChosen = UserFactory.create()
        product = ProductsFactory.create()
        try:
            client.get(reverse('addaccess', kwargs={'userPK': userChosen.pk, 'productPK': product.pk}))
        except Exception as e:
            assert "didn't return an HttpResponse object" in str(e)
