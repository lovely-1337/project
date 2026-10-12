import pytest


@pytest.mark.parametrize("email, password, status_code",[
    ("k0t@pes.com", "1234", 200),
    ("k0t@pes.com", "1234", 400),
    ("k0t1@pes.com", "1235", 200),
    ("k0t1", "1235", 422)
])
async def test_auth_flow(fresh_ac, email: str, password: str, status_code: int):
    resp_register = await fresh_ac.post(
            "/auth/register",
            json={
                "email": email,
                "password": password
            }
        )
    assert resp_register.status_code == status_code
    if status_code != 200:
        return




    resp_login = await fresh_ac.post(
            "/auth/login",
            json={
                            "email": email,
                            "password": password
                        }
                    )
    assert resp_login.status_code == 200
    assert fresh_ac.cookies["access_token"]
    assert "access_token" in resp_login.json()

    resp_me = await fresh_ac.get("/auth/me")
    assert resp_me.status_code == 200
    user = resp_me.json()
    assert user["email"] == email
    assert "id" in user
    assert "password" not in user
    assert "hashed_password" not in user

    resp_logout = await fresh_ac.post("/auth/logout")
    assert resp_logout.status_code == 200
    assert "acces_token" not in fresh_ac.cookies
   