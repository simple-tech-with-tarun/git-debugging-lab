def calculate_subtotal(price, quantity):
    return price * quantity


def apply_discount(subtotal, discount):
    return subtotal * (1 - discount)


def calculate_tax(subtotal, tax_rate):
    return subtotal * tax_rate


def calculate_order_total(price, quantity, discount, tax_rate=0.0):
    subtotal = calculate_subtotal(price, quantity)
    discounted_subtotal = apply_discount(subtotal, discount)
    tax = calculate_tax(discounted_subtotal, tax_rate)
    return discounted_subtotal + tax
