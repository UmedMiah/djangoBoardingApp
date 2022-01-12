import pytest
from boarding.models import UserAccess
from boarding.templatetags import access_check

from boarding.tests.factories import AccessFactory, ProductsFactory


pytestmark = pytest.mark.django_db

#This tests the access_check functions
def test_access_check():
    user_access = AccessFactory.create()
    assert access_check.checkAccess(user_access.product, UserAccess.objects.all())


def test_access_check_bad():
    product = ProductsFactory.create()
    assert not access_check.checkAccess(product, UserAccess.objects.all())


def test_printAccess_check():
    user_access = AccessFactory.create()
    assert access_check.printAccess(user_access.product, UserAccess.objects.all()) == "Has Access"


def test_printAccess_check_bad():
    product = ProductsFactory.create()
    assert access_check.printAccess(product, UserAccess.objects.all()) == "No Access"


def test_printAddRemove_check():
    user_access = AccessFactory.create()
    assert access_check.printAddRemove(user_access.product, UserAccess.objects.all()) == "Delete"


def test_printAddRemove_check_bad():
    product = ProductsFactory.create()
    assert access_check.printAddRemove(product, UserAccess.objects.all()) == "Add"
