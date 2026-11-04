def calculate_shipping_cost(weight, distance):
    base_cost = weight * 2
    distance_cost = distance * 0.5
    return base_cost + distance_cost


def calculate_order_total(price, quantity):
    return price * quantity


def process_shipment(weight, distance):
    return calculate_shipping_cost(weight, distance)
