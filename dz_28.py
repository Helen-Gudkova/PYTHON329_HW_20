import json
import requests
from dataclasses import dataclass
from typing import Optional, Any, Dict
from marshmallow import Schema, fields, validate, ValidationError
from marshmallow_jsonschema import JSONSchema


def get_weather(city_name: str) ->  Optional[Dict[str, Any]]:
    """
    Метод - использование API для получения погодных данных
    :param city_name: название города
    :return: прогноз погоды с OpenWeatherMap API.
    """
    api_key = "685d28ce7d0a2ce30ffb0d273c4e32fc"
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'lang': 'ru',
        'units': 'metric',
        'appid': api_key
    }
    response = requests.get(base_url, params=params)
    return response.json()

@dataclass
class CurrentWeather:
    """
    Датакласс CurrentWeather
    включающий поля из ответа API. Некоторые поля
    должны быть обязательными, другие – необязательными
    """
    city: str
    temperature: float
    description: str
    humidity: Optional[int] = None # Поле 'humidity' теперь необязательное
    wind_speed: Optional[float] = None # Поле 'wind_speed' теперь необязательное


class CurrentWeatherSchema(Schema):
    """
    Класс CurrentWeather - реализация схемы Marshmallow
    с расширением созданной схемы, добавив в неё дополнительные проверки - проверка на диапазон
    значений
    """
    city = fields.Str(required=True)
    temperature = fields.Float(required=True,
                               validate=validate.Range(min=-100, max=100))  # Пример проверки диапазона значений
    description = fields.Str(required=True)
    humidity = fields.Int(allow_none=True,
                          validate=validate.Range(min=0, max=100))  # Пример проверки диапазона значений
    wind_speed = fields.Float(allow_none=True, validate=validate.Range(min=0))  # Пример проверки диапазона значений

    class Meta:
        """
        Meta - класс для управления поведением схемы
        """
        # ordered = True - сохраняет порядок полей в схеме
        ordered = True
def main():
    # Пример использования
    city = input("Введите город:")
    weather_data = get_weather(city)
    print("Обработка данных о погоде с использованием API:")
    print(weather_data)

    # Создание экземпляра схемы Marshmallow
    schema = CurrentWeatherSchema()

    # Валидация данных с помощью схемы
    result = schema.load({
        'city': weather_data['name'],
        'temperature': weather_data['main']['temp'],
        'description': weather_data['weather'][0]['description'],
        'humidity': weather_data['main'].get('humidity'),
        'wind_speed': weather_data['wind'].get('speed')
     })

    if result:
        # Создание экземпляра класса CurrentWeather
        current_weather = CurrentWeather(**result)
        print("Экземпляр класса CurrentWeather:")
        print(current_weather)
    else:
        # Обработка ошибок валидации, если они есть
        errors = schema.validate({
            'city': weather_data['name'],
            'temperature': weather_data['main']['temp'],
            'description': weather_data['weather'][0]['description'],
            'humidity': weather_data['main'].get('humidity'),
            'wind_speed': weather_data['wind'].get('speed')
        })
        print("Ошибки валидации данных:")
        print(errors)

    # Генерация JSON-схемы из схемы Marshmallow
    json_schema = JSONSchema().dump(CurrentWeatherSchema())
    print("Преобразования моей схемы Marshmallow в JSONSchema:")
    print(json_schema)

    # Сохранение сгенерированной схемы в файл
    with open('current_weather_schema.json', 'w') as file:
        json.dump(json_schema, file, indent=4)

if __name__ == '__main__':
    main()