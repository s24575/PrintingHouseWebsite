import base64
import os

import requests
from flask.cli import load_dotenv
from pydantic import BaseModel, ValidationError


FURGONETKA_API_URL = "https://api.sandbox.furgonetka.pl/"


class AccessTokenResponse(BaseModel):
    token_type: str
    expires_in: int
    access_token: str
    refresh_token: str | None = None


class FurgonetkaService:
    def __init__(self, email: str, password: str, client_id: str, client_secret: str) -> None:
        self._email = email
        self._password = password
        self._client_id = client_id
        self._client_secret = client_secret

    def validate_address(self) -> dict | None:
        url = FURGONETKA_API_URL + "account/address-book/validate"

        address_example = {
            "name": "Jan Kowalski",
            # "company": "Nazwa firmy",
            "email": "mail@example.com",
            "street": "Targ Drzewny 9",
            "building_number": "11",
            # "flat_number": "11",
            "postcode": "80-894",
            "city": "Gdańsk",
            "country_code": "PL",
            # "county": "NY",
            # "nip": "1132567365",
            # "iban": "65103010872466704448246782",
            # "iban_name": "Jan Nowak",
            "phone": "567890567",
            # "point": "567890567",
            "service": "dpd",
            "default_pickup": True,
            "default_my_address": True,
            "default_sender": True,
            "is_public": True,
            # "uuid": "3abc8db0-8d8b-4f16-ac12-f69be9e01855"
        }

        access_token_response = self._get_access_token()
        headers = self._get_headers(f"Bearer {access_token_response.access_token}")

        try:
            response = requests.post(url, data=address_example, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except Exception as err:
            print(f"Other error occurred: {err}")
        return None

    def _get_access_token(self) -> AccessTokenResponse | None:
        url = FURGONETKA_API_URL + "oauth/token"

        data = {
            "grant_type": "password",
            "scope": "api",
            "username": self._email,
            "password": self._password,
        }

        auth = self._get_auth()
        auth = base64.b64encode(auth.encode()).decode()
        headers = self._get_headers("Basic " + auth)

        try:
            response = requests.post(url, data=data, headers=headers)
            response.raise_for_status()
            return AccessTokenResponse.model_validate(response.json())
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except ValidationError as e:
            print(f"Validation error: {e}")
        except Exception as err:
            print(f"Other error occurred: {err}")

    def _get_auth(self) -> str:
        return f"{self._client_id}:{self._client_secret}"

    @staticmethod
    def _get_headers(authorization: str, content_type: str = "application/x-www-form-urlencoded") -> dict[str, str]:
        return {"Authorization": authorization, "Content-Type": content_type}


if __name__ == "__main__":
    load_dotenv()
    email_ = os.environ.get("FURGONETKA_EMAIL")
    password_ = os.environ.get("FURGONETKA_PASSWORD")
    client_id_ = os.environ.get("FURGONETKA_CLIENT_ID")
    client_service_ = os.environ.get("FURGONETKA_CLIENT_SECRET")
    furgonetka_service = FurgonetkaService(email_, password_, client_id_, client_service_)
    furgonetka_service.validate_address()
