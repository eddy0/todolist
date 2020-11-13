from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    from app.models.user_model import User
    return User.query.get(int(user_id))
