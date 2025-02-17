import requests
from io import BytesIO
from PIL import Image
from map import calculate_spn

SEARCH_API_KEY = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
STATIC_MAPS_API_KEY = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

address_ll = "37.588392,55.734036"

search_params = {
    "apikey": SEARCH_API_KEY,
    "text": "Бутово Молл",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}


response = requests.get("https://search-maps.yandex.ru/v1/", params=search_params)

if not response:
    print("Не удалось выполнить запрос")
    exit()

json_response = response.json()

if not json_response.get("features"):
    print("Не найдено ни одной организации")
    exit()

organization = json_response["features"][0]

org_name = organization["properties"]["CompanyMetaData"]["name"]
org_address = organization["properties"]["CompanyMetaData"]["address"]
point = organization["geometry"]["coordinates"]
org_point = f"{point[0]},{point[1]}"

bounding_box = organization["properties"].get("boundedBy")
spn = calculate_spn(bounding_box)

map_params = {
    "ll": org_point,
    "spn": spn,
    "apikey": STATIC_MAPS_API_KEY,
    "pt": f"{org_point},pm2dgl~{address_ll},pm2rdl"
}

map_response = requests.get("https://static-maps.yandex.ru/v1", params=map_params)

im = BytesIO(map_response.content)
opened_image = Image.open(im)
opened_image.show()

print(f"Найденная организация:")
print(f"Название: {org_name}")
print(f"Адрес: {org_address}")
print(f"Координаты: {org_point}")
print(f"Масштаб карты (spn): {spn}")
