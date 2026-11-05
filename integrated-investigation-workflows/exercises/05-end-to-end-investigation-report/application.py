from shipping_utils import estimate_shipping


def calculate_order_total(price, quantity, weight, distance):
    subtotal = price * quantity
    shipping = estimate_shipping(weight, distance)
    return round(subtotal + shipping, 2)
