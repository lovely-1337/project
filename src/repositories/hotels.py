from datetime import date

from sqlalchemy import func, select

from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mapper.mappers import HotelDataMapper
from src.repositories.utils import rooms_id_for_bookings
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
        model = HotelsOrm
        mapper = HotelDataMapper
        async def get_all(
                       self,
                       location,
                       title,
                       limit,
                       offset) -> list[Hotel]:
                       query = (select(HotelsOrm))
                       if location:
                               query = query.filter(func.lower(HotelsOrm.location).contains(location.lower()))
                       if title:
                               query = query.filter(func.lower(HotelsOrm.title).contains(title))
                       query =  (
                               query
                               .limit(limit)
                               .offset(offset))
                       
                               
                       result = await self.session.execute(query)
                       
                       
                       return [Hotel.model_validate(hotel) for hotel in result.scalars().all()]

        async def get_filtered_by_time(
                        self,
                        date_from: date,
                        date_to: date,
                        location: str,
                        title: str,
                        limit: int,
                        offset: int,
                        )  -> list[Hotel]:
                rooms_ids_to_get = rooms_id_for_bookings( date_to=date_to, date_from=date_from)
                hotels_ids_to_get = (
                                        select(RoomsOrm.hotel_id)
                                        .select_from(RoomsOrm)
                                        .filter(RoomsOrm.id.in_(rooms_ids_to_get))
                                        )

                
                query = (select(HotelsOrm)).filter(HotelsOrm.id.in_(hotels_ids_to_get))
                        
                if location:
                        query = query.filter(func.lower(HotelsOrm.location).contains(location.lower()))
                if title:
                        query = query.filter(func.lower(HotelsOrm.title).contains(title))
                query =  (
                        query
                        .limit(limit)
                        .offset(offset))
                                       
                                               
                result = await self.session.execute(query)
                                       
                                       
                return [self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()]
           


        
                