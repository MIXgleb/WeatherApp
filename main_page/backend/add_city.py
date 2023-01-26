from .get_city_info import get_weather
from ..models import City


class InputCity:
    def __init__(self, city):
        self.city = city

    def add(self):
        """Добавляет город в базу"""
        city = City(name=self.city)
        city.save()

    def add_default_city(self):
        """Добавляет город по умолчанию в начало списка"""
        if City.objects.filter(id=1).exists():
            return
        if City.objects.filter(name=self.city).exists():
            City.objects.get(name=self.city).delete()
        default_city = City(id=1, name=self.city)
        default_city.save()

    def check(self):
        """Проверяет, если ли введеный пользователем город в базе"""
        city = self._rename()

        if not City.objects.filter(name=city).exists():
            self.add()

    def _rename(self):
        """Переводит название города на русский язык"""
        new_city_name = get_weather(self.city)

        if new_city_name.get('message', 'OK') != 'OK':
            return self.city.capitalize()
        return new_city_name['name']
