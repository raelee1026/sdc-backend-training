from fastapi import FastAPI, Path, Query
from pydantic import BaseModel
from typing import Union
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
async def get_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result