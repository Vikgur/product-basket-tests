from typing import Any, Hashable, Union

import pytest

from product_basket import Product


# Позитивные тесты
def test_empty_basket_properties(basket):
    """
    Тест для пустой корзины.

    Проверяет, что:
    - Общая стоимость (total_price) равна 0.
    - Общий вес (total_weight) равен 0.
    - Стоимость доставки (get_shipping_cost) равна 0.
    - Итоговая стоимость (get_price) равна 0.
    - Список товаров (list_products) пуст.
    """
    assert (
        basket.total_price == 0
    ), f"Общая стоимость пустой корзины должна быть 0, но получила {basket.total_price}"
    assert (
        basket.total_weight == 0
    ), f"Общий вес пустой корзины должен быть 0, но получил {basket.total_weight}"
    assert (
        basket.get_shipping_cost == 0
    ), f"Стоимость доставки для пустой корзины должна быть 0, но получила {basket.get_shipping_cost}"
    assert (
        basket.get_price == 0
    ), f"Итоговая стоимость пустой корзины должна быть 0, но получила {basket.get_price}"
    assert (
        basket.list_products == []
    ), f"Список товаров пустой корзины должен быть пуст, но получил {basket.list_products}"


@pytest.mark.parametrize(
    "price, weight, expected_shipping_cost",
    [
        (300, 5, 250),
        (500, 10, 100),
    ],
)
def test_add_single_product(
    basket, price: int, weight: int, expected_shipping_cost: int
):
    """Тест добавления одного товара с разными характеристиками и проверкой доставки."""
    product = Product("Фен", price, weight)
    basket.add_product(product)

    assert (
        len(basket.list_products) == 1
    ), f"Количество товаров должно быть 1, но стало {len(basket.list_products)}"
    assert (
        basket.total_price == price
    ), f"Общая стоимость должна быть {price} у.е., но стала {basket.total_price}"
    assert (
        basket.total_weight == weight
    ), f"Общий вес должен быть {weight} у.е., но стал {basket.total_weight}"
    assert (
        basket.get_shipping_cost == expected_shipping_cost
    ), f"Доставка должна быть {expected_shipping_cost} у.е., но стала {basket.get_shipping_cost}"
    assert (
        basket.get_price == price + expected_shipping_cost
    ), f"Итоговая стоимость должна быть {price + expected_shipping_cost} у.е., но стала {basket.get_price}"


def test_delete_product(basket):
    """Тест удаления товара из корзины."""
    product = Product("Пылесос", 1200, 15)
    basket.add_product(product, 1)

    basket.delete_product(product.id)

    assert (
        len(basket.list_products) == 0
    ), f"Корзина должна быть пустой, но содержит {len(basket.list_products)} товаров"
    assert (
        basket.total_price == 0
    ), f"Стоимость корзины должна быть 0 у.е., но стала {basket.total_price}"
    assert (
        basket.total_weight == 0
    ), f"Общий вес корзины должен быть 0 у.е., но стал {basket.total_weight}"
    assert (
        basket.get_shipping_cost == 0
    ), f"Доставка должна быть 0 у.е., но стала {basket.get_shipping_cost}"
    assert (
        basket.get_price == 0
    ), f"Итоговая стоимость должна быть 0 у.е., но стала {basket.get_price}"


def test_add_product(basket):
    """Тест добавления товара в корзину, проверки итоговой цены, веса, списка товаров и стоимости доставки."""
    product = Product("Микроволновка", 500, 10)
    basket.add_product(product, 2)

    assert (
        len(basket.list_products) == 2
    ), f"Количество товаров в корзине должно быть 2, но стало {len(basket.list_products)}"
    assert all(
        p.name == "Микроволновка" for p in basket.list_products
    ), "В корзине должны быть только микроволновки"
    assert (
        basket.total_price == 1000
    ), f"Общая стоимость должна быть 1000 у.е., но стала {basket.total_price}"
    assert (
        basket.total_weight == 20
    ), f"Общий вес должен быть 20 у.е., но стал {basket.total_weight}"
    assert (
        basket.get_shipping_cost == 0
    ), f"Доставка должна быть бесплатной (0 у.е.), но стала {basket.get_shipping_cost}"
    assert (
        basket.get_price == 1000
    ), f"Итоговая стоимость должна быть 1000 у.е., но стала {basket.get_price}"


