from fastapi import FastAPI, Path, Query, Body, Cookie
from pydantic import BaseModel
from typing import Union, Annotated
from enum import Enum
from datetime import datetime, timedelta

class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.put("/items/{item_id}")
async def put_item(item_id: Annotated[int, Path(ge=1, le=1000)], 
                    q: Annotated[str|None, Query(max_length=50, min_length=3)] = None,
                    item: Item = None):
    res = {"item_id": item_id, **item.model_dump()}
    if q:
        return {**res, "q": q}
    else :
        return res

@app.get("/items/{item_id}")
async def get_item(
    item_id: Annotated[int, Path(ge=1, le=1000)], 
    q: Annotated[str|None, Query(max_length=50, min_length=3)] = None, 
    sort_order: str = Query(default="asc", pattern="^(asc|desc)$")
):
    if q:
        return {
            "item_id": item_id, 
            "description": "This is a sample item that matches the query test_query",
            "sort_order": sort_order
        }
    else:
        return {
            "item_id": item_id,
            "description": "This is a sample item.",
            "sort_order": sort_order
        }
    
@app.post("/items/filter/")
async def filter_items(
    price_min: int,
    price_max: int,
    tax_included: bool ,
    tags: list[str] = Query(None),
):
    return {"price_range": [price_min, price_max], 
            "tax_included": tax_included, 
            "tags": tags,
            "message": "This is a filtered list of items based on the provided criteria."}

@app.post("/items/create_with_fields/")
async def create_item_with_fields(
    item: Item, 
    importance: Annotated[int, Body()],
):
    return {"item": item, "importance": importance}

@app.post("/offers/")
async def create_offer(
    name: Annotated[str, Body()],
    discount: Annotated[float, Body()], 
    items: Annotated[list[Item], Body()],
):
    return {"offer_name": name, "discount": discount, "items": items}

@app.post("/users/")
async def create_user(
    username: Annotated[str, Body()],
    email: Annotated[str, Body()],
    full_name: Annotated[str, Body()],
):
    return {"username": username, "email": email, "full_name": full_name}

@app.post("/items/extra_data_types/")
async def create_item_with_extra_data(
    start_time: Annotated[datetime, Body()], # Start time of the item's availability.
    end_time: Annotated[str, Body()], # End time of the item's availability.
    repeat_every: Annotated[timedelta, Body()], # Time interval for repeating the item.
    process_id: Annotated[str, Body()], # Unique identifier for the process.
):
    return {
            "message": "This is an item with extra data types.", 
            "process_id": process_id
    }

@app.get("/items/cookies/")
async def read_items_from_cookies(
    session_id: Annotated[str, Cookie()], # Session ID from the client's cookies.
):
    return {
        "session_id": session_id, 
        "message": "This is the session ID obtained from the cookies."
    }


