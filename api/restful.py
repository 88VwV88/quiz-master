from models import *
from database import db
from sqlalchemy import select
from datetime import datetime
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
    set_access_cookies,
)
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask import request, jsonify, make_response
from werkzeug.security import check_password_hash, generate_password_hash

jwt = JWTManager()


@jwt.user_identity_loader
def user_identity_lookup(user: User):
    return user.email


@jwt.user_lookup_loader
def user_lookup_loader(_, jwt_data):
    identity = jwt_data["sub"]
    return db.session.execute(select(User).filter_by(email=identity)).one_or_none()


class Login(Resource):
    def post(self):
        try:
            login_data = request.get_json()
            user = db.session.execute(
                select(User).where(User.email == login_data["email"])
            ).scalar()

            if check_password_hash(user.password, login_data["password"]):
                access_token = create_access_token(identity=user)
                response = make_response(
                    {"username": user.name, "token": access_token, "isAdmin": user.admin}, 200)
                set_access_cookies(response, access_token)
                response.headers['Access-Control-Allow-Credentials'] = 'true'
                return response
            return make_response({"message": "Invalid credentials"}, 401)
        except IntegrityError:
            return make_response({"message": "SQL Integrity error"}, 500)
        except Exception as err:
            print(err)
            return make_response({"message": "Unknown error"}, 500)


class Users(Resource):
    @jwt_required()
    def get(self):
        print(request.headers)
        current_user = get_jwt_identity()
        if current_user.name != "admin":
            if db.session.execute(
                select(User).where(User.name == current_user.name)
            ).first():
                return jsonify({'logged_in_as': current_user})
            else:
                return {"message": "User not found"}, 404
        return jsonify(
            {
                "users": [
                    {"name": user.name, "email": user.email, "admin": user.admin}
                    for user in db.session.execute(select(User)).scalars()
                ]
            }
        )

    def post(self):
        try:
            user = request.get_json()
            user["password"] = generate_password_hash(user["password"])

            user = User(
                name=user["name"],
                email=user["email"],
                password=user["password"],
                qualification=user["qualification"],
                dob=datetime.strptime(user["dob"], "%Y-%m-%d").date(),
            )
            db.session.add(user)
            db.session.commit()

            return make_response({"message": "User created successfully"}, 201)
        except IntegrityError:
            return make_response({"message": "User already exists!"}, 400)


class Subjects(Resource):
    @jwt_required()
    def get(self):
        return jsonify(
            {
                "subjects": [
                    {
                        "name": subject.name,
                        "description": subject.description,
                        "chapters": [
                            {"name": chapter.name, "description": chapter.description}
                            for chapter in subject.chapters
                        ],
                    }
                    for subject in db.session.execute(select(Subject)).scalars()
                ]
            }
        )

    @jwt_required()
    def post(self):
        try:
            subject = request.get_json()
            chapters = subject.pop("chapters")

            subject = Subject(
                name=subject["name"], description=subject["description"])
            db.session.add(subject)
            db.session.commit()

            chapters = {
                Chapter(
                    name=chapter["name"],
                    description=chapter["description"],
                    subject_id=subject.id,
                )
                for chapter in chapters
            }
            db.session.add_all(chapters)
            db.session.commit()
            return {"message": "Subject created successfully"}, 201
        except IntegrityError:
            return {"message": "Subject already exists!"}, 400

    @jwt_required()
    def delete(self, subject_id: int):
        try:
            subject = db.session.execute(select(Subject).where(
                Subject.id == subject_id)).scalar()
            db.session.delete(subject)
            db.session.commit()
            return {"message": "Subject deleted successfully"}, 200
        except IntegrityError as error:
            print(error)
            return {"message": "Failed to delete subject!"}, 500
        except Exception as error:
            print(error)
            return {"message": "Unknown error"}, 500


class Quizzes(Resource):
    @jwt_required()
    def get(self, quiz_id: int | None = None):
        if quiz_id is not None:
            return db.session.execute(
                select(Quiz).where(Quiz.id == quiz_id)
            ).scalar_one()
        return jsonify(
            {
                "quizzes": [
                    {
                        "quiz_id": quiz.id,
                        "name": quiz.name,
                        "remarks": quiz.remarks,
                        "chapter": quiz.chapter.name,
                        "date_of_quiz": quiz.date_of_quiz,
                        "questions": [
                            {
                                "statement": question.statement,
                                "options": [
                                    option.statement for option in question.options
                                ],
                            }
                            for question in quiz.questions
                        ],
                    }
                    for quiz in db.session.execute(select(Quiz)).scalars()
                ]
            }
        )

    @jwt_required()
    def post(self):
        try:
            quiz = request.get_json()

            if subject := db.session.execute(
                select(Subject).where(Subject.name == quiz["subject"])
            ).scalar():
                chapter = None
                for chapter in subject.chapters:
                    if chapter.name == quiz["chapter"]:
                        break

                if chapter is not None:
                    questions = quiz.pop("questions")
                    quiz = Quiz(
                        name=quiz["name"],
                        remarks=quiz["remarks"],
                        subject_id=subject.id,
                        chapter_id=chapter.id,
                        date_of_quiz=datetime.strptime(
                            quiz["date_of_quiz"], "%Y-%m-%d"
                        ).date(),
                        duration=quiz["duration"],
                    )
                    db.session.add(quiz)
                    db.session.commit()

                    for question in questions:
                        options = question.pop("options")
                        answer = question.pop("answer")
                        question = Question(
                            statement=question["statement"], quiz_id=quiz.id
                        )
                        db.session.add(question)
                        db.session.commit()

                        options = [
                            Option(
                                statement=option['statement'],
                                is_correct=(i == answer),
                                question_id=question.id,
                            )
                            for i, option in enumerate(options)
                        ]
                        db.session.add_all(options)
                        db.session.commit()

                    return {"message": "Quiz created successfully"}, 201

                return {"message": "Chapter not found"}, 404

            return {"message": "Subject not found"}, 404
        except IntegrityError as error:
            print(error)
            return {"message": "Failed to create quiz!"}, 500
        except Exception as error:
            print(error)
            return {"message": "Unknown error"}, 500

    @jwt_required()
    def delete(self, quiz_id: int):
        try:
            quiz = db.session.execute(select(Quiz).where(
                Quiz.id == quiz_id)).scalar()
            db.session.delete(quiz)
            db.session.commit()
            return {"message": "Quiz deleted successfully"}, 200
        except IntegrityError as error:
            print(error)
            return {"message": "Failed to delete quiz!"}, 500
        except Exception as error:
            print(error)
            return {"message": "Unknown error"}, 500
