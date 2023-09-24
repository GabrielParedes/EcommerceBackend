from flask import jsonify, Blueprint, request, current_app, send_from_directory
from src.database.db_mysql import fetch_all, is_db_connected, get_db_connection
from werkzeug.utils import secure_filename
import os
from uuid import uuid4


# Asegúrate de usar la ruta correcta

api = Blueprint("api", __name__)


# Función para crear el Blueprint de las rutas
def create_api_blueprint(app):
    # Crea el Blueprint de las rutas
    api = Blueprint("api", __name__)

    # Almacenar Imagenes
    @api.route("/api/upload", methods=["POST"])
    def upload_file():
        if "image" not in request.files:
            return jsonify({"error": "No se ha enviado ningún archivo"})

        file = request.files["image"]

        if file.filename == "":
            return jsonify({"error": "No se ha seleccionado un archivo"})

        if file:
            # Genera un valor aleatorio único usando uuid4
            random_value = str(uuid4().hex)
            original_filename = secure_filename(file.filename)
            filename = f"{random_value}_{original_filename}"
            print(filename)
            upload_folder = current_app.config[
                "UPLOAD_FOLDER"
            ]  # Obtiene la configuración desde current_app
            file.save(os.path.join(upload_folder, filename))
            image_uri = f"/{upload_folder}/{filename}"  # URL de la imagen
            image_url = f"/public/{filename}"

            return jsonify({"path": image_uri, "url": image_url})

    @api.route("/api/categorias", methods=["POST"])
    def insert_categoria():
        if is_db_connected():
            try:
                data = request.get_json()
                print(data)
                category = data["name"]
                photo_url = data["image"]
                print(category)
                print(photo_url)

                # Inserta la nueva categoría en la base de datos junto con la URL de la imagen
                query = f"INSERT INTO categorias (name, image) VALUES ('{category}', '{photo_url}')"
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()

                cursor.close()
                connection.close()

                return jsonify({"message": "Categoría insertada exitosamente"})
            except Exception as e:
                return jsonify({"error": str(e)})
        else:
            return jsonify({"error": "No se pudo conectar a la base de datos"})

    # API para mostrar todas las categorías
    @api.route("/api/categorias", methods=["GET"])
    def get_all_categorias():
        if is_db_connected():
            try:
                query = "SELECT * FROM categorias"
                result = fetch_all(query)
                print(result)
                return jsonify(result)
            except Exception as e:
                return jsonify({"error": str(e)})
        else:
            return jsonify({"error": "No se pudo conectar a la base de datos"})

    # API para borrar categoria por id
    @api.route("/api/categorias/<int:id>", methods=["DELETE"])
    def delete_categoria(id):
        if is_db_connected():
            try:
                query = f"DELETE FROM categorias WHERE id = {id}"
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()

                cursor.close()
                connection.close()

                return jsonify(
                    {"message": f"Categoria con ID {id} eliminado exitosamente"}
                )
            except Exception as e:
                return jsonify({"error": str(e)})
        else:
            return jsonify({"error": "No se pudo conectar a la base de datos"})

    # Ruta para actualizar una categoria por ID
    @api.route("/api/categorias/<int:id>", methods=["PUT"])
    def update_categoria(id):
        if is_db_connected():
            try:
                data = request.get_json()
                name = data["name"]
                image = data["image"]

                query = f"UPDATE categorias SET name = '{name}', image = '{image}' WHERE id = {id}"
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()

                cursor.close()
                connection.close()

                return jsonify({"message": "Categoria actualizado exitosamente"})
            except Exception as e:
                return jsonify({"error": str(e)})
        else:
            return jsonify({"error": "No se pudo conectar a la base de datos"})

    # API para mostrar todas las categorías por producto
    @api.route("/api/categorias/productos", methods=["GET"])
    def get_all_categoriasprod():
        if is_db_connected():
            try:
                query = """
                SELECT categorias.id AS categoria_id, categorias.name AS categoria_name, 
                       productos.id AS producto_id, productos.title AS producto_title,
                       productos.price AS producto_price, categorias.image AS categoria_image
                FROM categorias
                RIGHT JOIN productos ON categorias.id = productos.category_id;
            """
                result = fetch_all(query)
                # print(result)
                return jsonify(result)
            except Exception as e:
                return jsonify({"error": str(e)})
        else:
            return jsonify({"error": "No se pudo conectar a la base de datos"})
        


    # APIs para Productos

    # Insertar Productos
    @api.route("/api/productos", methods=["POST"])
    def insert_producto():
        if is_db_connected():
            try:
                data = request.get_json()
                print(data)
                title = data["title"]
                description = data["description"]
                type = data["type"]
                brand = data["brand"]
                category = data["category_id"]
                price = data["price"]
                sale = data.get("sale", 0)  # Valor por defecto si no se proporciona
                discount = data.get("discount", 0)
                stock = data["stock"]
                new = data.get("new", 0)  # Valor por defecto si no se proporciona

                query = f"INSERT INTO productos (title, description, type, brand, category_id, price, sale, discount, stock, new) VALUES ('{title}', '{description}', '{type}', '{brand}', '{category}', {price}, {sale}, '{discount}', {stock}, {new})"
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()  # Confirmar la transacción

                id_inserted = cursor.lastrowid

                cursor.close()
                connection.close()

                return jsonify({"message": "Producto insertado exitosamente", "id": id_inserted})
            except Exception as e:
                return jsonify({"error": str(e)})
        else:
            return jsonify({"error": "No se pudo conectar a la base de datos"})

    # Mostrar todos los productos
    @api.route("/api/productos", methods=["GET"])
    def get_productos():
        try:
            query = "SELECT p.*, CONCAT('http://localhost:5000', i.src) AS src, v.sku, v.size FROM productos p INNER JOIN imagenes i ON p.id = i.product_id INNER JOIN variantes v ON p.id = v.product_id"
            result = fetch_all(query)
            print(result)
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
                category_id = data["category_id"]
                price = data["price"]
                sale = data.get("sale", 0)  # Valor por defecto si no se proporciona
                discount = data.get("discount", "")
                stock = data["stock"]
                new = data.get("new", 0)  # Valor por defecto si no se proporciona

                query = f"UPDATE productos SET title = '{title}', description = '{description}', type = '{type}', brand = '{brand}', category_id = '{category_id}', price = {price}, sale = {sale}, discount = '{discount}', stock = {stock}, new = {new} WHERE id = {id}"
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

                return jsonify(
                    {"message": f"Producto con ID {id} eliminado exitosamente"}
                )
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

    # Ruta para obtener un cliente por username
    @api.route("/api/clientes/username", methods=["GET"])
    def get_cliente_by_email():
        if is_db_connected():
            try:
                data = request.get_json()
                username = data["username"]

                query = f"SELECT * FROM clientes WHERE username = {username}"
                result = fetch_all(query)

                if result:
                    return jsonify(result[0])
                else:
                    return jsonify({"message": "Cliente no encontrado"})
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

                id_inserted = cursor.lastrowid

                cursor.close()
                connection.close()

                return jsonify({"message": "Imagen insertada exitosamente", "id": id_inserted})
            except Exception as e:
                return jsonify({"error": str(e)})
        else:
            return jsonify({"error": "No se pudo conectar a la base de datos"})

    # Ruta para obtener una imagen por su ID
    @api.route("/api/imagenes/<int:product_id>", methods=["GET"])
    def get_imagen(product_id):
        if is_db_connected():
            try:
                query = f"SELECT * FROM imagenes WHERE product_id = {product_id}"
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
    @api.route("/api/imagenes/<int:product_id>", methods=["DELETE"])
    def delete_imagen(product_id):
        if is_db_connected():
            try:
                query = f"DELETE FROM imagenes WHERE product_id = {product_id}"
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
    @api.route("/api/variantes/<int:product_id>", methods=["GET"])
    def get_variante(product_id):
        if is_db_connected():
            try:
                query = f"SELECT * FROM variantes WHERE product_id = {product_id}"
                result = fetch_all(query)
                return jsonify(result)
            except Exception as e:
                return jsonify({"error": str(e)})
        else:
            return jsonify({"error": "No se pudo conectar a la base de datos"})

    # Ruta para eliminar una variante por su variante_id
    @api.route("/api/variantes/<int:product_id>", methods=["DELETE"])
    def delete_variante(product_id):
        if is_db_connected():
            try:
                connection = get_db_connection()
                cursor = connection.cursor()

                # Verifica si la variante existe antes de eliminar
                check_query = (
                    # f"SELECT * FROM variantes WHERE variante_id = {variante_id}"
                    f"SELECT * FROM variantes WHERE product_id = {product_id}"
                )
                cursor.execute(check_query)
                exist = cursor.fetchone()

                if not exist:
                    return jsonify({"error": "Variante no encontrada"})

                delete_query = (
                    # f"DELETE FROM variantes WHERE variante_id = {variante_id}"
                    f"DELETE FROM variantes WHERE product_id = {product_id}"
                )
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
    @api.route("/api/variantes/<int:product_id>", methods=["PUT"])
    def update_variante(product_id):
        if is_db_connected():
            try:
                data = request.get_json()
                # product_id = data["product_id"]
                id = data["id"]
                sku = data["sku"]
                size = data["size"]
                color = data["color"]
                image_id = data["image_id"]

                query = f"UPDATE variantes SET sku = '{sku}', size = '{size}', color = '{color}', image_id = {image_id} WHERE product_id = {product_id} AND id = '{id}"
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

                return jsonify(
                    {"message": "Detalle de compra actualizado exitosamente"}
                )
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

    # API para mostrar una categoría por su ID
    @api.route("/api/categorias/<int:id_categoria>", methods=["GET"])
    def get_categoria(id_categoria):
        if is_db_connected():
            try:
                query = f"SELECT * FROM categorias WHERE id = {id_categoria}"
                result = fetch_all(query)
                return jsonify(result)
            except Exception as e:
                return jsonify({"error": str(e)})
        else:
            return jsonify({"error": "No se pudo conectar a la base de datos"})

    @api.route("/public/<filename>", methods=["GET"])
    def get_uploaded_file(filename):
        return send_from_directory('src/uploads', filename)

    return api
