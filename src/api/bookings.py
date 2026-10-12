from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingADD, BookingADDRequest

router = APIRouter(prefix="/bookings", tags=["Бронирования"])




@router.get("")
async def get_bookings(
        db: DBDep,
        
):

    return await db.bookings.get_all()

@router.get("/me")
async def get_bookings_me(
        user_id: UserIdDep,
        db: DBDep,
        
):

    return await db.bookings.get_filtered(user_id=user_id)

@router.post("")
async def add_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingADDRequest,
):

    
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    
    if room is None:
        raise HTTPException(status_code=404, detail="Номер не найден")
    room_price: int = room.price
    _booking_data = BookingADD(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )
    booking = await db.bookings.add(_booking_data, hotel_id=room.hotel_id)
    await db.commit()
    return {"status": "OK", "data": booking}
