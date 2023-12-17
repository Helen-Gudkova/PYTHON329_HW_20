"""
Не грусти.
Рано или поздно все станет понятно,
все станет на свои места и выстроится в единую красивую схему
как кружева.

Станет понятно, зачем все было нужно,
потому что все будет правильно.

Льюис Кэрролл. Алиса в стране чудес
"""

from abc import ABC, abstractmethod
from typing import Any, Optional


class IngredientFactory(ABC):
    """
    Абстрактный Класс `IngredientFactory`
    определяет интерфейс для создания ингредиентов пиццы
    """
    @abstractmethod
    def create_cheese(self) -> str:
        """
        Абстрактный метод, должен быть переопределен для возврата типа сыра
        :return: str
        """
        pass

    @abstractmethod
    def create_sauce(self) -> str:
        """
        Абстрактный метод, должен быть переопределен для возврата типа соуса
        :return: str
        """
        pass

class DodoIngredientFactory(IngredientFactory):
    """
    Класс реализует `IngredientFactory`, предоставляя конкретные ингредиенты, используемые Додо Пиццей
    """
    def create_cheese(self) -> str:
        """
        Метод возвращает тип сыра, используемый Додо Пиццей
        :return:str
        """
        return "Mozzarella"

    def create_sauce(self) -> str:
        """
        Метод возвращает тип соуса, используемый Додо Пиццей
        :return:str
        """
        return "Tomato sauce"

class SizeFactory:
    """
    Класс управления созданием размеров пиццы
    """
    def create_size(self, size: str) -> Optional[str]:
        """
        Метод принимает название размера и возвращает его описание
        :param size: размер пиццы
        :return: Optional[str]
        """
        available_sizes = ["Маленькая", "Средняя", "Большая"]
        if size in available_sizes:
            return f"Размер пиццы составляет: {size}."
        else:
            return None

class PizzaBuilder:
    """
    Собирает пиццу, используя ингредиенты и размеры
    """
    def __init__(self, ingredient_factory: IngredientFactory, size_factory: SizeFactory, pizza_type: str) -> None:
        """
        Инициализирует экземпляры фабрик и тип пиццы
        :param ingredient_factory:IngredientFactory
        :param size_factory:SizeFactory
        :param pizza_type:str
        """
        self.ingredient_factory = ingredient_factory
        self.size_factory = size_factory
        self.pizza_type = pizza_type
        self.size: Optional[str] = None # Размер теперь может быть либо str, либо None

    def set_size(self, size: str)-> None:
        """
        Устанавливает размер пиццы
        :param size: str
        :return: None
        """
        self.size = self.size_factory.create_size(size)

    def build(self) -> str:
        """
        Собирает и возвращает описание пиццы
        :return:str
        """
        cheese = self.ingredient_factory.create_cheese()
        sauce = self.ingredient_factory.create_sauce()
        if self.size is not None:  # Проверяем, установлен ли размер
            return f"{self.size} Пицца {self.pizza_type} с сыром {cheese} и соусом {sauce} приготовлена."
        else:
            return "Размер пиццы не установлен или указан недопустимый размер."

def create_pizza() -> str:
    """
    Создаёт заказ пиццы
    :return: Описание заказа пиццы
    """
    ingredient_factory = DodoIngredientFactory()
    size_factory = SizeFactory()
    builder = PizzaBuilder(ingredient_factory, size_factory, "Pepperoni")
    builder.set_size("Средняя")
    return builder.build()

def main():
    pizza_order = create_pizza()
    print(pizza_order)

if __name__ == "__main__":
    main()