def test_add_multiple_products(basket):
    """Тест добавления нескольких товаров разных типов и проверки итоговых значений."""
    tv = Product("Телевизор", 800, 20)
    laptop = Product("Ноутбук", 1200, 5)
    phone = Product("Айфон", 700, 2)

    basket.add_product(tv, 1)
    basket.add_product(laptop, 1)
    basket.add_product(phone, 2)

    expected_price = 800 + 1200 + (700 * 2)
    expected_weight = 20 + 5 + (2 * 2)
    expected_shipping = 0

    assert (
        len(basket.list_products) == 4
    ), f"Количество товаров должно быть 4, но стало {len(basket.list_products)}"
    assert (
        basket.total_price == expected_price
    ), f"Общая стоимость должна быть {expected_price} у.е., но стала {basket.total_price}"
    assert (
        basket.total_weight == expected_weight
    ), f"Общий вес должен быть {expected_weight} у.е., но стал {basket.total_weight}"
    assert (
        basket.get_shipping_cost == expected_shipping
    ), f"Доставка должна быть {expected_shipping} у.е., но стала {basket.get_shipping_cost}"
    assert (
        basket.get_price == expected_price
    ), f"Итоговая стоимость должна быть {expected_price} у.е., но стала {basket.get_price}"


def test_sequential_usage(basket):
    """
    Тест последовательного использования корзины:
    - Добавляем несколько разных товаров.
    - Удаляем один тип товара.
    - Проверяем, что суммарные показатели (цена, вес и количество товаров)
      обновляются корректно.
    """
    tv = Product("Телевизор", 800, 20)
    laptop = Product("Ноутбук", 1200, 5)
    flash_drive = Product("Флешка", 100, 1)

    basket.add_product(tv, 1)
    basket.add_product(laptop, 2)
    basket.add_product(flash_drive, 3)

    expected_total_price = 800 + 2400 + 300
    expected_total_weight = 20 + 10 + 3
    expected_count = 1 + 2 + 3

    assert (
        basket.total_price == expected_total_price
    ), f"Итоговая стоимость должна быть {expected_total_price} у.е., но стала {basket.total_price}"
    assert (
        basket.total_weight == expected_total_weight
    ), f"Общий вес должен быть {expected_total_weight} у.е., но стал {basket.total_weight}"
    assert (
        len(basket.list_products) == expected_count
    ), f"В корзине должно быть {expected_count} товаров, но найдено {len(basket.list_products)}"

    basket.delete_product(laptop.id)

    expected_total_price = 800 + 300
    expected_total_weight = 20 + 3
    expected_count = 1 + 3

    assert basket.total_price == expected_total_price, (
        f"После удаления ноутбуков итоговая стоимость должна быть {expected_total_price} у.е., "
        f"но стала {basket.total_price}"
    )
    assert basket.total_weight == expected_total_weight, (
        f"После удаления ноутбуков общий вес должен быть {expected_total_weight} у.е., "
        f"но стал {basket.total_weight}"
    )
    assert len(basket.list_products) == expected_count, (
        f"После удаления ноутбуков в корзине должно быть {expected_count} товаров, "
        f"но найдено {len(basket.list_products)}"
    )


def test_sequential_operations(basket):
    """Тест последовательного добавления, удаления и повторного добавления товаров."""
    camera = Product("Камера", 700, 5)

    basket.add_product(camera, 2)
    assert (
        len(basket.list_products) == 2
    ), f"Количество товаров должно быть 2, но стало {len(basket.list_products)}"

    basket.delete_product(camera.id)
    assert (
        len(basket.list_products) == 0
    ), f"После удаления товаров корзина должна быть пустой, но содержит {len(basket.list_products)} товаров"

    basket.add_product(camera, 1)
    assert (
        len(basket.list_products) == 1
    ), f"После повторного добавления должно быть 1 товар, но стало {len(basket.list_products)}"


