from sqlalchemy import select

from src.reposittories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking
