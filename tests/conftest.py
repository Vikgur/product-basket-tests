import pytest

from product_basket import Basket


@pytest.fixture
def basket():
    """Фикстура для инициализации пустой корзины."""
    return Basket()
