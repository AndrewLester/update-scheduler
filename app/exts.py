import wtforms_json
# from authlib.client.client import OAuthClient
# from authlib.flask.client import OAuth
from authlib.oauth1.client import OAuth1Client
from flask_caching import Cache
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_sitemap import Sitemap


login = LoginManager()
db = SQLAlchemy()
migrate = Migrate(db=db)
cache = Cache()
# oauth = OAuth()
csrf = CSRFProtect()
wtforms_json.init()
