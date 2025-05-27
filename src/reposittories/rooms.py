from sqlalchemy import select

from src.reposittories.base import BaseRepositories
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room


class RoomsRepositories(BaseRepositories):
    model = RoomsOrm
    schema = Room
