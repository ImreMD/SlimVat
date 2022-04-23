from pydantic import BaseModel

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "customer_repr": "ZIKO",
        "disabled": False,
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
    },
    "alice": {
        "username": "alice",
        "email": "alice@example.com",
        "customer_repr": "DRMAX",
        "disabled": True,
        "hashed_password": "fakehashedsecret2",
    },
}

class User(BaseModel):
    username: str
    email: str
    customer_repr: str
    disabled: bool


class UserInDB(User):
    hashed_password: str

class Invoice(BaseModel):
    invoice_nbr: str
    description: str
    customer: str
    vat_status: bool

    class Config:
        orm_mode = True
