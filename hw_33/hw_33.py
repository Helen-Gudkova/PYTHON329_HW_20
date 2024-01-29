import json
import sqlite3
from pprint import pprint
from typing import List, Tuple, Any, Union


def read_json(file_path:str)-> None:
    """
    Функция возвращает список словарей с данными о городах.
    :param file_path: имя файла
    :return: None
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def read_sql_queries(file_path: str)-> str:
    """
    Функция возвращает строку с SQL-запросами
    :param file_path: имя файла
    :return: str
    """
    with open(file_path, 'r') as file:
        queries = file.read()
    return queries

def execute_query(query:str, db_path:str)-> None:
    """
     Функция - выполнение одного SQL-запроса
    :param query: запрос
    :param db_path: путь к файлу базы данных
    :return: None
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()


def execute_many_queries(queries: str, db_path: str)-> None:
    """
    Функция - выполнение нескольких SQL-запросов.
    :param queries: список SQL-запросов
    :param db_path: путь к файлу базы данных
    :return: None
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for query in queries:
        cursor.execute(query)
    conn.commit()
    conn.close()


def fetch_data(query:str, db_path:str)-> List[Tuple[Any, ...]]:
    """
    Функция возвращает данные, полученные в результате запроса
    :param query: SQL-запрос
    :param db_path: путь к файлу базы данных
    :return: List[Tuple[Any, ...]]
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data


def get_city_data(city_name: str, db_path:str)-> Union[List[Tuple[str, int, int, int, str, str]], None]:
    """
    Функция возвращает данные о городе, включая его субъект и район
    :param city_name: название города
    :param db_path: путь к файлу базы данных
    :return: Union[List[Tuple[str, int, int, int, str, str]], None]
    """
    query = f"SELECT c.city_name, c.lat, c.lon, c.population, s.subject_name, d.district_name " \
            f"FROM city c " \
            f"JOIN subject s ON c.subject_id = s.id " \
            f"JOIN district d ON c.district_id = d.id " \
            f"WHERE c.city_name = ?"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query, (city_name,))
    data = cursor.fetchall()
    conn.close()

    if len(data) > 0:
        return data
    else:
        return None

def main():
    # Пути к файлам
    json_file_path = 'cities.json'
    db_file_path = 'cities.db'

    # Считывание SQL-запросов из файла queries.sql
    with open('queries.sql', 'r', encoding='utf-8') as query_file:
        queries = query_file.read()
        print (queries)

    # Создание базы данных и подключение к ней
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Создание таблиц
    #cursor.executescript(queries)

    # Открываем файл и загружаем данные из JSON
    with open(json_file_path, 'r', encoding='utf-8') as file:
        city_data = json.load(file)
        pprint(city_data)

    # Вставка данных о субъектах с предварительной проверкой
    for city in city_data:
        subject_name = city['subject']
        # Проверяем, существует ли уже такое значение subject_name
        cursor.execute('SELECT * FROM subject WHERE subject_name = ?', (subject_name,))
        existing_record = cursor.fetchone()
        if existing_record is None:
            cursor.execute('INSERT INTO subject (subject_name) VALUES (?)', (subject_name,))
        else:
            print(f"Запись с именем '{subject_name}' уже существует. Пропускаем вставку.")

    # Вставка данных о округах с предварительной проверкой
    for city in city_data:
        district_name = city['district']
        # Проверяем, существует ли уже такое значение subject_name
        cursor.execute('SELECT * FROM district WHERE district_name = ?', (district_name,))
        existing_record = cursor.fetchone()
        if existing_record is None:
            cursor.execute('INSERT INTO district (district_name) VALUES (?)', (district_name,))
        else:
            print(f"Запись с именем '{district_name}' уже существует. Пропускаем вставку.")

    # Создание и заполнение таблицы городов с использованием подзапросов
    data_to_insert = [(city['name'], city['district'], city['subject'],city['coords']['lat'],city['coords']['lon'],city['population']) for city in city_data]

    cursor.executemany('''
        INSERT INTO city (city_name,district_id, subject_id,lat,lon,population) 
        SELECT ?, 
            (SELECT id FROM district WHERE district_name = ?),
            (SELECT id FROM subject WHERE subject_name = ?),
            ?,?,?
    ''', data_to_insert)

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()