from src.reposittories.base import BaseRepositories
from src.models.hotels import HotelsOrm


class HotelsRepositories(BaseRepositories):
    model = HotelsOrm
