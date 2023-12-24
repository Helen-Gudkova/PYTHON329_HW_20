import json
import requests
from dataclasses import dataclass
from typing import Optional, Any, Dict
from marshmallow import Schema, fields, validate, ValidationError

class WeatherRequest:
    def get_weather(self,city_name: str) ->  Optional[Dict[str, Any]]:
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

weather_req = WeatherRequest()
response = weather_req.get_weather('Москва')
print(response)
