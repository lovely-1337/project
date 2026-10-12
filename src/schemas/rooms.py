from pydantic import BaseModel

from src.schemas.facilities import Facility


class RoomADDRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] = []


class RoomADD(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class Room(RoomADD):
    id: int

 


class RoomsWithRels(Room):
    facilities: list[Facility]

class RoomPATCHRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] = []

class RoomPATCH(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None