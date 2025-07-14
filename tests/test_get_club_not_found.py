import pytest
import requests
import os
import json

BASE_URL = os.getenv("BASE_URL")

COMMON_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "PostmanRuntime/7.44.1",
    "Platform": "IOS",
    "App-Version": "4.5.0",
    "Accept": "*/*",
    "Cache-Control": "no-cache",
}


@pytest.fixture
def invalid_club_guid():
    return "00000000-0000-0000-0000-000000000000"


@pytest.fixture
def location_params():
    return {
        "lat": "55.754202886759",
        "lon": "37.815222611779"
    }


@pytest.fixture
def not_found_response(access_token, invalid_club_guid, location_params):
    headers = COMMON_HEADERS.copy()
    headers["token"] = access_token

    url = f"{BASE_URL}/clubs/{invalid_club_guid}"
    response = requests.get(url, headers=headers, params=location_params)

    print("Ответ сервера:", response.status_code)
    print("Тело ответа:", json.dumps(response.json(), indent=2, ensure_ascii=False))

    return response


def test_get_club_details_not_found(not_found_response):
    response = not_found_response

    assert response.status_code == 404, f"Expected 404, got {response.status_code}\n{response.text}"

    data = response.json()

    assert "error" in data, "В ответе нет поля 'error'"
    assert data["error"]["type"] == "CLUB_NOT_FOUND", f"Ожидался тип 'CLUB_NOT_FOUND', а пришёл {data['error']['type']}"
    assert data["error"][
               "message"] == "Клуб не найден.", f"Ожидалось сообщение 'Клуб не найден.', а пришло {data['error']['message']}"