def test_mixed_operations(basket):
    """Тест чередования добавления, удаления и повторного добавления товаров."""
    fridge = Product("Холодильник", 1500, 50)
    kettle = Product("Чайник", 300, 3)
    toaster = Product("Тостер", 400, 4)

    basket.add_product(fridge, 1)
    assert (
        len(basket.list_products) == 1
    ), f"В корзине должен быть 1 товар, но стало {len(basket.list_products)}"

    basket.add_product(kettle, 2)
    assert (
        len(basket.list_products) == 3
    ), f"В корзине должно быть 3 товара, но стало {len(basket.list_products)}"

    basket.delete_product(fridge.id)
    assert (
        len(basket.list_products) == 2
    ), f"После удаления холодильника должно остаться 2 товара, но стало {len(basket.list_products)}"

    basket.add_product(toaster, 1)
    assert (
        len(basket.list_products) == 3
    ), f"В корзине должно быть 3 товара, но стало {len(basket.list_products)}"

    basket.delete_product(kettle.id)
    assert (
        len(basket.list_products) == 1
    ), f"После удаления чайника должно остаться 1 товар, но стало {len(basket.list_products)}"

    expected_price = toaster.price
    assert (
        basket.total_price == expected_price
    ), f"Итоговая стоимость должна быть {expected_price} у.е., но стала {basket.total_price}"


def test_list_products_returns_copy(basket):
    """Тест, проверяющий, что `list_products` возвращает копию списка товаров, а не сам список.

    После получения списка товаров и его изменения, внутреннее состояние корзины не должно изменяться.
    """
    product = Product("Айфон", 100, 10)
    basket.add_product(product, 2)

    products_copy = basket.list_products
    products_copy.clear()

    assert len(basket.list_products) == 2, (
        f"Внутренний список товаров должен оставаться неизменным после изменения копии, "
        f"но в корзине осталось {len(basket.list_products)} товаров"
    )


def test_list_products_multiple_calls_return_new_instance(basket):
    """
    Тест, проверяющий, что каждый вызов list_products возвращает новый экземпляр списка.

    Изменение одного экземпляра не должно влиять на другой, полученный повторным вызовом.
    """
    product = Product("Пылесос", 100, 10)
    basket.add_product(product, 2)

    products_first_call = basket.list_products
    products_first_call.append("робот")
    products_second_call = basket.list_products

    assert (
        products_first_call is not products_second_call
    ), "Каждый вызов list_products должен возвращать новый экземпляр, но получили одинаковые объекты"
    assert (
        len(products_second_call) == 2
    ), f"Второй вызов list_products должен вернуть 2 товара, но вернул {len(products_second_call)}"


def test_unique_product_ids():
    """Тест на уникальность идентификаторов у продуктов."""
    product1 = Product("Айфон14", 100, 1)
    product2 = Product("Айфон15", 200, 2)
    product3 = Product("Айфон16", 300, 3)
    ids = {product1.id, product2.id, product3.id}
    assert len(ids) == 3, "Каждый продукт должен иметь уникальный идентификатор."


def test_sequential_operations_unique_ids(basket):
    """Тест, проверяющий последовательные операции с разными продуктами и уникальность их идентификаторов.

    1. Добавляется товар A и удаляется.
    2. Добавляются два новых товара (B и C).
    3. Проверяется, что у B и C уникальные идентификаторы.
    4. Проверяется, что их идентификаторы не совпадают с удалённым товаром A.
    """
    product_a = Product("Фен", 300, 2)
    basket.add_product(product_a)
    id_a = product_a.id
    basket.delete_product(id_a)

    product_b = Product("Робот-пылесос", 10, 1)
    product_c = Product("Плойка", 20, 1)
    basket.add_product(product_b)
    basket.add_product(product_c)

    assert product_b.id != product_c.id, (
        f"Идентификаторы новых товаров должны быть уникальными, но у {product_b} ({product_b.id}) "
        f"и {product_c} ({product_c.id}) идентификаторы совпадают"
    )
    assert (
        product_b.id != id_a
    ), f"Новый товар {product_b} не должен иметь идентификатор, равный удалённому ({id_a}), но получил {product_b.id}"
    assert (
        product_c.id != id_a
    ), f"Новый товар {product_c} не должен иметь идентификатор, равный удалённому ({id_a}), но получил {product_c.id}"


