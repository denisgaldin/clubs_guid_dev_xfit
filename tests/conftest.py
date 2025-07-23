import pytest
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
PHONE_NUMBER = os.getenv("PHONE_NUMBER", "9000008851")
SMS_CODE = os.getenv("SMS_CODE", "1234")

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "PostmanRuntime/7.44.1",
    "Platform": "IOS",
    "App-Version": "4.5.0",
    "Accept": "*/*",
    "Cache-Control": "no-cache"
}


@pytest.fixture(scope="session")
def sms_token():
    payload = {
        "phone": {
            "countryCode": "7",
            "number": PHONE_NUMBER
        }
    }
    response = requests.post(
        f"{BASE_URL}/authorization/sendVerificationCode",
        headers=HEADERS,
        json=payload
    )

    if response.status_code == 200:
        token = response.json()["result"]["token"]
        print(f"✅ Новый SMS token получен: {token}")
        time.sleep(3)
        return {"token": token, "code": SMS_CODE}
    elif response.status_code == 403 and "VERIFICATION_CODE_ALREADY_SEND_PORTAL" in response.text:
        token = os.getenv("SMS_TOKEN")
        if not token:
            pytest.fail("SMS_TOKEN не задан в .env при уже отправленном коде")
        print("⚠️ Используется токен из .env (код уже был отправлен)")
        return {"token": token, "code": SMS_CODE}
    else:
        pytest.fail(f"❌ Ошибка при получении SMS токена: {response.status_code} {response.text}")


@pytest.fixture(scope="session")
def access_token(sms_token):
    payload = {
        "token": sms_token["token"],
        "verificationCode": sms_token["code"]
    }
    response = requests.post(
        f"{BASE_URL}/authorization/basic",
        headers=HEADERS,
        json=payload
    )

    if response.status_code == 403 and "VERIFICATION_CODE_EXPIRED" in response.text:
        pytest.fail("❌ Код подтверждения истёк. Обнови его вручную или удали SMS_TOKEN из .env и перезапусти тесты.")

    if response.status_code != 200:
        pytest.fail(f"❌ Ошибка авторизации: {response.status_code} {response.text}")

    access_token = response.json().get("result", {}).get("access", {}).get("token")
    if not access_token:
        pytest.fail("❌ Access token отсутствует в ответе")

    print(f"✅ Access token получен: {access_token[:10]}...")
    return access_token
