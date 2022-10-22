from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from server.database import *
from server.models.item import (ErrorResponseModel, ResponseModel, ItemSchema, UpdateItemModel)
from server.scraper import *
from server.sendemail import *
from operator import itemgetter
import json
import os

router = APIRouter()


    
    
@router.get("/search", response_description="Items retrieved")
async def get_items(request: Request):
    query_string = request.url.query
    search_term = query_string.split('&')[0].replace('search_term=', '')
    email = query_string.split('&')[1].replace('email=', '')
    size = query_string.split('&')[-1].replace('size=', '')
    if int(size) < 20:
        return 'Invalid Size: size must be at least 20'
    
    try:
        terms_collection.find_one({})['terms']
    except TypeError:
        terms_collection.insert_one({'terms': dict()})
        
    if len(terms_collection.find_one({})['terms']) > 0:
        try:
            if terms_collection.find_one({})['terms'][search_term]:
                print(f'>>> Search term: {search_term} is already scraped before')
                items = await retrieve_items(search_term)
        except KeyError:
            browser = start_driver()
            results = scrape_items(browser, search_term)
            items = await add_items(results, search_term)
            new_search_term = await add_search_term({search_term: True})
    else:
        browser = start_driver()
        results = scrape_items(browser, search_term)
        items = await add_items(results, search_term)
        new_search_term = await add_search_term({search_term: True})
    if items:
        sample_data = items[0:int(size)]
        sorted_sample_data = sorted(sample_data, key=itemgetter('price'))
        file_name = 'sample.json'
        with open(os.path.join(os.getcwd(), file_name), "w") as final:
            json.dump(sorted_sample_data, final, indent=4)
        send_message(email, os.path.join(os.getcwd(), file_name))
        print(f">>> An Email has been sent to '{email}' with sample results")
        return ResponseModel(sorted_sample_data, "Items data retrieved successfully")
        
    return ResponseModel(items, "Empty list returned")



    
    