import json
from typing import List, Optional
from random import choice


class JsonFile:
    """
        Класс для работы с json - файлами
        """

    @staticmethod
    def read(filepath: str) -> List[str]:
        """
            Метод для чтения данных из JSON файла
            реализован как метод экземпляра
            :param filepath: Файл данных в формате json
            :return: список городов
           """
        with open(filepath, 'r', encoding='UTF-8') as file:
            data = json.load(file)
        return data

    @staticmethod
    def write(filepath: str, data: List[str]) -> None:
        """
            Метод для записи данных в JSON файл
            реализован как метод экземпляра
            :param filepath: Файл данных в формате json
            :param data: List[str]
            :return: None
            """
        with open(filepath, 'w', encoding='UTF-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def remove(self, computer_city):
        pass


class Cities:
    """
        Класс для представления данных о городах из JSON-файла.
        Содержит список всех городов
        """

    def __init__(self,city_data: JsonFile) -> None:
        """
            Конструктор класса `Cities`,
            который принимает список городов `city_data`
            и инициализирует состояние объекта
            :param city_data: список городов
            :return: None
            """
        self.city_list = city_data


class CityGame:
    """
        Класс для управления самой игрой,
        он будет принимать экземпляр класса `Cities`
        в качестве аргумента
        """
    def __init__(self, cities: Cities) -> None:
        """
            Конструктор класса `CityGame`,
            который принимает экземпляр класса `Cities`
            и инициализирует состояние игры
            :param cities: список городов
            :return: None
         """
        self.cities = cities
        self.current_city: Optional[str] = None
        self.game_over: bool = False
        self.city_input: str = ""

    def start_game(self) -> None:
        """
            Метод для начала игры,
            который включает первый ход компьютера
            :return: None
            """
        print("Игра началась!")
        self.computer_turn()

    def human_turn(self, city_input: str) -> None:
        """
            Метод для хода человека,
            который будет обрабатывать ввод пользователя.
           :param city_input: Str
           :return: None
           """
        self.city_input = city_input
        if not self.game_over:
            if self.current_city is None or city_input[0].lower() == self.current_city[-1]:
                if city_input in self.cities.city_list:
                    self.cities.city_list.remove(city_input)
                    self.current_city = city_input
                    print(city_input)
                    self.computer_turn()
            elif city_input not in self.cities.city_list:
                    print("Такого города нет в списке!")
                    self.game_over = True
                    #self.check_game_over()
            else:
                print("Город должен начинаться на последнюю букву предыдущего города!")
                self.game_over = True
                #self.check_game_over()
        else:
            print("Игра окончена!")

    def computer_turn(self) -> None:
        """
            Метод для хода компьютера,
            который будет выбирать город на основе правил игры.
            :return: None
            """

        if not self.game_over:
            if self.current_city is None:
                self.current_city = choice(self.cities.city_list)
                print(f"Компьютер начинает с города: {self.current_city}")
            else:
                valid_cities = [city for city in self.cities.city_list if city[0].lower() == self.current_city[-1]]
                if valid_cities:
                    computer_city = choice(valid_cities)
                    self.cities.city_list.remove(computer_city)
                    self.current_city = computer_city
                    self.city_input = computer_city
                    print(f"Компьютер называет город: {computer_city}")
                else:
                    print("Компьютер не может назвать город!")
                    self.check_game_over()
        else:
            print("Игра окончена!")

    def check_game_over(self) -> None:
        """
            Метод для проверки завершения игры
            и определения победителя.
            :return: None
            """
        if not self.cities.city_list or self.city_input != self.current_city and self.city_input != "" and self.city_input[0].lower() != \
                self.current_city[-1]:
            self.game_over = True
            print("Игра окончена! Победил компьютер!")
        elif not self.current_city:
            self.game_over = True
            print("Игра окончена! Победил игрок!")
        else:
            self.game_over = False
    # def save_game_state(self) -> None:


class GameManager:
    """
        Класс принимает экземпляры классов `JsonFile`,
       `Cities` и `CityGame` в качестве аргументов.
       """

    def __init__(self, json_file: JsonFile, cities: Cities, city_game: CityGame) -> None:
        """
            Конструктор класса `GameManager`,
            который принимает экземпляры классов `JsonFile`,
            `Cities` и `CityGame` в качестве аргументов
            и инициализирует результат игры
            :param json_file: экземпляр класса `JsonFile`
            :param cities: экземпляр класса `Cities`
            :param city_game: экземпляр класса `CityGame`
            :return: None
            """
        self.json_file: JsonFile = json_file
        self.cities: Cities = cities
        self.city_game: CityGame = city_game

    def call(self) -> None:
        """
            Метод, который позволяет вызывать объекты этого класса,
            как если бы они были функциями
            и который будет запускать всю игру.
           :return:None
        """
        self.run_game()
        self.display_game_result()

    def run_game(self) -> None:
        """
            Метод для запуска игры,
            который будет вызывать методы `start_game()`,
            `human_turn()` и `computer_turn()`
            поочередно до завершения игры
            :return: None
        """
        self.city_game.start_game()
        while not self.city_game.game_over:
            city_input = input("Введите название города: ")
            self.city_game.human_turn(city_input)
            self.city_game.check_game_over()

    def display_game_result(self) -> None:
        """
            Метод для отображения результата игры после завершения
            :return:  None
        """
        if self.city_game.game_over:
            print("Игра завершена!!!")
        else:
            print("Игра еще не завершена!")


if __name__ == "__main__":
    # Создайте экземпляры необходимых классов
    json_file = JsonFile()
    cities_data=json_file.read('city_existing.json')
    print(cities_data)
    cities = Cities(cities_data)
    #cities.init(cities_data)
    # print(cities)
    game = CityGame(cities)
    # print(game)

    # Создайте экземпляр GameManager и вызовите его, чтобы начать игру
    game_manager = GameManager(json_file, cities, game)
    game_manager.call()

# json_file = JsonFile()
# cities = json_file.read('city_existing.json')
# print(cities)
# cities.append('City D')
# cities1=json_file.write('new_cities.json', cities)
# print(json_file.read('new_cities.json'))
