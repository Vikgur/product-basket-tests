import itertools


class Product:
    """Класс, представляющий товар на маркетплейсе."""

    _id_counter = itertools.count(1)  # Генератор уникальных идентификаторов

    def __init__(self, name: str, price: int, weight: int) -> None:
        """
        Инициализация товара.

        :param name: Название товара
        :param price: Цена товара (натуральное число)
        :param weight: Вес товара (натуральное число)
        :raises ValueError: если цена или вес меньше 1
        """
        if price < 1:
            raise ValueError("Цена товара должна быть не меньше 1 у.е.")
        if weight < 1:
            raise ValueError("Вес товара должен быть не меньше 1 у.е.")

        self._id = next(self._id_counter)
        self._name = name
        self._price = price
        self._weight = weight

    @property
    def id(self) -> int:
        """Возвращает уникальный идентификатор товара."""
        return self._id

    @property
    def name(self) -> str:
        """Возвращает название товара."""
        return self._name

    @property
    def price(self) -> int:
        """Возвращает цену товара."""
        return self._price

    @property
    def weight(self) -> int:
        """Возвращает вес товара."""
        return self._weight


class Basket:
    """Класс, представляющий корзину товаров."""

    MAX_WEIGHT = 100  # Максимальный вес товаров в корзине
    MAX_ITEMS = 30  # Максимальное количество товаров в корзине

    def __init__(self) -> None:
        """Инициализация корзины."""
        self._products: dict[int, list[Product]] = {}

    def add_product(self, product: Product, quantity: int = 1) -> None:
        """
        Добавляет товар в корзину.

        :param product: Экземпляр класса Product
        :param quantity: Количество товара (по умолчанию 1)
        :raises TypeError: если переданы данные некорректного типа
        :raises ValueError: если добавление товара превышает лимиты корзины
        """
        if not isinstance(product, Product):
            raise TypeError(
                f"Ожидался объект Product, но получен {type(product).__name__}"
            )

        if not isinstance(quantity, int) or quantity < 1:
            raise TypeError(
                f"Ожидалось положительное целое число, но получено {type(quantity).__name__}"
            )

        if len(self.list_products) + quantity > self.MAX_ITEMS:
            raise ValueError(
                "Превышено максимальное количество товаров в корзине (30 у.е.)."
            )

        if self.total_weight + product.weight * quantity > self.MAX_WEIGHT:
            raise ValueError("Превышен максимальный вес товаров в корзине (100 у.е.).")

        if product.id not in self._products:
            self._products[product.id] = []

        self._products[product.id].extend([product] * quantity)

    def delete_product(self, product_id: int) -> None:
        """
        Удаляет товар из корзины целиком.

        :param product_id: Идентификатор товара
        """
        self._products.pop(product_id, None)

    @property
    def list_products(self) -> list[Product]:
        """Возвращает список всех товаров в корзине."""
        return [item for sublist in self._products.values() for item in sublist]

    @property
    def total_price(self) -> int:
        """Возвращает общую стоимость товаров в корзине."""
        return sum(product.price for product in self.list_products)

    @property
    def total_weight(self) -> int:
        """Возвращает общий вес товаров в корзине."""
        return sum(product.weight for product in self.list_products)

    @property
    def get_shipping_cost(self) -> int:
        """Возвращает стоимость доставки в зависимости от общей стоимости товаров."""
        if self.total_price == 0:
            return 0
        if self.total_price < 500:
            return 250
        elif 500 <= self.total_price < 1000:
            return 100
        return 0

    @property
    def get_price(self) -> int:
        """Возвращает итоговую стоимость корзины с учетом доставки."""
        return self.total_price + self.get_shipping_cost
