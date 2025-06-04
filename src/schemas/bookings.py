from datetime import date, datetime, timezone

from pydantic import BaseModel, Field


class BookingAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingAdd(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int
    created_add: datetime = Field(datetime.now(timezone.utc).replace(tzinfo=None))


class Booking(BookingAdd):
    id: int
