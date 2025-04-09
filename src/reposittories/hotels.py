from sqlalchemy import select
from src.reposittories.base import BaseRepositories
from src.models.hotels import HotelsOrm


class HotelsRepositories(BaseRepositories):
    model = HotelsOrm

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
        return result.scalars().all()
