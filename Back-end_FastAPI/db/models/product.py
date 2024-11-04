### Product model ###

from pydantic import BaseModel

class Product(BaseModel):
    id: str | None
    id_producto: int
    nombre: str
    descripcion: str
    precio: float
    categoria: str
    stock: int



