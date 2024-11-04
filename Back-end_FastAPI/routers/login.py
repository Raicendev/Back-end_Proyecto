### Librerias importadas:

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from db.models.user import User, Userdb
from db.models.product import Product
from db.models.order import Order
from db.schemas.user import user_schema
from db.schemas.product import product_schema
from db.schemas.order import order_schema, orders_schema
from db.client import db_client
from bson import ObjectId
from pydantic import BaseModel




### Variables:

ALGORITHM  = "HS256"
ACCESS_TOKEN_DURATION = 60
SECRET = "286844f15f8921d7d03843e2fcf6d557d91546cf2ce33b86d5a1057f9beb304f"
oauth2 = OAuth2PasswordBearer(tokenUrl="/login")
crypt = CryptContext(schemes=["bcrypt"])
exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
            headers={"WWW-Authenticate": "Bearer"})
router = APIRouter(tags=["login"],
                   responses={status.HTTP_404_NOT_FOUND: {"Message": "Not found"}})




### Funciones de autenticación:

async def auth_user(token: str = Depends(oauth2)):

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
    
    except JWTError:
        raise exception
    
    return search_user(username)


async def current_user(user: User = Depends(auth_user)):

    return user




### Registro:

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):

    user_db = search_user(form.username)

    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user is not registered.")
    
    user = search_user(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password.")
    

    access_token = {"sub": user.username,
                    "exp": datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_DURATION)}

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}




### Función de muestra de pedidos propios:

@router.get("/orders/me")
async def order(user: User = Depends(current_user)):

    list_order = []
    lista_save = orders_schema(db_client.orders.find())

    for i in lista_save:

        if i.username == user.username:
            list_order.append(i)
    
    if list_order.len == 0:
        return {"Message": "You don't have any order."}
    
    return list_order


### Funciones de añadido verificando la autenticación:

@router.post("/user", status_code=status.HTTP_201_CREATED)
async def user(user: User, users: User = Depends(current_user)):

    if users.is_admin:

        if type(search_db("email", user.email)) == User:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User already exists.")

        user_dict = dict(user)
        del user_dict["id"]

        id = db_client.users.insert_one(user_dict).inserted_id

        new_user = user_schema(db_client.users.find_one({"_id": id}))

        return User(**new_user) 
    
    else:

        return {"Message": "Invalid credentials."}


@router.post("/product", status_code=status.HTTP_201_CREATED)
async def user(product: Product, user: User = Depends(current_user)):

    if user.is_admin:

        if type(search_product("id_producto", product.id_producto)) == Product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="The product is already registered.")

        product_dict = dict(product)
        del product_dict["id"]

        id= db_client.products.insert_one(product_dict).inserted_id

        new_product = product_schema(db_client.products.find_one({"_id": id}))

        return Product(**new_product)
    
    else:

        return {"Message": "Invalid credentials."}


@router.get("/order/{id}", status_code=status.HTTP_201_CREATED)
async def order(id: str, user: User = Depends(current_user)):
    
    id_producto = id

    username = user.username
    
    pedido = {"id": "", "username": username, "id_producto": id_producto}

    order_dict = dict(pedido)
    del order_dict["id"]

    id = db_client.orders.insert_one(order_dict).inserted_id

    new_order = db_client.orders.find_one({"_id": id})

    return Order(**order_schema(new_order))
 




### Funciones de modificación con autenticación:

@router.put("/user")
async def user(user: User, users: User = Depends(current_user)):

    if type(search_db("email", user.email)) == Product or users.is_admin:

        user_dict = dict(user)
        del user_dict["id"]

        try:
            db_client.users.find_one_and_replace(
                {"_id": ObjectId(user.id)}, user_dict)

        except:
            return {"Error": "It is not possible to update the user."}

        return search_db("_id", ObjectId(user.id))
    
    else:

        return {"Message": "You can only modify your username"}
    

