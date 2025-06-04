from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Получение информации о всех бронированиях")
async def get_booking(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me", summary="Получение информации о бронированиях текущего пользователя")
async def get_my_booking(
        db: DBDep,
        user_id: UserIdDep
):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("", summary="Добавление данных о новом бронировании")
async def post_booking(
        db: DBDep,
        user_id: int,
        booking_data: BookingAddRequest = Body()
):
    room = await db.rooms.get_one_or_one(id=booking_data.room_id)
    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {"status": "OK", "data": booking}
