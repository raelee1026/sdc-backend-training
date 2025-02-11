from fastapi import FastAPI, Path, Query, HTTPException
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
async def update_item(
    item: Item,
    item_id: int = Path(..., ge=1, le=1000), 
    q: str | None = Query(default=None, min_length=3, max_length=50)
):
    if q is not None and (len(q) < 3 or len(q) > 50):
        raise HTTPException(
            status_code=422,
            detail="Query 'q' must be between 3 and 50 characters."
        )
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result

@app.get("/items/{item_id}")
async def get_item(
    item_id: int = Path(..., ge=1, le=1000),
    q: str | None = Query(default=None, min_length=3, max_length=50),
    sort_order: str = Query(default="asc", regex="^(asc|desc)$")
):
    if q is not None and (len(q) < 3 or len(q) > 50):
        raise HTTPException(
            status_code=422,
            detail="Query 'q' must be between 3 and 50 characters."
        )
    if item_id < 1 or item_id > 1000:
        raise HTTPException(
            status_code=422,
            detail="Item ID must be between 1 and 1000."
        )
    description = "This is a sample item."
    if q:
        description = f"This is a sample item that matches the query {q}."
    return {
        "item_id": item_id,
        "description": description,
        "sort_order": sort_order
    }