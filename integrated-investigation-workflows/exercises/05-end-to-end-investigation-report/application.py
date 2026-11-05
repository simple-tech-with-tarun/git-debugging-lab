def calculate_shipping(weight, distance):
    weight_cost = weight * 1.5
    distance_cost = distance * 0.25
    return weight_cost + distance_cost


def calculate_order_total(price, quantity, weight, distance):
    subtotal = price * quantity
    shipping = calculate_shipping(weight, distance)
    return round(subtotal + shipping, 2)

