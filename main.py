from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel
from typing import Union, Annotated
from enum import Enum

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
async def update_item(item_id: Annotated[int,Path(gt=0,le=1000)], 
                   item: Item, 
                   q: Annotated[str | None, Query(min_length=3, max_length = 50)] = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})

@app.get("/items/{item_id}")
async def read_item(item_id: Annotated[int,Path(gt=0, le=1000)], 
                        q: Annotated[str | None, Query(min_length=3, max_length = 50)] = None,
                        sort_order: str = Query(default="asc", pattern="^(asc|desc)$")):
    result = {"item_id": item_id}
    if q:
        result.update({"description": "This is a sample item that matches the query test_query"})
    else:
        result.update({"description": "This is a sample item."})
    result.update({"sort_order":sort_order})
    return result