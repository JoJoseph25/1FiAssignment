from routes import User
from configs.config import Config

def setup_routing(app):
    app.include_router(User.router, prefix=Config.URL_Prefix)
