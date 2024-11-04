from pydantic import BaseModel

class User(BaseModel):
    id: str | None
    username: str
    password: str
    email: str
    is_admin: bool

class Userdb(User):
    password: str
