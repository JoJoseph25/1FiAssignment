import uvicorn
from models import *
from fastapi import FastAPI
from configs.config import Config
from routes import setup_routing
from configs.extensions import setup_logger, setup_redis
from uvicorn.config import LOGGING_CONFIG
from configs.extensions import configure_logging

description = """
1Fi API helps you to create User and verify email/phone number to login.

You will be able to:
* **Get Scripts** (GET /scripts/<_clientID_>).
* **Add a Script** (POST /scripts/<_clientID_>).

* **Get Instances** (GET /instances/<_clientID_>).
* **Get Credits Information** (GET /credits/<_clientID_>).
* **Get Billing Information** (GET /bills/<_clientID_>).

"""
tags_metadata = [
    {
        "name": "User",
        "description": "User Info",
    },
    {
        "name": "SignUp",
        "description": "User Signup",
    },
    {
        "name": "Login",
        "description": "User Login",
    },
    {
        "name": "OTP",
        "description": "Verify using OTP",
    },
]


def create_app():
    """App factory."""
    app = FastAPI(
        title="1Fi BackendAPI",
        description=description,
        version="1.0.0",
        openapi_tags=tags_metadata,
        openapi_url=f"{Config.DOCS_URL_PREFIX}/openapi.json",
        docs_url=f"{Config.DOCS_URL_PREFIX}/docs",
        redoc_url=f"{Config.DOCS_URL_PREFIX}/redocs",
    )
    
    setup_routing(app)
    setup_logger(app)
    setup_redis(app)
    
    return app

# configure the application
app = create_app()

if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=5000, reload=True, log_config=configure_logging(LOGGING_CONFIG))


