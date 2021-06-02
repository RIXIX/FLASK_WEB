from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import config
import pickle
import os

#load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
DATABASE_URI = 'postgresql://vyfbdaka:tLsxsBoJVNz9s1uGpKPMmdtcaYMffeBv@batyr.db.elephantsql.com/vyfbdaka'

def create_app(config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    from weather_app.routes import main_route

    app.register_blueprint(main_route.bp)


    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
