from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mapper.mappers import RoomDataMapper, RoomDataWithRelsMapper
from src.repositories.utils import rooms_id_for_bookings


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date,
    ):
        rooms_ids_to_get = rooms_id_for_bookings(date_to, date_from, hotel_id)
        
       ## print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))



        query = (
        select(self.model)
        .options(joinedload(self.model.facilities))
        .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        
        result = await self.session.execute(query)
        return [RoomDataWithRelsMapper.map_to_domain_entity(model) for model in result.unique().scalars().all()]

    async def get_one_or_none_wiht_rels(
            self,
            hotel_id,
            id,
    ):
        query = select(self.model).options(joinedload(self.model.facilities)).filter_by(id=id, hotel_id=hotel_id)
        result = await self.session.execute(query)
        model = result.unique().scalars().one_or_none()
        if model is None:
                return None
        return RoomDataWithRelsMapper.map_to_domain_entity(model, from_attributes=True)