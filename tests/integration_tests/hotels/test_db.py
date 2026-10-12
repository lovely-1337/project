from src.schemas.hotels import HotelADD


async def test_get_hotel(db):
    hotel_data = HotelADD(title="Test", location="Test")
    await db.hotels.add(hotel_data)
    await db.commit()
async def test_get_hotel2(db):
    hotel_data = HotelADD(title="Test2", location="Test")
    await db.hotels.add(hotel_data)
    await db.commit()