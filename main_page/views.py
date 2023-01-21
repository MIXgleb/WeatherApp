from requests import get as reqget
from django.shortcuts import render
from .models import City
# from .forms import CityForm


api_key = '4a81f5c7a6a48ba49162ead9a62faf4b'
url = 'http://api.openweathermap.org/data/2.5/weather'
single_city_mode_bul = False
default_city_mode_bul = False
default_city = 'Бишкек'


"""Добавляет город в базу"""
def create_city(input_city):
    city = City(name=input_city)
    city.save()


'''Проверяет, если ли введеный пользователем город в базе
и в зависимости от проверки добавляет его в базу'''
def add_city(input_city):
    city = rename_input_city(input_city)

    if not City.objects.filter(name=city).exists():
        create_city(city)


"""Добавляет город по умолчанию в начало списка"""
def add_default_city():
    if City.objects.filter(id=1).exists():
        return
    if City.objects.filter(name=default_city).exists():
        City.objects.get(name=default_city).delete()
    new_city = City(id=1, name=default_city)
    new_city.save()


'''Переводит название города на русский язык с помощью API запроса'''
def rename_input_city(city):
    new_city_name = reqget(url,
                           params={'q': city,
                                   'APPID': api_key,
                                   'lang': 'ru',
                                   }).json()

    if new_city_name.get('message', 'OK') != 'OK':
        return city.capitalize()
    return new_city_name['name']


'''Создает полный словарь всех город из базы со всей необходимой информацией, 
а также проверяет существует ли введеный город'''
def create_cities_dict(cities):
    all_cities = []

    for city in cities:
        response = reqget(url,
                          params={'q': city.name,
                                  'APPID': api_key,
                                  'units': 'metric',
                                  'lang': 'ru',
                                  }).json()

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


'''Полностью очищает базу'''
def clear_all(cities):
    cities.delete()

    if default_city_mode_bul:
        create_city(default_city)


'''Переключает режим показа одного города'''
def single_city_mode(cities):
    global single_city_mode_bul
    single_city_mode_bul = not single_city_mode_bul
    length = len(cities)
    last_city = cities.last()
    clear_all(cities)

    if not default_city_mode_bul and length != 0:
        create_city(last_city)


'''Создает словарь для дизайна кнопки режима показа одного города'''
def check_single_mode():
    message = 'Показывать только один город'

    if single_city_mode_bul:
        return {'mode': 'Выкл',
                'class': 'btn btn-danger',
                'message': message}
    return {'mode': 'Вкл',
            'class': 'btn btn-success',
            'message': message}


'''Переключает режим показа города по умолчанию'''
def default_city_mode():
    global default_city_mode_bul
    default_city_mode_bul = not default_city_mode_bul

    if default_city_mode_bul:
        add_default_city()


'''Создает словарь для дизайна кнопки режима показа города по умолчанию'''
def check_default_mode():
    message = 'Показывать город по умолчанию'

    if default_city_mode_bul:
        return {'mode': 'Выкл',
                'class': 'btn btn-danger',
                'message': message}
    return {'mode': 'Вкл',
            'class': 'btn btn-success',
            'message': message}


'''Создание главной страницы'''
def start_page(request):
    cities = City.objects.all()
    empty_input_error = 'hidden'
    # form = CityForm()

    if request.method == 'POST':
        if 'add_city_button' in request.POST:
            input_city = request.POST['input_city']

            if input_city != '':
                if single_city_mode_bul:
                    cities.delete()
                add_city(input_city)
            else:
                empty_input_error = ''

        elif 'single_mode' in request.POST:
            single_city_mode(cities)

        elif 'default_mode' in request.POST:
            default_city_mode()

        elif 'clear_all' in request.POST:
            clear_all(cities)

    all_cities = create_cities_dict(cities)

    context = {'all_info': all_cities,
               # 'form': form,
               'single_mode_button': check_single_mode(),
               'default_mode_button': check_default_mode(),
               'empty_input_error': empty_input_error}

    return render(request, 'main_page/buttons.html', context)
