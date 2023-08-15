from flask import Flask
from config import load_config
from src.routes import api

app = Flask(__name__)
config = load_config(app)  # Carga la configuración desde config.py

app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=True)
