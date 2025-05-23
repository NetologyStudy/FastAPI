from fastapi import APIRouter, Query, Path, Body

from src.database import async_session_maker
from src.reposittories.rooms import RoomsRepositories
from src.schemas.rooms import RoomPATCH, RoomAdd


router = APIRouter(prefix="/hotel", tags=["Номера"])


@router.get("/{hotel_id}/rooms",
            summary="Получение данных о номерах",
            description="<h1>Получение номеров конкретного отеля<h1>")
async def get_rooms(
        hotel_id: int = Path(description="Уникальный идентификатор отеля", ge=1),
        title: str | None = Query(None, description="Категория/Тип номера"),
        price: int | None = Query(None, description="Цена номера"),
):

    async with async_session_maker() as session:
        return await RoomsRepositories(session).get_all(
            hotel_id=hotel_id,
            title=title,
            price=price,
        )


@router.get("/{hotel_id}/rooms/{room_id}",
            summary="Получение данных одного номера",
            description="<h1>Получение данных одного номера отеля по его id<h1>"
            )
async def get_hotel(hotel_id: int = Path(description="Уникальный идентификатор отеля", ge=1),
                    room_id: int = Path(description="Уникальный идентификатор отеля", ge=1)):
    async with async_session_maker() as session:
        return await RoomsRepositories(session).get_one_or_one(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}", summary="Добавление новых номеров")
async def add_room(room_data: RoomAdd = Body()):
    async with async_session_maker() as session:
        room = await RoomsRepositories(session).add(room_data)
        await session.commit()
    return {"status": "OK", "data": room}


# @router.put("")


