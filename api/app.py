import os
from database import *
from flask_cors import CORS
from flask import Flask, jsonify
from bcrypt import hashpw, gensalt
from flask_jwt_extended import unset_jwt_cookies
from restful import Login, Users, Subjects, Quizzes, jwt
from flask_restful import Api, NotFound, MethodNotAllowed

app = Flask(__name__)
app.config.update({
    "JWT_TOKEN_LOCATION": ["headers"],
    "JWT_COOKIE_CSRF_PROTECT": False,
    "SQLALCHEMY_DATABASE_URI":  "sqlite:///quiz-master.db",
    "JWT_SECRET_KEY":  os.environ.get(
        "JWT_SECRET_KEY", hashpw(b"itsAs3cr34tkeyforJWT", gensalt())
    ),
})

init_db(app)
api = Api(app)
cors = CORS(app)
jwt.init_app(app)
api.add_resource(Login, "/login")
api.add_resource(Users, "/users", "/users/<int:user_id>")
api.add_resource(Quizzes, "/quizzes", "/quizzes/<int:quiz_id>")
api.add_resource(Subjects, "/subjects", "/subjects/<int:subject_id>")


@app.route('/logout', methods=['POST'])
def logout():
    response = jsonify({'msg': 'logged out successfully!'})
    unset_jwt_cookies(response)
    return response


@app.errorhandler(NotFound)
def handle_method_not_found(e):
    response = jsonify({"message": str(e)})
    response.status_code = 404
    return response


@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed(e):
    response = jsonify({"message": str(e)})
    response.status_code = 405
    return response


if __name__ == "__main__":
    app.run(debug=True)
