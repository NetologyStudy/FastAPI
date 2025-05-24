from fastapi import APIRouter, Query, Path, Body

from src.database import async_session_maker
from src.reposittories.rooms import RoomsRepositories
from src.schemas.rooms import RoomPATCH, RoomAdd, RoomPUT


router = APIRouter(prefix="/hotel/{hotel_id}", tags=["Номера"])


@router.get("/rooms",
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


@router.get("/rooms/{room_id}",
            summary="Получение данных одного номера",
            description="<h1>Получение данных одного номера отеля по его id<h1>"
            )
async def get_hotel(hotel_id: int = Path(description="Уникальный идентификатор отеля", ge=1),
                    room_id: int = Path(description="Уникальный идентификатор отеля", ge=1)):
    async with async_session_maker() as session:
        return await RoomsRepositories(session).get_one_or_one(id=room_id, hotel_id=hotel_id)


@router.post("/rooms", summary="Добавление нового номера")
async def add_room(room_data: RoomAdd = Body()):
    async with async_session_maker() as session:
        room = await RoomsRepositories(session).add(room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.delete("/rooms/{room_id}",
               summary="Удаление данных о номер",
               description="<h1>Полное удаление данных номера по его id<h1>")
async def delete_room(room_id: int):
    async with async_session_maker() as session:
        await RoomsRepositories(session).delete(id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.put("/rooms/{room_id}",
            summary="Изменение данных одного номера",
            description="<h1>Полностью меняем все данные номера по его id<h1>"
            )
async def edit_room(room_id: int, room_data: RoomPUT):
    async with async_session_maker() as session:
        await RoomsRepositories(session).edit(room_data, exclude_unset=True, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/rooms/{room_id}",
              summary="Частичное изменение данных одного номера")
async def partially_edit_room(room_id: int, room_data: RoomPATCH):
    async with async_session_maker() as session:
        await RoomsRepositories(session).edit(room_data, exclude_unset=True, id=room_id)
        await session.commit()
    return {"status": "OK"}




