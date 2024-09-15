import os
import logging


class Config:
    try:
        # Tracing Configs
        SERVICE_NAME = "backendAPI"
        URL_Prefix = "/backend_api/v1"
        DOCS_URL_PREFIX="/backend_api/v1/internal"
        DEBUG = bool(os.environ.get("DEBUG", True))

        # Token Crreation 
        ALGORITHM = "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES = 2 * 60  # 2 hours
        REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
        JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
        JWT_REFRESH_SECRET_KEY = os.environ.get('JWT_REFRESH_SECRET_KEY')

        # DB connection
        SQLALCHEMY_ECHO = False
        SQLALCHEMY_TRACK_MODIFICATIONS = True
        DATABASE_URI = os.environ.get("DATABASE_URI")
        DB_USER = os.environ["DB_USER"].strip()
        DB_PASSWORD = os.environ["DB_PASSWORD"].strip()
        SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DATABASE_URI}"
        
        # Redis connection
        REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
        REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
        
        # OTP Service
        OTP_AUTH_KEY="430312Ahar2DJs66e4e918P1"
        EMAIL_TEMPLATE_ID = "global_otp"

    except Exception as e:
        logging.error("Error reading configurations")
        logging.error(str(e))
        exit()