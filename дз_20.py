from typing import Any, Callable
import csv
file_name = "PYTHON329 HW №20.csv"
user_name = input("Введите имя пользователя:")
user_password = input("Введите пароль:")
length = len(user_password)
uppercase = len([s for s in user_password if s.isupper()])
lowercase = len([s for s in user_password if s.islower()])
special_chars = len([s for s in user_password if s in ('!', '@','#')])

def password_validator(length: int = 8, uppercase: int = 1, lowercase: int = 1, special_chars: int = 1) -> None:
    """
    Декоратор для валидации паролей.
    Параметры:
    :param length: Минимальная длина пароля (по умолчанию 8).
    :param uppercase: Минимальное количество букв верхнего регистра (по умолчанию 1).
    :param lowercase: Минимальное количество букв нижнего регистра (по умолчанию 1).
    :param special_chars: Минимальное количество спец-знаков (по умолчанию 1).
    :return: None
    """
    def wrapper(user_password):
        if length >= 8 and special_chars >= 1 and uppercase >= 1 and lowercase >= 1:
            return func(user_password)
        else:
            raise ValueError("Пароль не соответствует заданным критериям сложности!")


def username_validator() -> None:
    """
        Декоратор проверки имени пользователя на отсутствие пробелов
        :return: None
        """
    def decorator(func):
        def wrapper(username,password):
            match username:
                case username as u if u.find(' ') == -1:
                    return func(username,password)
                case _:
                    raise ValueError(f"В имени пользователя {username} есть пробелы!")
        return wrapper
    return decorator

@password_validator(length=10, uppercase=2, lowercase=2, special_chars=2)
@username_validator()
def register_user(username: str, password: str) -> Callable:
    """
       Функция для регистрации нового пользователя
       и записи имени пользователя и пароля в CSV файл
       :param username: Имя пользователя
       :param password: Пароль пользователя
       :return: вызываемый объект
    """
    # Запись имени пользователя и пароля в CSV файл
    with open(file_name, 'a', encoding='utf-8') as file:
        file.write(f'\nИмя пользователя:{username}, пароль:{password}')
        print(f'\nИмя пользователя:{username}, пароль:{password}')

    def decorator(func: Callable) -> Callable:
        def wrapper(username) -> None:
            print(username)
            func(username)
            print(password)

        return wrapper

    return decorator
# Тестирование успешного случая
# try:
#     register_user("Helen","&FortunaFort15")
#     print("Регистрация прошла успешно!")
# except ValueError as e:
#     print(f"Ошибка: {e}")
# Тестирование неудачного случая по паролю
try:
    register_user(user_name,user_password)
    print("Регистрация прошла успешно!")
except ValueError as e:
    print(f"Ошибка: {e}")

# Тестирование неудачного случая по юзернейму
# try:
#     register_user(user_name,"Fortuna")
#     print("Регистрация прошла успешно!")
# except ValueError as e:
#     print(f"Ошибка: {e}")