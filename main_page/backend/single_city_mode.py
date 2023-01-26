from .add_city import InputCity
from .clear import clear

class SingleMode:
    check = False

    @staticmethod
    def switch(cities, default_mode_check, default_city):
        """Переключает режим показа одного города"""
        SingleMode.check = not SingleMode.check
        length = len(cities)
        last_city = cities.last()
        clear(cities, default_mode_check, default_city)

        if not SingleMode.check and length != 0:
            InputCity(last_city).check()

        if SingleMode.check and not default_mode_check and length != 0:
            InputCity(last_city).add()

    @staticmethod
    def button():
        """Создает словарь для дизайна кнопки режима показа одного города"""
        message = 'Показывать только один город'

        if SingleMode.check:
            return {'mode': 'Выкл',
                    'class': 'btn btn-danger',
                    'message': message}
        return {'mode': 'Вкл',
                'class': 'btn btn-success',
                'message': message}
