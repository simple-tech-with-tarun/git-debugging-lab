def estimate_shipping_cost(weight, distance):
    base_cost = weight * 2
    distance_cost = distance * 0.5
    return base_cost + distance_cost
