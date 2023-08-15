import os
from dotenv import load_dotenv


def load_config(app):
    load_dotenv()
    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY"
    )  # Define otras configuraciones aquí
    return app
