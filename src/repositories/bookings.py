from datetime import date

from fastapi import HTTPException
from sqlalchemy import select

from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mapper.mappers import BookingDataMapper
from src.repositories.utils import rooms_id_for_bookings
from src.schemas.bookings import BookingADD


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_booking_with_today_checkin(self):
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from== date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add(self, data: BookingADD, hotel_id: int):
        free_rooms_query = rooms_id_for_bookings(
            date_to=data.date_to,
            date_from=data.date_from,
            hotel_id=hotel_id,
        )
        res = await self.session.execute(free_rooms_query)
        free_rooms_ids: list[int] = res.scalars().all()
        if data.room_id not in free_rooms_ids:
            raise HTTPException(status_code=409, detail="Нет свободных номеров на эти даты")
        return await super().add(data)
            

   