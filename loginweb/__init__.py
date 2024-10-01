from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)



app = Flask(__name__)
app.config['SECRET_KEY'] = 'sfsdfsdfsd fsdfsdf'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///database.db'
db.init_app(app)

from .views import views
from .auth import auth
from .models import User, Note

app.register_blueprint(views, url_prefix='/') 
app.register_blueprint(auth, url_prefix='/')

login_manager = LoginManager()
login_manager.login_view = 'auth.acceso'
login_manager.init_app(app)
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))