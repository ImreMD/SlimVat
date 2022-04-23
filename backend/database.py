from model import Invoice
from attr import asdict
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
database = client.SlimVat
collection = database.Invoices

async def fetch_one_invoice(invoice_nbr):
    document = await collection.find_one({"invoice_nbr": invoice_nbr})
    return document

async def fetch_all_invoices():
    todos = []
    cursor = collection.find({})
    async for document in cursor:
        todos.append(Invoice(**document))
    return todos

async def create_invoice(Invoice):
    print(f'todo_dict : {Invoice}')
    document = Invoice
    result = await collection.insert_one(document)
    print(f'result :{result}')
    return result

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



