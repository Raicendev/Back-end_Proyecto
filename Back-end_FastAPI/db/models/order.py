from pydantic import BaseModel

class Order(BaseModel):
    id: str | None
    username: str
    id_product: str
