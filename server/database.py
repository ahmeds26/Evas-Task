from pymongo import MongoClient
from dotenv import dotenv_values
import urllib.parse



config = dotenv_values(".env")


mongodb_client = MongoClient(config["ATLAS_URI"])
mongo_database = mongodb_client[config["DB_NAME"]]
print(f">>>> Connected to the {config['DB_NAME']} database!")
items_collection = mongo_database[config['DB_COLLECTION']]
terms_collection = mongo_database[config['DB_TERMS_COLLECTION']]
terms_collection.insert_one({'terms': dict()})


def item_helper(item) -> dict:
    return {
        "id": str(item["_id"]),
        "product_name": item["product_name"],
        "price": item["price"],
        "location": item["location"],
        "listed_date": item["listed_date"],
        "product_link": item["product_link"],
        "product_image": item["product_image"],
        "product_search_term": item["product_search_term"]
    }

# Retrieve all items present in the database    
async def retrieve_items(search_term: str) -> list:
    items = []
    for item in items_collection.find({'product_search_term': search_term}):
        items.append(item_helper(item))
    return items
    
    
# Add a new item into to the database
async def add_items(items_data: list, search_term: str) -> list:
    items = items_collection.insert_many(items_data)
    new_items = await retrieve_items(search_term)
    return new_items
    
# Add a new search term into to the database
async def add_search_term(search_term_data: dict) -> dict:
    term = terms_collection.update_one(terms_collection.find_one({}),{"$set":{"terms": {**terms_collection.find_one({})['terms'], **search_term_data}}})
    return True
    
    
