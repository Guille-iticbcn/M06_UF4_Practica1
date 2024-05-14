from typing import Union
from typing import List
from fastapi import FastAPI
import product_db

from pydantic import BaseModel

app = FastAPI()

class product(BaseModel):
    name:str
    description:str
    company:str
    price:float
    units:int
    subcategory_id:int


@app.get("/product", response_model=List[dict])
def read_product():
    return product_db.products_schema(product_db.read())


@app.get("/product_id/{id}")
def read_product(id: int, q:Union[str, None] = None):
    return {"product_id": id, "Body": q}


@app.post("/create_product")
async def create_product(data:product):
    name = data.name
    description = data.description
    company = data.company
    price = data.price
    units = data.units
    subcategory_id = data.subcategory_id
    l_product_id = product_db.create(name, description, company, price, units, subcategory_id)
    return {
        "msg": "S’ha afegit correctement",
        "id product": l_product_id,
        "name": name
    }


@app.put("/update_product/{product_id}")
def update_product(units:int, product_id:int):
    product_db.update_product(units, product_id)


@app.delete("/delete_product/{id}")
def delete_product(id:int):
    product_db.delete_product(id)