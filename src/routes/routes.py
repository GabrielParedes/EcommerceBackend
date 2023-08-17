from flask import jsonify, Blueprint, request

from src.database.db_mysql import fetch_all, is_db_connected, get_db_connection

# Asegúrate de usar la ruta correcta

api = Blueprint("api", __name__)


# APIs para Productos
# Insertar Productos
@api.route("/api/productos", methods=["POST"])
def insert_producto():
    if is_db_connected():
        try:
            data = request.get_json()
            title = data["title"]
            description = data["description"]
            type = data["type"]
            brand = data["brand"]
            category = data["category"]
            price = data["price"]
            sale = data.get("sale", 0)  # Valor por defecto si no se proporciona
            discount = data.get("discount", "")
            stock = data["stock"]
            new = data.get("new", 0)  # Valor por defecto si no se proporciona

            query = f"INSERT INTO productos (title, description, type, brand, category, price, sale, discount, stock, new) VALUES ('{title}', '{description}', '{type}', '{brand}', '{category}', {price}, {sale}, '{discount}', {stock}, {new})"
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()  # Confirmar la transacción

            cursor.close()
            connection.close()

            return jsonify({"message": "Producto insertado exitosamente"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


# Mostrar todos los productos
@api.route("/api/productos", methods=["GET"])
def get_productos():
    try:
        query = "SELECT * FROM productos"
        result = fetch_all(query)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})


# Mostrar un producto por su ID
@api.route("/api/productos/<int:id>", methods=["GET"])
def get_producto_by_id(id):
    try:
        query = f"SELECT * FROM productos WHERE id = {id}"
        result = fetch_all(query)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})


# Actualizar un producto por su ID
@api.route("/api/productos/<int:id>", methods=["PUT"])
def update_producto(id):
    if is_db_connected():
        try:
            data = request.get_json()
            title = data["title"]
            description = data["description"]
            type = data["type"]
            brand = data["brand"]
            category = data["category"]
            price = data["price"]
            sale = data.get("sale", 0)  # Valor por defecto si no se proporciona
            discount = data.get("discount", "")
            stock = data["stock"]
            new = data.get("new", 0)  # Valor por defecto si no se proporciona

            query = f"UPDATE productos SET title = '{title}', description = '{description}', type = '{type}', brand = '{brand}', category = '{category}', price = {price}, sale = {sale}, discount = '{discount}', stock = {stock}, new = {new} WHERE id = {id}"
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

            cursor.close()
            connection.close()

            return jsonify(
                {"message": f"Producto con ID {id} actualizado exitosamente"}
            )
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


