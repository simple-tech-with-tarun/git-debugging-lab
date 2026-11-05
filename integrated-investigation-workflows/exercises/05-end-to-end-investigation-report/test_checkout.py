from application import calculate_order_total


def test_order_total():
    actual = calculate_order_total(
        price=100,
        quantity=2,
        weight=2,
        distance=10,
    )

    expected = 205.50

    assert actual == expected, f"Expected {expected}, got {actual}"


if __name__ == "__main__":
    test_order_total()
    print("PASS: checkout tests are correct")
