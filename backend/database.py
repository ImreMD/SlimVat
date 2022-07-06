from model import Invoice, fake_invoices_db
from attr import asdict
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
database = client.SlimVat
collection = database.Invoices

async def fetch_one_invoice(invoice_nbr):
    document = await collection.find_one({"invoice_nbr": invoice_nbr})
    return document

async def fetch_users_invoices(customer_klas2):
    n = await collection.count_documents({})
    invoices = [d for d in fake_invoices_db if d['customer'] == customer_klas2]
    cursor = collection.find({"customer": "ZIKO"}, {"_id":0})
    all_invoices = await cursor.to_list(length=n)
    #print(f'all invoices for {customer_klas2} : {all_invoices[:2]}')
    #for document in await cursor.to_list(length=n):
        #print(document)
    return invoices, all_invoices #all_invoices #invoices

async def fetch_all_invoices():
    todos = []
    cursor = collection.find({})
    async for document in cursor:
        todos.append(Invoice(**document))
    return todos

async def insert_invoice(Invoice):
    #print(f'invoice_dict : {Invoice}')
    document = Invoice
    result = await collection.insert_one(document)
    response_dict = {'acknowledged':result.acknowledged, 
                    'inserted_id':str(result.inserted_id)}
    print(f'invoice inserted:{result.acknowledged} with id: {result.inserted_id}')
    return response_dict 
    #returned to main.py

async def update_invoice(inv_nbr, desc, cust, vat_st):
    await collection.update_one({"invoice_nbr": inv_nbr},
                                {"$set":{"description": desc}},
                                {"$set":{"customer": cust}},
                                {"$set":{"vat_status": vat_st}})
    document = await collection.find_one({"invoice_nbr": inv_nbr})
    return document

async def remove_invoice(inv_nbr):
    #occurance = await collection.count_documents({"title": title})
    print(f"inside_remove : {inv_nbr}")
    result = await collection.delete_one({"title": inv_nbr})
    return result.deleted_count



