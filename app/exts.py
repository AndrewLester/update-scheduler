import wtforms_json
from authlib.integrations.flask_client import OAuth
from authlib.oauth1.client import OAuth1Client
from flask_caching import Cache
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


login = LoginManager()
db = SQLAlchemy()
migrate = Migrate(db=db)
cache = Cache()
oauth_client = OAuth()
csrf = CSRFProtect()
wtforms_json.init()


# Monkey patch _fetch_token method because Schoology only accepts get requests here
def _fetch_token(self, url, **kwargs):
        resp = self.session.get(url, auth=self.auth, **kwargs)
        token = self.parse_response_token(resp.status_code, resp.text)
        self.token = token
        self.auth.verifier = None
        return token


def fetch_access_token(self, url, verifier=None, **kwargs):
    if verifier:
        self.auth.verifier = verifier
    if not self.auth.verifier:
        pass
        # self.handle_error('missing_verifier', 'Missing "verifier" value')
    return self._fetch_token(url, **kwargs)


OAuth1Client._fetch_token = _fetch_token
OAuth1Client.fetch_access_token = fetch_access_token
