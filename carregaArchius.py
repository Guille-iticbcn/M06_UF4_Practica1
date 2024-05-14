import csv
import mysql.connector

connection = mysql.connector.connect(
    host="tu_host",
    user="tu_usuario",
    password="tu_contraseña",
    database="tu_base_de_datos"
)
cursor = connection.cursor()

def load_products_from_csv(file_path):
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category_name = row['category']
                subcategory_name = row['subcategory']
                product_name = row['product']
                company = row['company']
                price = row['price']
                units = row['units']

                cursor.execute("SELECT category_id FROM category WHERE name = %s", (category_name,))
                category_result = cursor.fetchone()
                if category_result:
                    cursor.execute("UPDATE category SET updated_at = CURRENT_TIMESTAMP() WHERE category_id = %s", (category_result[0],))
                else:
                    cursor.execute("INSERT INTO category (name) VALUES (%s)", (category_name,))
                    category_id = cursor.lastrowid

                cursor.execute("SELECT subcategory_id FROM subcategory WHERE name = %s", (subcategory_name,))
                subcategory_result = cursor.fetchone()
                if subcategory_result:
                    cursor.execute("UPDATE subcategory SET updated_at = CURRENT_TIMESTAMP() WHERE subcategory_id = %s", (subcategory_result[0],))
                else:
                    cursor.execute("INSERT INTO subcategory (name, category_id) VALUES (%s, %s)", (subcategory_name, category_id))
                    subcategory_id = cursor.lastrowid

                cursor.execute("SELECT product_id FROM product WHERE name = %s", (product_name,))
                product_result = cursor.fetchone()
                if product_result:
                    cursor.execute("UPDATE product SET updated_at = CURRENT_TIMESTAMP() WHERE product_id = %s", (product_result[0],))
                else:
                    cursor.execute("INSERT INTO product (name, company, price, units, subcategory_id) VALUES (%s, %s, %s, %s, %s)", (product_name, company, price, units, subcategory_id))

            connection.commit()
            return {"message": "Càrrega massiva de productes completada correctament."}
    except Exception as e:
        return {"error": str(e)}

result = load_products_from_csv('ruta/del/archivo.csv')
print(result)

cursor.close()
connection.close()