# Граничные тесты
def test_product_immutability():
    """Тест, подтверждающий, что свойства объекта Product доступны только для чтения."""
    product = Product("Ноутбук", 1200, 5)
    with pytest.raises(AttributeError):
        product.price = 1500
    with pytest.raises(AttributeError):
        product.weight = 10
    with pytest.raises(AttributeError):
        product.name = "Новый ноутбук"


@pytest.mark.parametrize(
    "total_price, expected_shipping", [(499, 250), (500, 100), (999, 100), (1000, 0)]
)
def test_shipping_cost(basket, total_price: int, expected_shipping: int):
    """Тест расчета стоимости доставки на граничных значениях."""
    product = Product("Кондиционер", total_price, 20)
    basket.add_product(product)

    assert (
        basket.get_shipping_cost == expected_shipping
    ), f"Доставка должна быть {expected_shipping} у.е., но стала {basket.get_shipping_cost}"


def test_reaching_max_items_limit(basket):
    """Тест добавления товара до предельного количества (30 шт.), затем попытка добавить ещё должна вызывать исключение."""
    product = Product("Клавиатура", 50, 2)

    basket.add_product(product, 30)
    assert (
        len(basket.list_products) == 30
    ), f"В корзине должно быть 30 товаров, но стало {len(basket.list_products)}"

    with pytest.raises(
        ValueError, match="Превышено максимальное количество товаров в корзине"
    ):
        basket.add_product(product, 1)


def test_reaching_max_weight_limit(basket):
    """Тест добавления товара до предельного веса (100 у.е.), затем попытка добавить ещё должна вызывать исключение."""
    product = Product("Обогреватель", 200, 10)

    basket.add_product(product, 10)
    assert (
        basket.total_weight == 100
    ), f"Общий вес должен быть 100 у.е., но стал {basket.total_weight}"

    with pytest.raises(ValueError, match="Превышен максимальный вес товаров в корзине"):
        basket.add_product(product, 1)


def test_extreme_values(basket):
    """Тест работы с экстремальными значениями цены и веса.

    1. Создаётся товар с очень высокой ценой (`10**9`) и минимально допустимым весом (`1`).
    2. Товар добавляется в корзину.
    3. Проверяется, что:
       - Общая стоимость товаров в корзине соответствует ожидаемой экстремальной цене.
       - Общий вес в корзине корректно учитывается.
       - Доставка остаётся бесплатной (так как стоимость товара превышает 1000 у.е.).
       - Итоговая стоимость товаров соответствует стоимости товара без доплат.
    """
    extreme_price = 10**9
    extreme_weight = 1
    product = Product("Супер-пупер товар", extreme_price, extreme_weight)
    basket.add_product(product)

    assert (
        basket.total_price == extreme_price
    ), f"Общая стоимость должна быть {extreme_price} у.е., но стала {basket.total_price}"
    assert (
        basket.total_weight == extreme_weight
    ), f"Общий вес должен быть {extreme_weight} у.е., но стал {basket.total_weight}"
    assert (
        basket.get_shipping_cost == 0
    ), f"Доставка должна быть бесплатной (0 у.е.), но стала {basket.get_shipping_cost}"
    assert (
        basket.get_price == extreme_price
    ), f"Итоговая стоимость должна равняться цене товара {extreme_price} у.е., но стала {basket.get_price}"


# Негативные тесты
@pytest.mark.parametrize("price, weight", [(0, 1), (1, 0), (0, 0)])
def test_invalid_product_creation(price: int, weight: int):
    """Тест создания товара с некорректными параметрами."""
    with pytest.raises(
        ValueError,
        match="Цена товара должна быть не меньше 1 у.е.|Вес товара должен быть не меньше 1 у.е.",
    ):
        Product("Бракованный товар", price, weight)


