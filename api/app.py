import os
from database import *
from flask import Flask
from flask_restful import Api
from bcrypt import hashpw, gensalt
from restful import Login, Users, Subjects, Quizzes, jwt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz-master.db"
app.config["JWT_SECRET_KEY"] = os.environ.get(
    "JWT_SECRET_KEY", hashpw(b"itsAs3cr34tkeyforJWT", gensalt())
)

init_db(app)
api = Api(app)
jwt.init_app(app)
api.add_resource(Login, "/login")
api.add_resource(Users, "/users", "/users/<int:user_id>")
api.add_resource(Quizzes, "/quizzes", "/quizzes/<int:quiz_id>")
api.add_resource(Subjects, "/subjects", "/subjects/<int:subject_id>")

if __name__ == "__main__":
    app.run(debug=True)
