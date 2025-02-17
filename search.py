import sys
from io import BytesIO
import requests
from PIL import Image
from map import get_spn

YANDEX_GEOCODER_API_KEY = "8013b162-6b42-4997-9691-77b7074026e0"
YANDEX_MAPS_API_KEY = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"


def get_toponym(query):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": YANDEX_GEOCODER_API_KEY,
        "geocode": query,
        "format": "json"
    }
    response = requests.get(geocoder_api_server, params=params)

    if not response:
        raise Exception("Ошибка запроса к геокодеру")

    json_response = response.json()
    try:
        return json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    except IndexError:
        raise Exception("Адрес не найден")


def get_map(toponym):
    toponym_coordinates = toponym["Point"]["pos"]
    longitude, latitude = toponym_coordinates.split(" ")

    dx, dy = get_spn(toponym)

    map_params = {
        "ll": f"{longitude},{latitude}",
        "spn": f"{dx},{dy}",
        "l": "map",
        "pt": f"{longitude},{latitude},pm2rdl"
    }

    map_api_server = "https://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    if not response:
        raise Exception("Ошибка запроса к Static Maps API")

    return response.content


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python search.py <адрес>")
        sys.exit(1)

    toponym_to_find = " ".join(sys.argv[1:])

    try:
        toponym = get_toponym(toponym_to_find)
        image_data = get_map(toponym)

        im = Image.open(BytesIO(image_data))
        im.show()
    except Exception as e:
        print("Ошибка:", e)
