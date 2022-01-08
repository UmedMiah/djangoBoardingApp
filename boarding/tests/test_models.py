import pytest

from boarding.models import User

pytestmark = pytest.mark.django_db

# @pytest.mark.django_db
# def test_example(products_factory):
#     user_access = products_factory.build()
#     print(user_access.name)
#     assert True

# @pytest.mark.django_db
def test_models(access_factory):
    user_access = access_factory.build()
    print(user_access.user.username)
    assert user_access.user.username == 'John Doe' and user_access.product.name == 'product_name'