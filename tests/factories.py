import string

import factory
import factory.fuzzy

from orderful.models.associations import CategoryProductAssociation
from orderful.models.categories import Category
from orderful.models.products import Product
from orderful.models.users import User
from orderful.services.users import UserService
from tests.constants import TEST_PASSWORD


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    name = factory.Faker("name")
    email = factory.Faker("email")
    password = factory.LazyFunction(lambda: UserService.get_password_hash(TEST_PASSWORD))
    superuser = False
    active = False

    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"


class CategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    name = factory.Faker("name")
    parent = None

    class Meta:
        model = Category
        sqlalchemy_session_persistence = "commit"


class ProductFactory(factory.alchemy.SQLAlchemyModelFactory):
    name = factory.Faker("name")
    price = factory.fuzzy.FuzzyDecimal(0.01, 9999.99, 2)
    article = factory.fuzzy.FuzzyText(length=10, chars=string.ascii_lowercase)
    quantity = factory.fuzzy.FuzzyInteger(5, 20)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Product
        sqlalchemy_session_persistence = "commit"


class CategoryProductAssociationFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = CategoryProductAssociation
        sqlalchemy_session_persistence = "commit"
