from datetime import datetime, timedelta
from http.client import responses
from typing import List, Optional, List

from fastapi import Depends, FastAPI, HTTPException, status, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

#Oauth2 & hash ############################################
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
#JWT ######################################################
from jose import JWTError, jwt



#Internal import###########################################
from model import Invoice, User, UserInDB, fake_users_db, fake_invoices_db, Token, TokenData
from database import (
    fetch_user,
    fetch_one_invoice,
    fetch_all_invoices,
    fetch_users_invoices,
    insert_invoice,
    update_invoice,
    update_invoices,
    remove_invoice
)
#------------------------------------------------------------------------------------#

#App Object############################
app = FastAPI()
#######################################

#oauth scheme & JWT #########################
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

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


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hashed(password):
    return pwd_context.hash(password)



#User identifier utilities################

async def authenticate_user(username: str, password: str):
    user = User(**(await fetch_user(username)))
    
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        #check where token expiration checked?
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def fake_hash_password(password: str):
    return "fakehashed" + password
###########################################

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



# End points###############################

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()): #: OAuth2PasswordRequestForm = Depends()):
    #return user ot not user
    print(f'payload username: {form_data.username} payload password: {form_data.password}')
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    #creates token
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    json_compatible_item_data = jsonable_encoder({"access_token": access_token, "token_type": "Bearer"})
    print(json_compatible_item_data)
    return JSONResponse(content=json_compatible_item_data)


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/token/check/")
async def get_token_info(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    expires: str = payload.get("exp")
    expiry_date:str = datetime.utcfromtimestamp(expires)
    return {"user": username, "token" : token, "expiry token": expiry_date}

@app.get("/api/invoices")#, response_model= List(Invoice))
async def get_invoice(current_user: User = Depends(get_current_active_user)):
    response, responses =  await fetch_users_invoices(current_user.customer_repr)
    #print(responses)
    return  responses

@app.get("/api/invoice{invoice_nbr}", response_model=Invoice)
async def get_invoice_by_id(invoice_nbr):
    response = await fetch_one_invoice(invoice_nbr)
    if response:
        return response
    raise HTTPException(404, f"There is no invioce with this title {invoice_nbr}")

@app.post("/api/invoice") #no response_model, response_model = Invoice)
async def post_invoice(invoice: Invoice):
    response = await insert_invoice(invoice.dict())
    #response from database.py  b:create_invoice_return
    print(f'record inserted: {response["acknowledged"]}')
    if response["acknowledged"]:
        return response["inserted_id"]
    raise HTTPException(400, f"Something went wrong / Bad request")

@app.put("/api/invoices") 
async def put_invoices(invoices = Body(default=None)):
    print(f'body is : {invoices["invoices_send"]}')
    await update_invoices(invoices["invoices_send"])
    return {'response':'invoices received'}

@app.put("/api/invoice{invoice_nbr}") #no response_model, response_model = Invoice)
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