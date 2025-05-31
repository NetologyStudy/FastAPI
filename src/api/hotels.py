from fastapi import Query, APIRouter, Body, Path

from src.schemas.hotels import HotelPATCH, HotelAdd
from src.api.dependencies import PaginationDep, DBDep

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получение данных об отелях", description="<h1>Получаем полный список всех отелей</h1>")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Место локации"),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.get("/{hotel_id}",
            summary="Получение данных одного отеля",
            description="<h1>Получение данных одного отеля по его id<h1>")
async def get_hotel(
        db: DBDep,
        hotel_id: int = Path(description="Уникальный идентификатор отеля", ge=1)
):
    return await db.hotels.get_one_or_one(id=hotel_id)


@router.post("", summary="Добавление данных нового отеля")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(openapi_examples={
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
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Полное обновление данных об отеле")
async def edit_hotel(
        db: DBDep,
        hotel_id: int, hotel_data: HotelAdd
):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичное обновление данных об отеле")
async def partially_edit_hotel(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelPATCH
):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}",
               summary="Удаление данных отеля",
               description="<h1>Полное удаление отеля по его id<h1>")
async def delete_hotel(
        db: DBDep,
        hotel_id: int
):
    await db.hotels.delete(id=hotel_id)
    await db.commit()

    return {"status": "OK"}