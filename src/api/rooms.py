from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomADD, RoomADDRequest, RoomPATCH, RoomPATCHRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, db: DBDep,
    date_from: date = Query(example="2026-10-01", description="Дата заезда в отель"),
    date_to: date = Query(example="2026-10-01", description="Дата выезда из отеля")
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none_wiht_rels(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomADDRequest = Body()):
    _room_data = RoomADD(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomADDRequest,
        db: DBDep,
):
    _room_data = RoomADD(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPATCHRequest,
        db: DBDep,
):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPATCH(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=_room_data_dict["facilities_ids"])

    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}