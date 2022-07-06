from pydantic import BaseModel
from typing import Optional

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

fake_invoices_db = [
            {"invoice_nbr": "KFVR/000001/22", "description": "invoice_1", "customer":"ZIKO", "vat_status": False },
            {"invoice_nbr": "KFVR/000002/22", "description": "invoice_2", "customer":"ZIKO", "vat_status": False},
            ]

#Security class#########################

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

#User class#########################

class User(BaseModel):
    username: str
    email: str
    customer_repr: str
    disabled: bool
    hashed_password: str

class UserInDB(User):
    hashed_password: str

#Invioce class#########################

class Invoice(BaseModel):
    
    invoice_nbr: str
    description: str
    customer: str
    vat_status: bool

class Config:
    orm_mode = True
