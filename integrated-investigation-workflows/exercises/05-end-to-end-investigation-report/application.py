def calculate_shipping(weight, distance):
    weight_cost = weight * 1.5
    distance_cost = distance * 0.25
    return weight_cost + distance_cost


def calculate_tax(amount, tax_rate):
    return amount * tax_rate


def calculate_order_total(price, quantity, weight, distance, tax_rate=0):
    subtotal = price * quantity
    shipping = calculate_shipping(weight, distance)
    taxable_total = subtotal + shipping
    tax = calculate_tax(taxable_total, tax_rate)
    return round(taxable_total + tax, 2)
