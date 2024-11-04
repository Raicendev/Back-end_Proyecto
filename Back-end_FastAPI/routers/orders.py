from fastapi import APIRouter, HTTPException, status
from db.models.order import Order
from db.schemas.order import order_schema, orders_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/orders",
                   tags=["orders"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})


### Funciones de visualización:

@router.get("/", response_model=list[Order])
async def orders():

    return orders_schema(db_client.orders.find())


@router.get("/{id}")
async def order_id(id: str):
    
    return search_order("_id", ObjectId(id))




### Funciones adicionales:

def search_order(field: str, key):

    try:
        order = db_client.orders.find_one({field: key})
        return Order(**order_schema(order))
    except:
        return {"Error": "Order not found."}

#{"id":"66522d493825ddee0bacfd10", "cod_order": 1,"username": "juanjo", "id_product": "6650f5a5d0a7edc8607519b1"}