@router.put("/product")
async def product(product: Product, user: User = Depends(current_user)):

    if user.is_admin:

        product_dict = dict(product)
        del product_dict["id"]

        try:
            db_client.products.find_one_and_replace(
                {"_id": ObjectId(product.id)}, product_dict)
        except:
            return {"Error": "The product has not been modified."}

        return search_product("_id", ObjectId(product.id))

    else:

        return {"Message": "Invalid credentials."}

@router.put("/productdb/stock")
async def product(product: Product, user: User = Depends(current_user)):

    if user.is_admin:
        product_dict = dict(product)
        del product_dict["id"]

        try:
            db_client.products.find_one_and_replace(
                {"_id": ObjectId(product.id)}, product_dict)
        except:
            return {"Error": "Stock could not be updated."}

        return search_product("_id", ObjectId(product.id))
    
    else:

        return {"Message": "Invalid credentials."}


@router.put("/order")
async def order(order: Order, user: User = Depends(current_user)):

    busqueda = search_order("username", order.username)
    if not type(busqueda) == Order:
        return{"Message": "This user does not have any orders"} 

    if busqueda.username == user.username or user.is_admin:

        order_dict = dict(order)
        del order_dict["id"]

        try:
            db_client.orders.find_one_and_replace(
                {"_id": ObjectId(order.id)}, order_dict)

        except:
            return {"Error": "It is not possible to update the order."}

        return search_order("_id", ObjectId(order.id))


    else:

        return {"Message": "You do not own this order."}





### Funciones de eliminación con autenticación:

@router.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str, user: User = Depends(current_user)):

    if user.is_admin:
        found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})


        if not found:
            return {"Error": "The user could not be deleted."}
        
        return {"Message": "User successfully deleted."}
    else:

        return {"Message": "Invalid credentials."}
    

@router.delete("/productdb/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def product(id: str, user: User = Depends(current_user)):

    if user.is_admin:

        found = db_client.products.find_one_and_delete({"_id": ObjectId(id)})

        if not found:
            return {"Error": "Product has not been removed"}
        
        return {"Message": "Product successfully deleted."}
    
    else:

        return {"Message": "Invalid credentials."}


@router.delete("/productdb/categoria/eliminar/{categoria}", status_code=status.HTTP_204_NO_CONTENT)
async def product(categoria: str, user: User = Depends(current_user)):
        
    if user.is_admin:

        found = db_client.products.delete_many({"categoria": categoria})
    
        if not found:
            return {"error": "The category has not been deleted."}
        
        return {"Message": "The category has been successfully deleted."}
        
    else:

        return {"Message": "Invalid credentials."}


@router.delete("/order/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str, user: User = Depends(current_user)):

    busqueda = search_order("_id", ObjectId(id))

    if not type(busqueda) == Order:
        return {"Message": "this request does not exist"}

    if busqueda.username == user.username or user.is_admin:

        found = db_client.orders.find_one_and_delete({"_id": ObjectId(id)})


        if not found:
            return {"Error": "The order could not be deleted."}
        
        return {"Message": "Order successfully deleted."}

    else:

        return {"Message": "You do not own this order."}    


### Funciones adicionales:

def search_db(field: str, key):

    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"Message": "User not found."}


def search_user(username: str):
    try:
        user = db_client.users.find_one({"username": username})
        return User(**user_schema(user))
    except:
        return {"Message": "User not found"}

def search_userdb(username: str):
    try:
        user = db_client.users.find_one({"username": username})
        return Userdb(**user_schema(user))
    except:
        return {"Message": "User not found"}

def search_product(field: str, key):

    try:
        product = db_client.products.find_one({field: key})
        return Product(**product_schema(product))
    except:
        return {"Error": "Product not found."}

def search_order(field: str, key):

    try:
        order = db_client.orders.find_one({field: key})
        return Order(**order_schema(order))
    except:
        return {"Error": "Order not found."}