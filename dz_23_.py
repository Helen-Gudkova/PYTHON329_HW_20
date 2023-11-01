### Система расчёта доставки товаров ###
import json
from dataclasses import dataclass
from typing import List, Dict, Union


### ** Базовые классы: **
class Product:
    """ Базовый класс инициализации товара по атрибутам"""
    def __init__(self, dimensions: float, weight: float, fragility: bool, price: float, category: int,
                 name: str) -> None:
        """
        Конструктор класса Product
        :param dimensions: габариты
        :param weight: вес
        :param fragility: хрупкость: True/False
        :param price: цена
        :param category: категория
        :param name: название
        :return: None
        """
        self.dimensions = dimensions
        self.weight = weight
        self.fragility = fragility
        self.price = price
        self.category = category
        self.name = name

    def info(self) -> str:
        """ Метод вывода информации о товаре
        :return: str"""
        return f"габариты {self.dimensions}, вес {self.weight}," \
               f" хрупкость {self.fragility}, цена {self.price}, категория {self.category}, название {self.name}"


class Delivery(Product):
    """ Базовый класс расчета
    стоимости доставки, учитывая атрибуты товара и скорости доставки для
    разных категорий товаров
    """
    def __init__(self, dimensions: float, weight: float, fragility: bool, price: float, category: int,
                 name: str, delivery_speed: float) -> None:
        """
        Конструктор класса Delivery
        :param dimensions: габариты
        :param weight: вес
        :param fragility: хрупкость: True/False
        :param price: цена
        :param category: категория
        :param name: название
        :param delivery_speed: скорость доставки
        :return: None
        """
        super().__init__(dimensions, weight, fragility, price, category, name)
        self.delivery_speed = delivery_speed

    def calculate_cost(self) -> Union[float, str]:
        """
        Метод для расчета стоимости доставки,
        учитывая атрибуты товара
        (габариты, вес, хрупкость и цену для
        разных категорий товаров)
        :return: Union[float, str]
        """
        if self.category == 1:
            if self.fragility:
                delivery_option = self.weight * 0.1 + self.price * 0.05 + self.dimensions * 0.05 + self.delivery_speed + 0.1
            else:
                delivery_option = self.weight * 0.1 + self.price * 0.05 + self.dimensions * 0.05 + self.delivery_speed
            return delivery_option
        elif self.category == 2:
            if self.fragility:
                delivery_option = self.weight * 0.05 + self.price * 0.05 + self.dimensions * 0.05 + self.delivery_speed + 0.1
            else:
                delivery_option = self.weight * 0.05 + self.price * 0.05 + self.dimensions * 0.05 + self.delivery_speed
            return delivery_option
        elif self.category == 3:
            if self.fragility:
                delivery_option = self.weight * 0.001 + self.price * 0.05 + self.dimensions * 0.05 + self.delivery_speed + 0.1
            else:
                delivery_option = self.weight * 0.001 + self.price * 0.05 + self.dimensions * 0.05 + self.delivery_speed
            return delivery_option
        else:
            return "Unknown category"

### ** Датаклассы: **
### Тайпхинты для методов возвращающих экземпляры собственного класса
@dataclass
class PromoCodeData:
    """Датакласс инициализации кода и скидки в процентах"""
    def __init__(self, code: str, discount: float) -> None:
        """
        Конструктор класса PromoCodeData
        :param code: код
        :param discount: скидка в процентах
        :return: None
        """
        self.code = code
        self.discount = discount

    @classmethod
    def load_from_json(cls, json_path: str) -> List['PromoCodeData']:
        """
        Метод загрузки информации о промо-кодах из JSON файла.
        С десериализацией данных из файла.
        :param json_path:JSON файл
        :return: List['PromoCodeData'] - список промокодов
        """
        with open(json_path, 'r', encoding='UTF-8') as file:
            data = json.load(file)
            promocodes = []
        for item in data:
            if 'code' in item:
                promocodes.append(item['code'])
        return promocodes


###  Миксины:
class InternationalMixin:
    """Класс миксин для корректировки стоимости доставки
     на основе атрибутов товара"""
    def __init__(self, dimensions: float, weight: float, fragility: bool) -> None:
        """
        Конструктор класса InternationalMixin
        :param dimensions: габариты
        :param weight: вес
        :param fragility: хрупкость: True/False
        :return: None
        """
        self.weight = weight
        self.dimensions = dimensions
        self.fragility = fragility

    def adjust_for_weight(self) -> None:
        """
        Метод коррекции стоимости на основе веса товара.
        :return: None
        """
        print(f'Введите вес товара {self.weight}')

    def adjust_for_dimensions(self) -> None:
        """
        Метод коррекции стоимости на основе габаритов товара.
        :return: None
        """
        print(f'Введите габариты товара {self.dimensions}')

    def adjust_for_fragility(self) -> None:
        """
        Метод коррекции стоимости, если товар хрупкий
        :return: None
        """
        print(f'Введите признак хрупкости товара {self.fragility}')


