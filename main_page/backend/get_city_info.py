from requests import get
from decouple import config


api_key = config('api_key')
url = config('url')


def get_weather(city):
    """Получает информацию о погоде в городе"""
    response = get(url,
                   params={'q': city,
                           'APPID': api_key,
                           'units': 'metric',
                           'lang': 'ru',
                           })
    return response.json()


def create_cities_dict(cities):
    """Создает полный словарь всех город из базы со всей необходимой информацией,
    а также проверяет существует ли введеный город"""
    all_cities = []

    for city in cities:
        response = get_weather(city.name)

        if response.get('message', 'OK') != 'OK':
            city_info = {
                'city': f'Город "{city.name}" не найден',
                'temp': None,
                'icon': None
            }
        else:
            city_info = {
                'city': response['name'],
                'temp': response['main']['temp'],
                'icon': response['weather'][0]['icon']
            }

        all_cities.append(city_info)

    return all_cities