@pytest.mark.parametrize(
    "invalid_price, invalid_weight",
    [("1000", 5), (1000, "5"), (None, 10), (200, None), ([], 5), (100, {})],
)
def test_invalid_data_types(invalid_price: Any, invalid_weight: Any):
    """Тест передачи некорректных типов данных при создании товара."""
    with pytest.raises(TypeError, match=".*"):
        Product("Некорректный товар", invalid_price, invalid_weight)


def test_add_zero_products(basket):
    """Тест добавления 0 товаров в корзину."""
    product = Product("Электрочайник", 100, 3)

    with pytest.raises(
        TypeError, match="Ожидалось положительное целое число, но получено int"
    ):
        basket.add_product(product, 0)


def test_negative_quantity(basket):
    """Тест добавления отрицательного количества товара."""
    product = Product("Айфон", 700, 5)
    with pytest.raises(TypeError, match="Ожидалось положительное целое число"):
        basket.add_product(product, -3)


@pytest.mark.parametrize(
    "invalid_product, invalid_quantity",
    [
        ("Телевизор", 2),
        ([], 1),
        (Product("Чайник", 300, 3), "два"),
        (Product("Ноутбук", 1200, 5), None),
        (Product("Флешка", 100, 1), {}),
    ],
)
def test_invalid_data_in_basket_methods(
    basket, invalid_product: Any, invalid_quantity: Union[int, Any]
):
    """Тест передачи некорректных типов данных в методы корзины."""
    with pytest.raises(TypeError, match=".*"):
        basket.add_product(invalid_product, invalid_quantity)


def test_delete_nonexistent_product(basket):
    """Тест удаления несуществующего товара."""
    basket.delete_product(999)

    assert (
        len(basket.list_products) == 0
    ), f"Корзина должна быть пустой, но содержит {len(basket.list_products)} товаров"


def test_delete_product_invalid_type(basket):
    """Тест удаления товара с некорректным типом идентификатора.
    Поскольку метод delete_product не выполняет проверку типа, ожидается, что корзина останется неизменной.
    """
    product = Product("Аэрогриль", 100, 1)
    basket.add_product(product)
    count_before = len(basket.list_products)
    basket.delete_product("invalid_id")
    assert (
        len(basket.list_products) == count_before
    ), "При передаче некорректного типа идентификатора корзина не должна измениться"


@pytest.mark.parametrize("invalid_key", [1.5, (1,)])
def test_delete_product_invalid_hashable_key(basket, invalid_key: Hashable):
    """Тест удаления товара с нецелочисленными, но hashable идентификаторами.

    1. В корзину добавляется товар.
    2. Вызывается `delete_product()` с `float` или `tuple` в качестве ключа.
    3. Проверяется, что корзина остаётся неизменной, так как:
       - Метод `delete_product()` должен игнорировать некорректные ключи без исключений.
       - Количество товаров в корзине не должно измениться.
    """
    product = Product("Фен", 100, 10)
    basket.add_product(product)
    count_before = len(basket.list_products)

    basket.delete_product(invalid_key)

    assert len(basket.list_products) == count_before, (
        f"Корзина должна оставаться неизменной при удалении с нецелочисленным ключом, "
        f"но количество товаров изменилось с {count_before} до {len(basket.list_products)}"
    )


@pytest.mark.parametrize("invalid_key", [[1], {1: "a"}])
def test_delete_product_invalid_unhashable_key(basket, invalid_key: Any):
    """Тест удаления товара с unhashable (некорректными) идентификаторами.

    1. В корзину добавляется товар.
    2. Вызывается `delete_product()` с `list` или `dict` в качестве ключа.
    3. Проверяется, что:
       - Метод `delete_product()` выбрасывает `TypeError`.
       - Корзина остаётся неизменной после выброса исключения.
    """
    product = Product("Холодильник", 100, 10)
    basket.add_product(product)
    count_before = len(basket.list_products)

    with pytest.raises(TypeError, match=".*"):
        basket.delete_product(invalid_key)

    assert len(basket.list_products) == count_before, (
        f"Корзина должна оставаться неизменной при попытке удаления с unhashable ключом, "
        f"но количество товаров изменилось с {count_before} до {len(basket.list_products)}"
    )
