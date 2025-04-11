from sqlalchemy import select
from src.reposittories.base import BaseRepositories
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel


class HotelsRepositories(BaseRepositories):
    model = HotelsOrm
    schema = Hotel

    async def get_all(
            self,
            title,
            location,
            limit,
            offset
    ):
        query = select(HotelsOrm)
        if location:
            query = query.filter(HotelsOrm.location.icontains(location.strip()))
        if title:
            query = query.filter(HotelsOrm.title.icontains(title.strip()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]
