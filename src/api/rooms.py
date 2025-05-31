from fastapi import APIRouter, Path, Body

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(prefix="/hotel/{hotel_id}", tags=["Номера"])


@router.get("/rooms",
            summary="Получение данных о номерах",
            description="<h1>Получение номеров конкретного отеля<h1>")
async def get_rooms(
        db: DBDep,
        hotel_id: int
):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get("/rooms/{room_id}",
            summary="Получение данных одного номера",
            description="<h1>Получение данных одного номера отеля по его id<h1>"
            )
async def get_hotel(
        db: DBDep,
        hotel_id: int = Path(description="Уникальный идентификатор отеля", ge=1),
        room_id: int = Path(description="Уникальный идентификатор номера", ge=1)
):
    return await db.rooms.get_one_or_one(id=room_id, hotel_id=hotel_id)


@router.post("/rooms", summary="Добавление нового номера")
async def add_room(
        db: DBDep,
        hotel_id: int, room_data: RoomAddRequest = Body()
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.put("/rooms/{room_id}",
            summary="Изменение данных одного номера",
            description="<h1>Полностью меняем все данные номера по его id<h1>"
            )
async def edit_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/rooms/{room_id}",
              summary="Частичное изменение данных одного номера")
async def partially_edit_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/rooms/{room_id}",
               summary="Удаление данных о номер",
               description="<h1>Полное удаление данных номера по его id<h1>")
async def delete_room(
        db: DBDep,
        hotel_id: int,
        room_id: int
):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}
