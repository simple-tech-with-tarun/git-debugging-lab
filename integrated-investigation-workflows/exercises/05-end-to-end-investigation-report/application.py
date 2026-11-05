from shipping_utils import estimate_shipping


def calculate_tax(amount, tax_rate):
    return amount * tax_rate


def calculate_order_total(price, quantity, weight, distance, tax_rate=0):
    subtotal = price * quantity
    shipping = estimate_shipping(weight, distance)
    taxable_total = subtotal + shipping
    tax = calculate_tax(taxable_total, tax_rate)
    return round(taxable_total + tax, 2)
