from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db=SQLAlchemy() 



def create_app():
    app = Flask(__name__,template_folder='templates',static_folder='static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@RAUT/Sample?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./waypoint.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from routes import register_routes
    register_routes(app,db)

    migrate = Migrate(app, db)

    return app