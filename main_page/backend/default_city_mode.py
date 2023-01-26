from .add_city import InputCity


class DefaultMode:
    check = False
    default_city = 'Москва'

    @staticmethod
    def switch(cities, single_mode_check):
        """Переключает режим показа города по умолчанию"""
        DefaultMode.check = not DefaultMode.check

        if DefaultMode.check:
            if single_mode_check:
                cities.delete()
            InputCity(DefaultMode.default_city).add_default_city()

    @staticmethod
    def button():
        """Создает словарь для дизайна кнопки режима показа города по умолчанию"""
        message = 'Показывать город по умолчанию'

        if DefaultMode.check:
            return {'mode': 'Выкл',
                    'class': 'btn btn-danger',
                    'message': message}
        return {'mode': 'Вкл',
                'class': 'btn btn-success',
                'message': message}
