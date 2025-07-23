import pytest
import os

BASE_URL = os.getenv("BASE_URL")


def test_authorization_by_sms(access_token):
    assert access_token is not None and access_token != "", "Access token пустой или не получен"
    print("✅ Access token успешно получен и валиден:", access_token[:10], "...")
