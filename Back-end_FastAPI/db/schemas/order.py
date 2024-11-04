
def order_schema(order) -> dict:
    return {
        "id": str(order["_id"]),
        "username": order["username"],
        "id_product": order["id_product"]}

def orders_schema(orders) -> list:
    return [order_schema(order) for order in orders]