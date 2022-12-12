from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "forum_database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "DoLbpxWD2T"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .authentications import authentications

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(authentications, url_prefix="/")

    from .database_models import User, Post_nfl, Post_nba, Post_mlb, Post_nhl, Comment_nfl, Comment_nba, Comment_mlb, Comment_nhl, Like_nfl

    # SQLAlchemy3
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "authentications.login"
    login_manager.init_app(app)

    # Callback
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
