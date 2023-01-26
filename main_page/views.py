from django.shortcuts import render
from .models import City
from .backend.add_city import InputCity
from .backend.default_city_mode import DefaultMode
from .backend.single_city_mode import SingleMode
from .backend.get_city_info import create_cities_dict
from .backend.clear import clear


def start_page(request):
    """Создание главной страницы"""
    cities = City.objects.all()
    empty_input_error = 'hidden'
    # form = CityForm()

    if request.method == 'POST':
        if 'add_city_button' in request.POST:
            input_city = request.POST['input_city']

            if input_city != '':
                if SingleMode.check:
                    cities.delete()
                InputCity(input_city).check()
            else:
                empty_input_error = ''

        elif 'single_mode' in request.POST:
            SingleMode.switch(cities, DefaultMode.check, DefaultMode.default_city)

        elif 'default_mode' in request.POST:
            DefaultMode.switch(cities, SingleMode.check)

        elif 'clear_all' in request.POST:
            clear(cities, DefaultMode.check, DefaultMode.default_city)

    all_cities = create_cities_dict(cities)

    context = {'all_info': all_cities,
               # 'form': form,
               'single_mode_button': SingleMode.button(),
               'default_mode_button': DefaultMode.button(),
               'empty_input_error': empty_input_error}

    return render(request, 'main_page/buttons.html', context)
