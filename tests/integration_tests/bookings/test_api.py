import pytest

from tests.conftest import get_db_null_pool


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2026-10-01", "2026-10-10", 200),
    (1, "2026-10-02", "2026-10-11", 200),
    (1, "2026-10-03", "2026-10-12", 200),
    (1, "2026-10-04", "2026-10-13", 200),
    (1, "2026-10-05", "2026-10-14", 200),
    (1, "2026-10-06", "2026-10-15", 409),
    (1, "2026-10-17", "2026-10-25", 200),
])
async def test_add_booking(
    room_id, date_from, date_to, status_code,
    db, authenticated_ac):
    # room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings", 
        json = {
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res

@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()
@pytest.mark.parametrize("room_id, date_from, date_to, booked_rooms", [
    (1, "2026-10-01", "2026-10-10", 1),
    (1, "2026-10-02", "2026-10-11", 2),
    (1, "2026-10-03", "2026-10-12", 3),
    ]
    )
async def test_add_and_get_my_bookings(
    room_id, date_from, date_to,booked_rooms,
     authenticated_ac, delete_all_bookings):
    response = await authenticated_ac.post(
            "/bookings", 
            json = {
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to,
            }
        )
    assert response.status_code == 200

    response_my_bookings = await authenticated_ac.get("/bookings/me")  

    assert len(response_my_bookings.json()) == booked_rooms