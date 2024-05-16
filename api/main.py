from typing import Union
from typing import List
from fastapi import FastAPI
import product_db

from pydantic import BaseModel
from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app = FastAPI()
# Configuración del directorio de subida
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Creem la plantilla amb els atributs del producte.
class product(BaseModel):
    name:str
    description:str
    company:str
    price:float
    units:int
    subcategory_id:int

#Endpoint de tots el productes.
@app.get("/product", response_model=List[dict])
def read_product():
    return product_db.products_schema(product_db.read())

#Endpoint per imprimir un únic producte.
@app.get("/product_id/{id}")
def read_product(id: int, q:Union[str, None] = None):
    return {"product_id": id, "Body": q}

#Endpoint per crear un producte.
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

#Endpoint per actualitzar les unitats d'un producte per ID.
@app.put("/update_product/{product_id}")
def update_product(units:int, product_id:int):
    product_db.update_product(units, product_id)

#Endpoint per eliminar un producte.
@app.delete("/delete_product/{id}")
def delete_product(id:int):
    product_db.delete_product(id)

@app.route('/upload', methods=['POST'])
def carregaArxius():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File successfully uploaded', 'filename': filename}), 200

    return jsonify({'message': 'File upload failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)