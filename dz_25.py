from typing import Tuple, Dict, Any

class CustomMeta(type):
    """
    Метакласс,который автоматически добавляет новое поле и метод в классы,
    использующие этот метакласс
    """

    def __new__(cls, name: str, bases: Tuple[type, ...], dct: Dict[str, Any]) -> 'CustomMeta':
        """
        Магический метод __new__
        для создания классов и добавления в них необходимых атрибутов
        :param name: строка, представляющая имя создаваемого класса
        :param bases: кортеж, содержащий базовые классы нового класса
        :param dct:  словарь, содержащий пространство имен (атрибуты и методы), определенные в классе.
         В dct хранится информация о полях и методах, объявленных в классе
        :return: 'CustomMeta'
        """
        # Добавление нового поля в класс
        dct['extra_field'] = 'Значение по умолчанию'

        # Добавление нового метода в класс
        def extra_method(self):
            print("Это дополнительный метод, добавленный метаклассом")

        dct['extra_method'] = extra_method
        return super().__new__(cls, name, bases, dct)


class MyClass1(metaclass=CustomMeta):
    """
    Простой класс использующий метакласс
    """
    extra_field: str
    extra_method: Any

    def __init__(self) -> None:
        pass


class MyClass2(metaclass=CustomMeta):
    """
    Простой класс использующий метакласс
    """
    extra_field: str
    extra_method: Any

    def __init__(self) -> None:
        pass


obj1 = MyClass1()
print(obj1.extra_field)
obj1.extra_method()  # Выведет сообщение, определенное в методе extra_method
obj2 = MyClass2()
print(obj2.extra_field)
obj1.extra_method()  # Выведет сообщение, определенное в методе extra_method