class SortByCostMixin:
    """Класс миксин сортировки списка вариантов доставки
    """
    def __init__(self, delivery_options: List[Dict]) -> None:
        """ Конструктор класса SortByCostMixin
        :param delivery_options: List[Dict]
        :return: None
        """
        self.delivery_options = delivery_options

    def sort_by_price_ascending(self) -> List[Dict]:
        """
        Метод сортировки списка вариантов доставки,
        от меньшего к большему по цене.
        :return: List[Dict]
        """
        print(f"Первоначальный список вариантов доставки для служб A, B и C (скорость доставки: цена):\n {self.delivery_options}")
        self.delivery_options = sorted(self.delivery_options, key=lambda x: list(x.values())[0])
        return self.delivery_options

    def sort_by_price_descending(self) -> List[Dict]:
        """
        Метод сортировки списка вариантов доставки,
        от большего к меньшему по цене.
        :return: List[Dict]
        """
        self.delivery_options = sorted(self.delivery_options, key=lambda x: list(x.values())[0], reverse=True)
        return self.delivery_options

    def sort_by_delivery_speed(self) -> List[Dict]:
        """
        Метод сортировки списка вариантов доставки,
        по скорости доставки.
        :return: List[Dict]
        """
        self.delivery_options = sorted(self.delivery_options, key=lambda x: list(x.keys())[0])
        return self.delivery_options


### ** Специализированные классы доставки **:
class DeliveryServiceA(Product):
    """
    Класс доставки для службы A
    """
    def __init__(self, dimensions: float, weight: float, fragility: bool, price: float, category: int,
                 name: str, delivery_speed: float) -> None:
        """ Конструктор класса DeliveryServiceA
        :param dimensions: габариты
        :param weight: вес
        :param fragility: хрупкость: True/False
        :param price: цена
        :param category: категория
        :param name: название
        :param delivery_speed: скорость доставки
        :return: None
        """
        super().__init__(dimensions, weight, fragility, price, category, name)
        self.delivery_speed = delivery_speed

    def calculate_cost_for_service(self) -> float:
        """
        Формула расчета стоимости
        для службы доставки A.
        :return: float
        """
        cost = self.weight * 0.1 + self.price * 0.05 + self.dimensions * 0.05 + self.delivery_speed
        return cost


class DeliveryServiceB(InternationalMixin):
    """ Класс доставки для службы B
    """
    def __init__(self, dimensions: float, weight: float, fragility: bool, delivery_speed: float) -> None:
        """
        Дополнительные атрибуты инициализации для
        службы В
        :param dimensions: габариты
        :param weight: вес
        :param fragility: хрупкость: True/False
        :param delivery_speed: скорость доставки
        :return: None
        """
        super().__init__(dimensions, weight, fragility)
        self.delivery_speed = delivery_speed

    def adjust_for_weight(self) -> None:
        """
        Переопределение метода для службы В
        :return: None
        """
        super().adjust_for_weight()  # Дополнительные действия для службы В

    def adjust_for_dimensions(self) -> None:
        """
        Переопределение метода для службы В
        :return: None
        """
        super().adjust_for_dimensions()  # Дополнительные действия для службы В

    def adjust_for_fragility(self) -> None:
        """
        Переопределение метода для службы В
        :return: None
        """
        super().adjust_for_fragility()  # Дополнительные действия для службы В

    def calculate_cost_for_service(self) -> float:
        """
        Реализация логики службы B с
         интеграцией `InternationalMixin`.
        :return: float
        """
        cost = self.weight * 0.2 + self.fragility + self.dimensions * 0.1 + self.delivery_speed
        return cost


class DeliveryServiceC(InternationalMixin):
    """ Класс доставки для службы C
        """
    def __init__(self, dimensions: float, weight: float, fragility: bool, delivery_speed: float) -> None:
        """
        Дополнительные атрибуты инициализации для
        службы C
        :param dimensions: габариты
        :param weight: вес
        :param fragility: хрупкость: True/False
        :param delivery_speed: скорость доставки
        :return: None
        """
        super().__init__(dimensions, weight, fragility)
        self.delivery_speed = delivery_speed

    def adjust_for_weight(self) -> None:
        """
        Переопределение метода для службы C
        :return: None
        """
        super().adjust_for_weight()  # Дополнительные действия для службы C

    def adjust_for_dimensions(self) -> None:
        """
        Переопределение метода для службы C
        :return: None
        """
        super().adjust_for_dimensions()  # Дополнительные действия для службы C

    def adjust_for_fragility(self) -> None:
        """
        Переопределение метода для службы C
        :return: None
        """
        super().adjust_for_fragility()  # Дополнительные действия для службы C

    def calculate_cost_for_service(self) -> float:
        """
        Реализация логики службы C с
         интеграцией `InternationalMixin`.
        :return: float
        """
        cost = self.weight * 0.05 + self.fragility + self.dimensions * 0.02 + self.delivery_speed
        return cost


