def calculate_discount_amount(total, discount):
    return (discount / 100) * total


def apply_discount(total, discount):
    if not 0 <= discount <= 1:
        raise ValueError("Discount must be between 0 and 1")

    discount_amount = calculate_discount_amount(total, discount)
    return total - discount_amount


def format_invoice(total):
    return f"Invoice total: ${total:.2f}"


def calculate_total(price, quantity):
    return price * quantity


def process_order(price, quantity, discount):
    total = calculate_total(price, quantity)
    discounted_total = apply_discount(total, discount)
    return format_invoice(discounted_total)
