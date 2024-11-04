# Importamos lo que vamos a necesitar.
from fastapi import FastAPI, status, HTTPException
from routers import login, users, product, orders
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema


# Se define variable que almacenara el FastAPI.
app = FastAPI()


app.include_router(login.router)
app.include_router(users.router)
app.include_router(product.router)
app.include_router(orders.router)

# EndPoint de entrada en la API.
@app.get("/")
async def root():
    return {"Welcome to FastAPI": "Magnificent Project!, A Store with Products and Users. Developed by Juan Jose Barroso Hidalgo and Rafael Centella Guijarro."}



### Registrar nuevo usuario:

@app.get("/register", response_model= User, status_code=status.HTTP_202_ACCEPTED)
async def registro():

    id = ""
    username = input("Enter your username: ")
    password = input("Enter your previously encrypted password on this website (https://bcrypt-generator.com/): ")
    email = input("Enter your email: ")

    if type(search_db("email", email)) == User:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User already exists.")
    admin = False

    user = {"id": id, "username": username, "password": password, "email": email, "is_admin": admin}

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id": id}))

    return User(**new_user)

### Funciones adicionales:

def search_db(field: str, key):

    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"Error": "User not found."}

#{"id":"6650c7e3dcd30ce988835b97", "username": "Rafa", "password": "$2a$12$HK73aLtJQ0Go82dN4k1zIO477jvYGAWj8oaquFDqJ1kp9mp541A9S", "email": "rafa@localhost.com", "is_admin": false}

