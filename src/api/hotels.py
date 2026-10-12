from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, PaginationDep
from src.schemas.hotels import HotelADD, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])



@router.get("")
@cache(expire=20)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="Локация"),
        title: str | None = Query(None, description="Название отеля"),
        date_from:date = Query(None, description="Дата заезда"),
        date_to: date = Query(None, description="Дата выезда")
):
    
    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )
   


@router.post("")
async def create_hotel(db: DBDep,
    hotel_data: HotelADD = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Сочи 5 звезд у моря",
                    "location": "ул. Моря, 1",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель Дубай У фонтана",
                    "location": "ул. Шейха, 2",
                },
            },
        }
    )
):
    
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
        

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelADD):
    
    await db.hotels.edit(hotel_data, id = hotel_id)
    await db.commit()
    return {"Status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить location, а можно title</h1>",
)
async def partially_edit_hotel(
     db: DBDep,
    hotel_id: int,
    hotel_data: HotelPATCH,
):
        
        await db.hotels.edit(hotel_data, exclude_unset= True, id = hotel_id)
        await db.commit()
        return {"Status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    
    await db.hotels.delete(id = hotel_id)
    await db.commit()
    return {"status": "OK"}