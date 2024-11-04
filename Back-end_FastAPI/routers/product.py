### Product DB API ###

from fastapi import APIRouter, HTTPException, status
from db.models.product import Product
from db.schemas.product import product_schema, products_schema
from db.client import db_client
from bson import ObjectId
from pydantic import BaseModel



router = APIRouter(prefix="/productdb",
                   tags=["productdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})
 
### Endpoint Listar Productos ###

@router.get("/", response_model=list[Product])
async def products():
    return products_schema(db_client.products.find())


### Endpoint Buscar Producto Por ID ###

@router.get("/{id}") 
async def product(id: str):
    return search_product("_id", ObjectId(id))


### Endpoint Buscar Producto Por Nombre ###

@router.get("/buscar/{nombre}") 
async def product(nombre: str):
    return search_product("nombre", nombre)  

### Endpoint Lista Productos ordenados por precio ###  

@router.get("/orden/ordenar", response_model=list[Product])
async def products(ordenar: str):

    if ordenar == "ordenar":
       
        products = db_client.products.find().sort("precio", -1)

    return products_schema(products)
   
    
### Endpoint Lista Productos Por Categoria ###


@router.get("/buscar/categoria/{categoria}") 
async def product(categoria: str):

    
    return search_category("categoria", categoria)


### Endpoint Lista Productos ordenados por precio ###  

@router.get("/orden/ordenar", response_model=list[Product])
async def products(ordenar: str):

    if ordenar == "ordenar":
       
        products = db_client.products.find().sort("precio", -1)

    return products_schema(products)


'''
@router.patch("/stock/{id_producto}", response_model = Product)
async def actualizar_stock(id_producto: str, product: Product):
    stored_item_data = product[id_producto]
    stored_item_model = Product(**stored_item_data)
    update_data = product.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    
    return updated_item'''
      

## funcion buscar producto

def search_product(field: str, key):

    try:
        product = db_client.products.find_one({field: key})
        return Product(**product_schema(product))
    except:
        return {"error": "No se ha encontrado el producto"}
    

def search_category(field: str, key) -> list:
  
    try:
        products = db_client.products.find({field: key})
        return [product_schema(product) for product in products]
    except:
        return {"error": "No se ha encontrado el producto"}

    #{"id": "5", "id_producto": 5,"nombre": "camiseta de calidad", "descripcion": "azul y verde", "precio": 30, "categoria":"ropa", "stock": 120}



