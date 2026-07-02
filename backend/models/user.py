from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    full_name: str
    username: str
    hashed_password: str
    created_at: str

