from django.contrib.auth.models import User
import factory
from faker import Faker
from boarding import models

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fake.name()

class ProductsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Products

    name = 'product_name'

class AccessFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.UserAccess

    user = factory.SubFactory(UserFactory)
    product = factory.SubFactory(ProductsFactory)
