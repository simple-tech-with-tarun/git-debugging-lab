def apply_discount(total, discount):
    discount_amount = discount * total
    return total - discount_amount


def format_invoice(total):
    return f"Invoice total: ${total:.2f}"


def calculate_total(price, quantity):
    return  price * quantity


def process_order(price, quantity, discount):
    total = calculate_total(price, quantity)
    discounted_total = apply_discount(total, discount)
    return format_invoice(discounted_total)
