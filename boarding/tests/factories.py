import factory
# from typing import Any, Sequence
from faker import Faker
from django.contrib.auth.models import User
from boarding import models
# from factory import Faker, post_generation
# from factory.django import DjangoModelFactory

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = 'John Doe'
    # email = fake.email()
    # # name = Faker("name")

    # @post_generation
    # def password(self, create: bool, extracted: Sequence[Any], **kwargs):
    #     password = (
    #         extracted
    #         if extracted
    #         else Faker(
    #             "password",
    #             length=42,
    #             special_chars=True,
    #             digits=True,
    #             upper_case=True,
    #             lower_case=True,
    #         ).evaluate(None, None, extra={"locale": None})
    #     )
    #     self.set_password(password)

class ProductsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Products

    name = 'product_name'

class AccessFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.UserAccess

    user = factory.SubFactory(UserFactory)
    product = factory.SubFactory(ProductsFactory)
