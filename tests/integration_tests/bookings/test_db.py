from datetime import date

from sqlalchemy import delete

from src.models.bookings import BookingsOrm
from src.schemas.bookings import BookingADD


async def test_booking_crud(db):
    await db.session.execute(delete(BookingsOrm))
    await db.commit()
    user_id = (await db.users.get_all())[0].id
    room = (await db.rooms.get_all())[0]
    booking_data = BookingADD(
            user_id=user_id,
            room_id=room.id,
            date_from=date(year=2026, month=10, day=1),
            date_to=date(year=2026, month=10, day=10),
            price=100,
    )
    new_booking = await db.bookings.add(booking_data, hotel_id=room.hotel_id)

    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.room_id == new_booking.room_id
    assert booking.user_id == new_booking.user_id
    booking_update_data = BookingADD(
            user_id=user_id,
            room_id=room.id,
            date_from=date(year=2026, month=10, day=1),
            date_to=date(year=2026, month=10, day=10),
            price=1000,
        )
    await db.bookings.edit(booking_update_data, id=new_booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.price == 1000
    await db.bookings.delete(id=booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not booking

