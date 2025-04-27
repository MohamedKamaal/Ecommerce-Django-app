import pytest
from orders.tests.factories import OrderFactory, OrderItemFactory, UserFactory, ProductVariationFactory
from orders.models import Order, OrderItem

@pytest.mark.django_db
def test_order_creation():
    user = UserFactory()
    shipping_info = user.shippinginfo_set.create(first_name='Jane', last_name='Doe', address='456 Another St', email='jane.doe@example.com')
    order = OrderFactory(user=user, shipping_info=shipping_info)

    assert order.user == user
    assert order.shipping_info == shipping_info
    assert order.status == 'pending'
    assert order.total_cents > 0

@pytest.mark.django_db
def test_order_item_creation():
    order = OrderFactory()
    product = ProductVariationFactory()
    order_item = OrderItemFactory(order=order, product=product)

    assert order_item.order == order
    assert order_item.product == product
    assert order_item.quantity > 0
    assert order_item.total_cents == order_item.product.price_cents * order_item.quantity

@pytest.mark.django_db
def test_total_property():
    order = OrderFactory(total_cents=5000)  # $50.00
    assert order.total == 50.00

    order_item = OrderItemFactory(quantity=3, total_cents=3000)  # $30.00 for 3 items
    assert order_item.total == 30.00
