from flask import Flask
from config import load_config
from src.routes import api
from flask_cors import CORS
from src.routes import create_api_blueprint

app = Flask(__name__)
CORS(app)


app.config["UPLOAD_FOLDER"] = "src/uploads"
config = load_config(app)  # Carga la configuración desde config.py

# Registra las rutas utilizando create_api_blueprint
app.register_blueprint(create_api_blueprint(app))

if __name__ == "__main__":
    app.run(debug=True)
    # Imprimir listado de rutas al ejecutar el script
    if app.debug:
        print("Listado de Rutas:")
        for rule in app.url_map.iter_rules():
            print(f"Ruta: {rule.rule}, Métodos: {', '.join(rule.methods)}")
