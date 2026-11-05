from shipping_utils import estimate_shipping


def calculate_tax(amount, tax_rate):
    return amount * tax_rate


def calculate_order_total(price, quantity, weight, distance, tax_rate=0):
    subtotal = price * quantity
    shipping = estimate_shipping(weight, distance)
    tax = calculate_tax(subtotal, tax_rate)
    return round(subtotal + shipping + tax, 2)
