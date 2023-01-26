from .add_city import InputCity


def clear(cities, default_check, default_city):
    """Очищает базу с учетом модов"""
    cities.delete()

    if default_check:
        InputCity(default_city).add()
