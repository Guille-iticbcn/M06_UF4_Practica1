from client import db_client

def product_schema(product) -> dict:
    return {"id": product[0],
            "name": product[1],
            "description": product[2],
            "company": product[3],
            "price": product[4],
            "units": product[5],
            "subcategory": product[6]
            }

def products_schema(products) -> dict:
    return [product_schema(product) for product in products]

# Mètode per llegir els productes de la BDD.
def read():
    try:
        conn = db_client()
        cur = conn.cursor()
        cur.execute("SELECT * FROM product")
        result = cur.fetchall()
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió: {e}" }
    
    finally:
        conn.close()
    
    return result

#Mètode per crear productes.
def create (name, description, company, price, units, subcategory_id):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "INSERT into product (name, description, company, price, units, subcategory_id) VALUES (%s, %s, %s, %s, %s, %s);"
        values=(name, description, company, price, units, subcategory_id)
        cur.execute(query, values)

        conn.commit()

    except Exception as e:
        return {"status": -1, "message": f"Error de conexió:{e}"}
    
    finally:
        conn.close()
    
    return "S’ha afegit correctement" 

#Mètode per canviar les unitats d'un producte introduïnt la ID.
def update_product(units, product_id):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "update product SET units = %s WHERE product_id = %s;"
        values = (units, product_id)
        cur.execute(query, values)

        conn.commit()

    except Exception as e:
        return {"status": -1, "message": f"Error de conexió:{e}"}
    
    finally:
        conn.close()

#Mètode per eliminar un producte.
def delete_product(id):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "DELETE FROM product WHERE id = %s;"
        cur.execute(query,(id,))

        conn.commit()

    except Exception as e:
        return {"status": -1, "message": f"Error de conexió:{e}"}
    
    finally:
        conn.close()