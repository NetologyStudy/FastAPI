from fastapi import Query, APIRouter, Body, HTTPException
from sqlalchemy import insert, select

from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.reposittories.hotels import HotelsRepositories
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получение данных об отелях", description="<h1>Получаем полный список всех отелей</h1>")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Место локации"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepositories(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )



@router.post("", summary="Добавление данных нового отеля")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": {
            "title": "Отель Rich 5 звезд у моря",
            "location": "Сочи, ул. Моря 1",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель Deluxe у фонтана",
            "location": "Дубай, ул. Шейха 2",
        }
    }
})
):
    async with async_session_maker() as session:
        hotel = await HotelsRepositories(session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel}


@router.delete("/{hotel_id}", summary="Удаление данных отеля")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepositories(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}




@router.put("/{hotel_id}", summary="Полное обновление данных об отеле")
async def edit_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepositories(session).edit(hotel_data, id=hotel_id)
        await session.commit()


@router.patch("/{hotel_id}", summary="Частичное обновление данных об отеле")
def partially_edit_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    hotel = [hotel for hotel in hotels if hotel['id'] == hotel_id][0]
    if hotel_data.name is None:
        hotel["title"] = hotel_data.title
    if hotel_data.title is None:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}