# Borrar un producto por su ID
@api.route("/api/productos/<int:id>", methods=["DELETE"])
def delete_producto(id):
    if is_db_connected():
        try:
            query = f"DELETE FROM productos WHERE id = {id}"
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

            cursor.close()
            connection.close()

            return jsonify({"message": f"Producto con ID {id} eliminado exitosamente"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


# APIs para Clientes
# Ruta para insertar un cliente
@api.route("/api/clientes", methods=["POST"])
def insert_cliente():
    try:
        data = request.get_json()
        name = data["name"]
        username = data["username"]
        password = data["password"]

        query = f"INSERT INTO clientes (name, username, password) VALUES ('{name}', '{username}', '{password}')"
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Cliente insertado exitosamente"})
    except Exception as e:
        return jsonify({"error": str(e)})


# Ruta para obtener todos los clientes
@api.route("/api/clientes", methods=["GET"])
def get_clientes():
    if is_db_connected():
        try:
            query = "SELECT * FROM clientes"
            result = fetch_all(query)

            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


# Ruta para obtener un cliente por ID
@api.route("/api/clientes/<int:id>", methods=["GET"])
def get_cliente_by_id(id):
    if is_db_connected():
        try:
            query = f"SELECT * FROM clientes WHERE id = {id}"
            result = fetch_all(query)

            if result:
                return jsonify(result[0])
            else:
                return jsonify({"message": "Cliente no encontrado"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


# Ruta para actualizar un cliente por ID
@api.route("/api/clientes/<int:id>", methods=["PUT"])
def update_cliente(id):
    if is_db_connected():
        try:
            data = request.get_json()
            name = data["name"]
            username = data["username"]
            password = data["password"]

            query = f"UPDATE clientes SET name = '{name}', username = '{username}', password = '{password}' WHERE id = {id}"
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

            cursor.close()
            connection.close()

            return jsonify({"message": "Cliente actualizado exitosamente"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


# Ruta para borrar un cliente por ID
@api.route("/api/clientes/<int:id>", methods=["DELETE"])
def delete_cliente(id):
    if is_db_connected():
        try:
            query = f"DELETE FROM clientes WHERE id = {id}"
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

            cursor.close()
            connection.close()

            return jsonify({"message": "Cliente eliminado exitosamente"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


# APIs Imagenes
# Ruta para insertar una imagen
@api.route("/api/imagenes", methods=["POST"])
def insert_imagen():
    if is_db_connected():
        try:
            data = request.get_json()
            product_id = data["product_id"]
            img_id = data["id"]
            alt = data["alt"]
            src = data["src"]
            color = data["color"]

            query = f"INSERT INTO imagenes (product_id, id, alt, src, color) VALUES ({product_id}, '{img_id}', '{alt}', '{src}', '{color}')"
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

            cursor.close()
            connection.close()

            return jsonify({"message": "Imagen insertada exitosamente"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


# Ruta para obtener una imagen por su ID
@api.route("/api/imagenes/<int:image_id>", methods=["GET"])
def get_imagen(image_id):
    if is_db_connected():
        try:
            query = f"SELECT * FROM imagenes WHERE image_id = {image_id}"
            result = fetch_all(query)

            if result:
                return jsonify(result[0])
            else:
                return jsonify({"error": "Imagen no encontrada"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


# Ruta para actualizar una imagen por su ID
@api.route("/api/imagenes/<int:image_id>", methods=["PUT"])
def update_imagen(image_id):
    if is_db_connected():
        try:
            data = request.get_json()
            id = data.get("id")
            alt = data.get("alt")
            src = data.get("src")
            color = data.get("color")

            query = f"UPDATE imagenes SET alt = '{alt}', src = '{src}', color = '{color}', id = '{id}' WHERE image_id = {image_id}"
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

            cursor.close()
            connection.close()

            return jsonify({"message": "Imagen actualizada exitosamente"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


# Ruta para eliminar una imagen por su ID
@api.route("/api/imagenes/<int:image_id>", methods=["DELETE"])
def delete_imagen(image_id):
    if is_db_connected():
        try:
            query = f"DELETE FROM imagenes WHERE image_id = {image_id}"
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

            cursor.close()
            connection.close()

            return jsonify({"message": "Imagen eliminada exitosamente"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


# Ruta para obtener todas las imágenes
@api.route("/api/imagenes", methods=["GET"])
def get_all_imagenes():
    if is_db_connected():
        try:
            query = "SELECT * FROM imagenes"
            result = fetch_all(query)
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


# APIs Variantes
# Ruta para insertar una variante
@api.route("/api/variantes", methods=["POST"])
def insert_variante():
    if is_db_connected():
        try:
            data = request.get_json()
            product_id = data["product_id"]
            id = data["id"]
            sku = data["sku"]
            size = data["size"]
            color = data["color"]
            image_id = data["image_id"]

            query = f"INSERT INTO variantes (product_id, id, sku, size, color, image_id) VALUES ({product_id}, '{id}', '{sku}', '{size}', '{color}', {image_id})"
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

            cursor.close()
            connection.close()

            return jsonify({"message": "Variante insertada exitosamente"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


# Ruta para obtener todas las variantes
@api.route("/api/variantes", methods=["GET"])
def get_all_variantes():
    if is_db_connected():
        try:
            query = "SELECT * FROM variantes"
            result = fetch_all(query)
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


# Ruta para obtener una variante por su variante_id
@api.route("/api/variantes/<int:variante_id>", methods=["GET"])
def get_variante(variante_id):
    if is_db_connected():
        try:
            query = f"SELECT * FROM variantes WHERE variante_id = {variante_id}"
            result = fetch_all(query)
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


# Ruta para eliminar una variante por su variante_id
@api.route("/api/variantes/<int:variante_id>", methods=["DELETE"])
def delete_variante(variante_id):
    if is_db_connected():
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Verifica si la variante existe antes de eliminar
            check_query = f"SELECT * FROM variantes WHERE variante_id = {variante_id}"
            cursor.execute(check_query)
            exist = cursor.fetchone()

            if not exist:
                return jsonify({"error": "Variante no encontrada"})

            delete_query = f"DELETE FROM variantes WHERE variante_id = {variante_id}"
            cursor.execute(delete_query)
            connection.commit()

            cursor.close()
            connection.close()

            return jsonify({"message": "Variante eliminada exitosamente"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


# Ruta para actualizar una variante por su variante_id
@api.route("/api/variantes/<int:variante_id>", methods=["PUT"])
def update_variante(variante_id):
    if is_db_connected():
        try:
            data = request.get_json()
            product_id = data["product_id"]
            id = data["id"]
            sku = data["sku"]
            size = data["size"]
            color = data["color"]
            image_id = data["image_id"]

            query = f"UPDATE variantes SET product_id = {product_id}, id = '{id}', sku = '{sku}', size = '{size}', color = '{color}', image_id = {image_id} WHERE variante_id = {variante_id}"
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

            cursor.close()
            connection.close()

            return jsonify({"message": "Variante actualizada exitosamente"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


# APIs para las compras


@api.route("/api/compras", methods=["POST"])
def insert_compra():
    if is_db_connected():
        try:
            data = request.get_json()
            name = data["name"]
            phone = data["phone"]
            email = data["email"]
            address = data["address"]
            total = data["total"]
            payment_type = data["payment_type"]
            customer_id = data["customer_id"]

            query = f"INSERT INTO compras (name, phone, email, address, total, payment_type, customer_id) VALUES ('{name}', '{phone}', '{email}', '{address}', {total}, '{payment_type}', {customer_id})"
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()
            connection.close()

            return jsonify({"message": "Compra insertada exitosamente"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


@api.route("/api/compras", methods=["GET"])
def get_compras():
    if is_db_connected():
        try:
            query = "SELECT * FROM compras"
            result = fetch_all(query)
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


@api.route("/api/compras/<int:id_compra>", methods=["GET"])
def get_compra(id_compra):
    if is_db_connected():
        try:
            query = f"SELECT * FROM compras WHERE id = {id_compra}"
            result = fetch_all(query)
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


@api.route("/api/compras/<int:id_compra>", methods=["DELETE"])
def delete_compra(id_compra):
    if is_db_connected():
        try:
            query = f"DELETE FROM compras WHERE id = {id_compra}"
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({"message": "Compra eliminada exitosamente"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


@api.route("/api/compras/<int:id_compra>", methods=["PUT"])
def update_compra(id_compra):
    if is_db_connected():
        try:
            data = request.get_json()
            name = data["name"]
            phone = data["phone"]
            email = data["email"]
            address = data["address"]
            total = data["total"]
            payment_type = data["payment_type"]
            customer_id = data["customer_id"]

            query = f"UPDATE compras SET name='{name}', phone='{phone}', email='{email}', address='{address}', total={total}, payment_type='{payment_type}', customer_id={customer_id} WHERE id={id_compra}"

            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

            cursor.close()
            connection.close()

            return jsonify({"message": "Compra actualizada exitosamente"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


# APIs para detalle de compra
# Mostrar todos los detalles de compra
@api.route("/api/detalle_compra", methods=["GET"])
def get_all_detalle_compra():
    if is_db_connected():
        try:
            query = "SELECT * FROM detalle_compra"
            result = fetch_all(query)
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


# Mostrar un detalle de compra por su id
@api.route("/api/detalle_compra/<int:id_detalle>", methods=["GET"])
def get_detalle_compra(id_detalle):
    if is_db_connected():
        try:
            query = f"SELECT * FROM detalle_compra WHERE id = {id_detalle}"
            result = fetch_all(query)
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


# Insertar un nuevo detalle de compra
@api.route("/api/detalle_compra", methods=["POST"])
def insert_detalle_compra():
    if is_db_connected():
        try:
            data = request.get_json()
            product_id = data["product_id"]
            qty = data["qty"]
            subtotal = data["subtotal"]
            purchase_id = data["purchase_id"]

            query = f"INSERT INTO detalle_compra (product_id, qty, subtotal, purchase_id) VALUES ({product_id}, {qty}, {subtotal}, {purchase_id})"
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

            cursor.close()
            connection.close()

            return jsonify({"message": "Detalle de compra insertado exitosamente"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


# Actualizar un detalle de compra por su id
@api.route("/api/detalle_compra/<int:id_detalle>", methods=["PUT"])
def update_detalle_compra(id_detalle):
    if is_db_connected():
        try:
            data = request.get_json()
            product_id = data["product_id"]
            qty = data["qty"]
            subtotal = data["subtotal"]
            purchase_id = data["purchase_id"]

            query = f"UPDATE detalle_compra SET product_id={product_id}, qty={qty}, subtotal={subtotal}, purchase_id={purchase_id} WHERE id={id_detalle}"
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

            cursor.close()
            connection.close()

            return jsonify({"message": "Detalle de compra actualizado exitosamente"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})


# Eliminar un detalle de compra por su id
@api.route("/api/detalle_compra/<int:id_detalle>", methods=["DELETE"])
def delete_detalle_compra(id_detalle):
    if is_db_connected():
        try:
            query = f"DELETE FROM detalle_compra WHERE id = {id_detalle}"
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

            cursor.close()
            connection.close()

            return jsonify({"message": "Detalle de compra eliminado exitosamente"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"})
