import factory
import factory.fuzzy

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
