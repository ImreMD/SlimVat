import asyncio
from database import fetch_all_invoices, remove_invoice 

def test_database():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(fetch_all_invoices())
    loop.close()
    return result

def test_delete(title):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(remove_invoice(title))
    loop.close()
    return result

#a = test_delete("cdasv")