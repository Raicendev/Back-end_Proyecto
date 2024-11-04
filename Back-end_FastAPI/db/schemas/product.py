
### Product schema ###

def product_schema(product) -> dict:
    return {
        "id": str(product["_id"]),
        "id_producto": product["id_producto"],
        "nombre": product["nombre"],
        "descripcion": product["descripcion"],
        "precio": product["precio"],
        "categoria": product["categoria"],
        "stock": product["stock"]
    }

def products_schema(products) -> list:
    return [product_schema(product) for product in products]