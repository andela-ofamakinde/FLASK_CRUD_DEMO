from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/user/source/PersonalProjects/FlaskProject/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
