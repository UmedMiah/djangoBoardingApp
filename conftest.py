import pytest

from pytest_factoryboy import register
from boarding.tests.factories import UserFactory, ProductsFactory, AccessFactory
from config.settings import base

register(UserFactory)
register(ProductsFactory)
register(AccessFactory)


@pytest.fixture(scope='session')
def django_db_setup():
    base.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'db.example.com',
        'NAME': 'external_db',
    }

# @pytest.fixture(autouse=True)
# def media_storage(settings, tmpdir):
#     settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def new_user(db, user_factory):
    user = user_factory.create()
    return user
