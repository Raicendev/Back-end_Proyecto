def user_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "is_admin": user["is_admin"],
        "password": user["password"]}

def user_schemadb(user) -> dict:
    return {
        "username": user["username"],
        "password": user["password"]}

def users_schema(users) -> list:
    return [user_schema(user) for user in users]