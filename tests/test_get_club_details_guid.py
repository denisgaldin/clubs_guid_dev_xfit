import pytest
import requests
import json
import os
import time

BASE_URL = os.getenv("BASE_URL")

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "PostmanRuntime/7.44.1",
    "Platform": "IOS",
    "App-Version": "4.5.0",
    "Accept": "*/*",
    "Cache-Control": "no-cache",
}

CLUB_GUID = "4dba0c90-fd63-40a1-b66c-5cc540d20a25"


def test_get_club_details_by_guid(access_token):
    time.sleep(5)

    headers = HEADERS.copy()
    headers["token"] = access_token

    params = {
        "lat": "55.754202886759",
        "lon": "37.815222611779"
    }

    url = f"{BASE_URL}/clubs/{CLUB_GUID}"
    response = requests.get(url, headers=headers, params=params)

    print("Ответ сервера:", response.status_code)
    print("Тело ответа:", json.dumps(response.json(), indent=2, ensure_ascii=False))

    assert response.status_code == 200, f"Expected 200, got {response.status_code}\n{response.text}"

    data = response.json()

    assert "result" in data, "В ответе нет поля 'result'"
    assert "clubDetails" in data["result"], "В ответе нет поля 'clubDetails'"
    assert "title" in data["result"]["clubDetails"], "В ответе нет поля 'title' внутри clubDetails"
