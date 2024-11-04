from fastapi import APIRouter, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId
from pydantic import BaseModel


router = APIRouter(prefix="/users",
                   tags=["users"],
                   responses={status.HTTP_404_NOT_FOUND: {"Message": "Not found."}})

### Funciones de visualización:

@router.get("/{id}")
async def user_id(id: str):
    
    return search_db("_id", ObjectId(id))


@router.get("/", response_model=list[User])
async def users():

    return users_schema(db_client.users.find())



### Funciones adicionales:

def search_db(field: str, key):

    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"Error": "User not found."}


#{"id":"", "username": "juanjo", "password": "$2a$12$HK73aLtJQ0Go82dN4k1zIO477jvYGAWj8oaquFDqJ1kp9mp541A9S", "email": "juanjo@localhost.com", "is_admin": false}