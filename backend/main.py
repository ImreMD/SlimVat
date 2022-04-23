from fastapi import Depends, FastAPI, HTTPException, status

from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from model import Invoice, User, UserInDB, fake_users_db

from database import (
    fetch_one_invoice,
    fetch_all_invoices,
    create_invoice,
    update_invoice,
    remove_invoice
)
#------------------------------------------------------------------------------------#

#App Object############################
app = FastAPI()
#######################################

#oauth scheme #########################
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
########################################

#Origins CORS###########################
origins = ["http://localhost:3000",
           "http://127.0.0.1:3000",
           "http://localhost:8000",
           "http://localhost"]

app.add_middleware( 
                    CORSMiddleware, 
                    allow_origins = origins, 
                    allow_credentials = True, 
                    allow_methods = ["*"], 
                    allow_headers= ["*"]
                    )
##########################################

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hashed(password):
    return pwd_context.hash(password)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

#User identifier utilities################
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user
    

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def fake_hash_password(password: str):
    return "fakehashed" + password
###########################################

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}



@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/")
def read_root(token: str = Depends(oauth2_scheme)):
    return {'data':{'name': 'Kabook'}}

@app.get("/api/invoices")
async def get_invoice():
    response = await fetch_all_invoices()
    return response

@app.get("/api/invoice{invoice_nbr}", response_model=Invoice)
async def get_invoice_by_id(invoice_nbr):
    response = await fetch_one_invoice(invoice_nbr)
    if response:
        return response
    raise HTTPException(404, f"There is no invioce with this title {invoice_nbr}")

@app.post("/api/invoice", response_model = Invoice)
async def post_invoice(invoice: Invoice):
    response = await create_invoice(invoice.dict())
    if response:
        return response
    raise HTTPException(400, f"Something went wrong / Bad request")

@app.put("/api/invoice{invoice_nbr}", response_model = Invoice)
async def put_invoice(invoice_nbr: str, desc: str, cust: str, vat_st: str):
    response = await update_invoice(invoice_nbr, desc, cust, vat_st)
    if response:
        return response
    raise HTTPException(404, f"There is no TODO with this title {invoice_nbr}")

@app.delete("/api/todo/{invoice_nbr}")
async def delete_invoice(invoice_nbr):
    response = await remove_invoice(invoice_nbr)
    if response:
        return response
    raise HTTPException(404, f"There is no TODO with this title {invoice_nbr}")