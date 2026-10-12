
from fastapi import APIRouter, Body, Query

from api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Hotels"])

hotels = [
    {"id": 1, "title": "Tel-Aviv", "name": "tel-aviv"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
    {"id": 3, "title": "Monako", "name": "monako"},
    {"id": 4, "title": "London", "name": "london"},
    {"id": 5, "title": "Tbilisi", "name": "tbilisi"},
    {"id": 6, "title": "Singapour", "name": "singapour"},
    {"id": 7, "title": "Panama", "name": "panama"},
]
    




@router.get("")
def get_hotels(
    pagination: PaginationDep,
    id : int | None = Query(None, description="Айдишник"),
    title: str | None = Query(None, description="Название"),
):
    hotels_=[]
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
          continue
        hotels_.append(hotel)
    if pagination.page and pagination.per_page:
        return hotels_[pagination.per_page * (pagination.page-1):][:pagination.per_page]
    return hotels_


@router.post("")
def create_hotel(
    hotel_data: Hotel=Body(openapi_examples={"1": {"summary": "Tel-Aviv", "value":{
        "title": "BigHotel", "name":"Mossad", 
    }}})):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"]+1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
    return {"Status": "OK"}

@router.put("")
def put_hotel(
    hotel_id: int,
    hotel_data: Hotel,
    ):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            return {"Status": "OK"}
    return {"Status": "OK"}

@router.patch("")
def patch_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH
):
    for hotel in hotels:
        if hotel["id"] == hotel_id:

            if hotel_data.title is not None:
                hotel["title"] = hotel_data.title

            if hotel_data.name is not None:
                hotel["name"] = hotel_data.name

            return {"Status": "OK"}

    return {"Status": "Hotel not found"}
    
    

@router.delete("/{hotel_id}")
def delete_hotel( hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotels["id"] != hotel_id]
    return {"Status": "OK"}
