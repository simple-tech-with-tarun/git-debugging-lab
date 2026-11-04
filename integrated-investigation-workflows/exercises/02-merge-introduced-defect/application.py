def calculate_subtotal(price, quantity):
    return price * quantity


def apply_discount(subtotal, discount):
    return subtotal * (1 - discount)


def calculate_tax(subtotal, tax_rate):
    return subtotal * tax_rate


def calculate_order_total(price, quantity, discount):
    subtotal = calculate_subtotal(price, quantity)
    discounted_subtotal = apply_discount(subtotal, discount)
    return discounted_subtotal
