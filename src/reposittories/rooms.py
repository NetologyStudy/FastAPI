from sqlalchemy import select

from src.reposittories.base import BaseRepositories
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room


class RoomsRepositories(BaseRepositories):
    model = RoomsOrm
    schema = Room

    async def get_all(
            self,
            hotel_id,
            title,
            price,

    ):
        query = select(RoomsOrm).where(RoomsOrm.hotel_id == hotel_id)
        if title:
            query = query.filter(RoomsOrm.title.icontains(title.strip()))
        if price:
            query = query.filter(RoomsOrm.price == price)
        result = await self.session.execute(query)
        return [Room.model_validate(room, from_attributes=True) for room in result.scalars().all()]