###  **Логика промо-кода**:
class PromoCodeMixin(PromoCodeData):
    """Класс для логики промо-кода"""
    def __init__(self, code: str, discount: float, promo_code: str) -> None:
        """
        Конструктор инициализации для
        класса PromoCodeMixin
        :param code: str
        :param discount: float
        :param promo_code: str
        :return: None
        """
        super().__init__(code, discount)
        self.promo_code = promo_code

    def apply_promo_code(self, promo_code: str) -> str:
        """
        Метод проверки, есть ли скидка по промо-коду,
        и, если да, корректировать стоимость доставки.
        :return: str
        """
        if self.code == self.promo_code:
            return f"Промо-код {self.promo_code} уже использован"
        promocodes = self.load_from_json('sale.json')
        for promo in promocodes:
            if promo_code == promo:
                #self.discount = promo.discount
                return f"Промо-код {promo_code} успешно применен"
        return "Недействительный промо-код"

    def adjust_delivery_cost(self, current_cost: float) -> float:
        """Расчет стоимости доставки с
        учетом применения промо-кода и его скидки
        :param: current_cost
        :return: float"""
        if self.discount is not None:
            adjusted_cost = (current_cost * (100-float(self.discount)))/100
            return adjusted_cost
        return current_cost

def main():
    # Создаем объекты класса Product с разными категориями (1,2,3)
    product1 = Product(10.5, 4.5, True, 10000, 1, "блендер")
    product2 = Product(15.5, 6.5, False, 15000, 2, "набор ножей")
    product3 = Product(5.5, 2.5, True, 8000, 3, "сковородка")
    product1 = product1.info()
    product2 = product2.info()
    product3 = product3.info()
    print(f"Товар 1: {product1}")
    print(f"Товар 2: {product2}")
    print(f"Товар 3: {product3}")
    delivery1 = Delivery(10.5, 4.5, True, 10000, 1, "блендер", 10.5)
    delivery2 = Delivery(15.5, 6.5, False, 15000, 2, "набор ножей", 15.5)
    delivery3 = Delivery(5.5, 2.5, True, 8000, 3, "сковородка", 5.5)
    print(f"Стоимость доставки для товара 1: {delivery1.calculate_cost()}")
    print(f"Стоимость доставки для товара 2: {delivery2.calculate_cost()}")
    print(f"Стоимость доставки для товара 3: {delivery3.calculate_cost()}")
    sale = PromoCodeData("SALE20", 20)
    sales = sale.load_from_json('sale.json')
    print(f"Список промо-кодов из json файла:\n {sales}")
    # Инициализируем объекты служб доставки
    service_a = DeliveryServiceA(10.5, 4.5, True, 10000, 1, "блендер", 100.5)
    print(f"Стоимость доставки в службе A: {round(service_a.calculate_cost_for_service(),2)}")
    service_b = DeliveryServiceB(10.5, 4.5, True, 80.5)
    print(f"Стоимость доставки в службе B: {round(service_b.calculate_cost_for_service(),2)}")
    service_c = DeliveryServiceC(5.5, 1.5, False, 50.5)
    print(f"Стоимость доставки в службе C: {round(service_c.calculate_cost_for_service(),2)}")
    # Применяем промо-код, если есть
    promo = PromoCodeMixin("PROMO15", 10, "DISCOUNT10")
    print(promo.apply_promo_code("DISCOUNT10"))
    current_cost = 601.47
    adjusted_cost = promo.adjust_delivery_cost(current_cost)
    print(f"Стоимость доставки после применения скидки: {adjusted_cost}")
    # Получаем отсортированный список доставок
    sort_by_cost = SortByCostMixin([{100.5: 601.47}, {80.5: 103.45}, {50.5: 50.69}])
    print(f"Сортировка списка вариантов (цена по возрастанию):{sort_by_cost.sort_by_price_ascending()}")
    print(f"Сортировка списка вариантов (цена по убыванию):{sort_by_cost.sort_by_price_descending()}")
    print(f"Сортировка списка вариантов (по скорости доставки):{sort_by_cost.sort_by_delivery_speed()}")

if __name__ == "__main__":
    main()
