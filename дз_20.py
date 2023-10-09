from typing import Any, Callable
import csv

def password_validator(length: int = 8, uppercase: int = 1, lowercase: int = 1, special_chars: int = 1) -> Callable:
    """
    Декоратор для валидации паролей.
    Параметры:
    :param length: Минимальная длина пароля (по умолчанию 8).
    :param uppercase: Минимальное количество букв верхнего регистра (по умолчанию 1).
    :param lowercase: Минимальное количество букв нижнего регистра (по умолчанию 1).
    :param special_chars: Минимальное количество спец-знаков (по умолчанию 1).
    :return: Callable
    """
    def decorator(func):
        def wrapper(username, password):
            if length < 8:
                raise ValueError("Длина пароля должна быть больше или равно 8 символов!")
            elif special_chars < 1:
                raise ValueError("Минимальное количество спец-знаков, по умолчанию 1!")
            elif uppercase < 1:
                raise ValueError("Минимальное количество букв верхнего регистра, по умолчанию 1!")
            elif lowercase < 1:
                raise ValueError("Минимальное количество букв нижнего регистра, по умолчанию 1!")
            elif length < 8 and special_chars < 1:
                raise ValueError("Длина пароля должна быть больше или равно 8 символов и минимальное количество спец-знаков, по умолчанию 1!")
            elif length < 8 and uppercase < 1:
                raise ValueError("Длина пароля должна быть больше или равно 8 символов и минимальное количество букв верхнего регистра, по умолчанию 1!")
            elif length < 8 and lowercase < 1:
                raise ValueError("Длина пароля должна быть больше или равно 8 символов и минимальное количество букв нижнего регистра, по умолчанию 1!")
            elif special_chars < 1 and uppercase < 1:
                raise ValueError("Минимальное количество спец-знаков, по умолчанию 1 и минимальное количество букв верхнего регистра, по умолчанию 1!")
            elif special_chars < 1 and lowercase < 1:
                raise ValueError("Минимальное количество спец-знаков, по умолчанию 1 и минимальное количество букв нижнего регистра, по умолчанию 1!")
            elif uppercase < 1 and lowercase < 1:
                raise ValueError("Минимальное количество букв верхнего регистра, по умолчанию 1 и минимальное количество букв нижнего регистра, по умолчанию 1!")
            elif length < 8 and uppercase < 1 and lowercase < 1:
                raise ValueError("Длина пароля должна быть больше или равно 8 символов и минимальное количество букв верхнего регистра, по умолчанию 1 и минимальное количество букв нижнего регистра, по умолчанию 1!")
            elif uppercase < 1 and lowercase < 1 and special_chars < 1:
                raise ValueError("Минимальное количество букв верхнего регистра и минимальное количество букв нижнего регистра и минимальное количество спец-знаков, по умолчанию 1!")
            elif length < 8 and special_chars < 1 and lowercase < 1:
                raise ValueError("Длина пароля должна быть больше или равно 8 символов и минимальное количество спец-знаков и минимальное количество букв нижнего регистра, по умолчанию 1!")
            elif length < 8 and special_chars < 1 and uppercase < 1:
                raise ValueError("Длина пароля должна быть больше или равно 8 символов и минимальное количество букв верхнего регистра и минимальное количество спец-знаков, по умолчанию 1!")
            return func(username, password)

        return wrapper

    return decorator

def username_validator() -> Callable:
    """
        Декоратор проверки имени пользователя на отсутствие пробелов
        :return: Callable
        """
    def decorator(func):
        def wrapper(username, password):
            if username.find(' ') >= 1:
                raise ValueError(f"В имени пользователя {username} есть пробелы!")
            return func(username, password)

        return wrapper

    return decorator


@password_validator(length=12, uppercase=1, lowercase=7, special_chars=1)
# Тестирование неудачного случая по паролю
# @password_validator(length=8, uppercase=1, lowercase=7, special_chars=0)
@username_validator()
def register_user(username: str, password: str) -> Any:
    """
       Функция для регистрации нового пользователя
       и записи имени пользователя и пароля в CSV файл
       :param username: Имя пользователя
       :param password: Пароль пользователя
       :return: вызываемый объект
    """
    # Запись имени пользователя и пароля в CSV файл
    with open("user.csv", "a", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])
    print("Пользователь успешно зарегистрирован!")

# Тестирование успешного случая
try:
    register_user("Helen", "&FortunaFort12")
    print("Регистрация прошла успешно!")
except ValueError as e:
    print(f"Ошибка: {e}")

# Тестирование неудачного случая по паролю
# try:
#     register_user("Helen", "FortunaFort")
#     print("Регистрация прошла успешно!")
# except ValueError as e:
#     print(f"Ошибка: {e}")

# Тестирование неудачного случая по username
# try:
#     register_user("Helen Doe", "&FortunaFort12")
#     print("Регистрация прошла успешно!")
# except ValueError as e:
#     print(f"Ошибка: {e}")
