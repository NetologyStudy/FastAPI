from src.models.users import UsersOrm
from src.reposittories.base import BaseRepositories
from src.schemas.users import User


class UsersRepositories(BaseRepositories):
    model = UsersOrm
    schema = User
