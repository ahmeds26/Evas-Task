import uuid
from typing import Optional
from pydantic import BaseModel, Field


class ItemSchema(BaseModel):
    product_name: str = Field(...)
    price: str = Field(...)
    location: str = Field(...)
    listed_date: str = Field(...)
    product_link: str = Field(...)
    product_image: str = Field(...)
    product_search_term: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "product_name": "product 1",
                "price": "1,500",
                "location": "cairo, eg",
                "listed_date": "2 days ago",
                "product_link": "product link page",
                "product_image": "product image link",
                "product_search_term": "search term"
            }
        }


class UpdateItemModel(BaseModel):
    product_name: Optional[str]
    price: Optional[str]
    location: Optional[str]
    listed_date: Optional[str]
    product_link: Optional[str]
    product_image: Optional[str]
    product_search_term: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "product_name": "product 1",
                "price": "1,500",
                "location": "cairo, eg",
                "listed_date": "2 days ago",
                "product_link": "product link page",
                "product_image": "product image link",
                "product_search_term": "search term"
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
