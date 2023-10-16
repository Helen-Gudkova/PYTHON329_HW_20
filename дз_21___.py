import csv
import json
from typing import List, Dict, Union, Any

class CsvFileHandler:
    """
        Класс для работы с csv - файлами
        """
    def read_file(self, filepath: str, as_dict: bool = False) -> Union[List[List[str]], List[Dict[str, str]]]:
        """
                Метод для чтения данных из CSV файла
                реализован как метод экземпляра
                По умолчанию данные должны возвращаться в виде списка списков,
                но при установке флага `as_dict` в `True`, данные должны возвращаться в виде списка словарей
                :param filepath: файл данных в формате csv
                :param as_dict: флаг для управления форматом ввода/вывода данных
                :return: список списков или список словарей
                """
        with open(filepath, 'r', newline='') as file:
            reader = csv.reader(file)
            if as_dict == True:
                headers = next(reader)
            elif as_dict == False:
                data = [row for row in reader]
        return data

    def write_file(self, filepath: str, data: Union[List[List[str]], List[Dict[str, str]]], as_dict: bool = False) -> None:
        """
                Метод для записи данных в CSV файл
                реализован как метод экземпляра
                По умолчанию данные должны возвращаться в виде списка списков,
                но при установке флага `as_dict` в `True`, данные должны возвращаться в виде списка словарей
                :param filepath: файл данных в формате csv
                :param data: список списков или список словарей
                :param as_dict: флаг для управления форматом ввода/вывода данных
                :return:None
                """
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            if as_dict:
                headers = data[0]
                #headers = data[0].keys()
                writer.writerow(headers)
                for item in data:
                    writer.writerow(list(item))
                    #writer.writerow(list(item.values()))
            else:
                writer.writerows(data)

    def append_file(self,filepath: str, data: Union[List[List[str]], List[Dict[str, str]]], as_dict: bool = False) -> None:
        """
                Метод для дописывания данных в CSV файл
                реализован как метод экземпляра
                Флаг `as_dict` работает аналогично как в методе `write_file`
                :param filepath: файл данных в формате csv
                :param data: список списков или список словарей
                :param as_dict: флаг для управления форматом ввода/вывода данных
                :return:None
                """
        with open(filepath, 'a', newline='') as file:
            writer = csv.writer(file)
            if as_dict:
                headers = data[0]
                #headers = data[0].keys()
                writer.writerow(headers)
                for item in data:
                    writer.writerow(list(item))
                    #writer.writerow(list(item.values()))
            else:
                writer.writerows(data)

class JsonFileHandler:
    """
        Класс для работы с json - файлами
        """
    def read_file(self, filepath: str, as_dict: bool = False) -> Union[List[List[str]], List[Dict[str, str]]]:
        """
                Метод для чтения данных из JSON файла
                реализован как метод экземпляра
                Флаг `as_dict` работает аналогично как в классе `CsvFileHandler`.
                :param filepath: Файл данных в формате json
                :param as_dict: флаг для управления форматом ввода/вывода данных
                :return: список списков или список словарей
                """
        with open(filepath, 'r') as file:
            data = json.load(file)
            if as_dict and isinstance(data, list):
                data = [dict(item) for item in data]
        return data

    def write_file(self, filepath: str, data: Union[List[List[str]], List[Dict[str, str]]], as_dict: bool = False) -> None:
        """
                Метод для записи данных в JSON файл
                реализован как метод экземпляра
                Флаг `as_dict` работает аналогично как в классе `CsvFileHandler`.
                :param filepath: Файл данных в формате json
                :param data: список списков или список словарей
                :param as_dict: флаг для управления форматом ввода/вывода данных
                :return: None
                """
        with open(filepath, 'w') as file:
            if as_dict:
                json.dump(data, file, indent=4)
            else:
                json.dump(data, file)

    def append_file(self, filepath: str, data: Union[List[List[str]], List[Dict[str, str]]], as_dict: bool = False) -> None:
        """
                Метод для дописывания данных в JSON файл
                реализован как метод экземпляра
                При попытке вызова этого метода должно возникать исключение `TypeError` с сообщением,
                что данный тип файла не поддерживает операцию дописывания
                :param filepath: файл данных в формате json
                :param data: список списков или список словарей
                :param as_dict:  флаг для управления форматом ввода/вывода данных
                :return: None
                """
        raise TypeError("Данный тип файла не поддерживает операцию дописывания.")

class TxtFileHandler:
    """
           Класс для работы с txt - файлами
        """
    def read_file(self, filepath: str) -> List[str]:
        """
                Метод для чтения данных из TXT файла.
                Должен быть реализован как метод экземпляра.
                :param filepath: Файл данных в формате txt
                :return: List[str]
                """
        with open(filepath, 'r') as file:
            data = file.readlines()
        return data

    def write_file(self, filepath: str, data: List[str]) -> None:
        """
                Метод для записи данных в TXT файл.
                Должен быть реализован как метод экземпляра.
                :param filepath: Файл данных в формате txt
                :param data: List[str]
                :return: None
                """
        with open(filepath, 'w') as file:
            file.writelines(data)

    def append_file(self, filepath: str, data: List[str]) -> None:
        """
                Метод для дописывания данных в TXT файл.
                Должен быть реализован как метод экземпляра.
                :param filepath: Файл данных в формате txt
                :param data: List[str]
                :return: None
                """
        with open(filepath, 'a') as file:
            file.writelines(data)

# Пример использования:
csv_handler = CsvFileHandler()
json_handler = JsonFileHandler()
txt_handler = TxtFileHandler()

data_csv = [['John', 'Doe', 'john@example.com'], ['Jane', 'Smith', 'jane@example.com']]
csv_handler.write_file('data.csv', data_csv)
csv_data = csv_handler.read_file('data.csv')
print(csv_data)

data_json = [{'name': 'John', 'email': 'john@example.com'}, {'name': 'Jane', 'email': 'jane@example.com'}]
json_handler.write_file('data.json', data_json)
json_data = json_handler.read_file('data.json')
print(json_data)

data_txt = ['Hello', 'World']
txt_handler.write_file('data.txt', data_txt)
txt_data = txt_handler.read_file('data.txt')
print(txt_data)
