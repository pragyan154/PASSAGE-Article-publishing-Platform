from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db  = SQLAlchemy()
data = "database.db"

def create_app():
    app = Flask(__name__,template_folder='../template')
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{data}'
    db.init_app(app)


    from .views import views
    from .auth import auth
    from .models import User , Post

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    create_data(app)
    Login_manager = LoginManager()
    Login_manager.login_view = "auth.login"
    Login_manager.init_app(app)

    @Login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_data(app):
    if not path.exists("website/"+ data):
        db.create_all(app=app)
        print("db created")
