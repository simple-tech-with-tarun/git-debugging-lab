from shipping_utils import estimate_shipping_cost


def calculate_order_total(price, quantity):
    return price * quantity


def process_shipment(weight, distance):
    return estimate_shipping_cost(weight, distance)