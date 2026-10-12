from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityADD
from src.tasks.tasks import test_task

router = APIRouter(prefix="/hotels/facilities", tags=["Удобства"])



@router.get("")
@cache(expire=10)
async def get_facilities(
        
        db: DBDep,
        
        
):
    print("GO TO DB")
    return await db.facilities.get_all()
   


@router.post("")
async def create_facility(
   
    db: DBDep,
    facility_data: FacilityADD = Body()
      
):
    
    
    facility = await db.facilities.add(facility_data)
    await db.commit()

    test_task.delay()
   
    return {"status": "OK", "data": facility}




# @router.put("/{hotel_id}/{room_id}/facilities/{facility_id}")
# async def edit_facility(db: DBDep, hotel_id: int, room_id: int, facility_id: int, facility_data: FacilityADD):
    
#     await db.facilities.edit(facility_data, id = facility_id)
#     await db.commit()
#     return {"Status": "OK"}


# @router.patch(
#     "/{hotel_id}/{room_id}/facilities/{facility_id}"
# )
# async def partially_edit_facility(
#      db: DBDep,
#     hotel_id: int,
#     room_id: int,
#     facility_id: int,
#     facility_data: FacilityPATCH,
# ):
        
#         await db.facilities.edit(facility_data, exclude_unset= True, id = facility_id)
#         await db.commit()
#         return {"Status:" "OK"}


# @router.delete("/{hotel_id}/{room_id}/facilities/{facility_id}")
# async def delete_facility(db: DBDep, hotel_id: int, room_id: int, facility_id: int):
    
#     await db.facilities.delete(id = facility_id)
#     await db.commit()
#     return {"status": "OK"}