from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spanish_database.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = 'asdhjkasjdh8i2y3+=+-'
app.config['DEBUG'] = True


if __name__ == '__main__':
    app.run(debug=True)
