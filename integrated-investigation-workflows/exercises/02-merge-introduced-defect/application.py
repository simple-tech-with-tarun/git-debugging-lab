def calculate_subtotal(price, quantity):
    return price * quantity


def apply_discount(subtotal, discount):
    return subtotal * (1 - discount)


def calculate_order_total(price, quantity, discount):
    subtotal = calculate_subtotal(price, quantity)
    return apply_discount(subtotal, discount)

