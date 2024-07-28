from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    from app.models import User  # Import User model here to avoid circular imports

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    
    from app.routes import main
    app.register_blueprint(main)
    
    return app
