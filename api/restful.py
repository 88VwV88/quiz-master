from models import *
from database import db
from datetime import datetime
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
    set_access_cookies,
)
from flask_restful import Resource
from sqlalchemy import select, delete, update
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
        except Exception as error:
            print(error)
            return make_response({"message": "Unknown error"}, 500)


class Users(Resource):
    @jwt_required()
    def get(self):
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
                        "id": subject.id,
                        "name": subject.name,
                        "description": subject.description,
                        "chapters": [
                            {"id": chapter.id, "name": chapter.name,
                                "description": chapter.description}
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
            db.session.execute(delete(Subject).where(Subject.id == subject_id))
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
        current_user = db.session.execute(
            select(User).where(User.email == get_jwt_identity())
        ).scalar()

        if quiz_id is not None:
            quizzes = db.session.execute(
                select(Quiz).where(Quiz.id == quiz_id).join(
                    Score, Score.user_id != current_user.id)
            ).scalar()
            return jsonify(quizzes)
        return jsonify(
            {
                "quizzes": [
                    {
                        "quiz_id": quiz.id,
                        "name": quiz.name,
                        "remarks": quiz.remarks,
                        "subject": quiz.chapter.subject.name,
                        "chapter": quiz.chapter.name,
                        "hh": quiz.hours,
                        "mm": quiz.minutes,
                        "date_of_quiz": quiz.date_of_quiz,
                        "questions": [
                            {
                                "id": question.id,
                                "statement": question.statement,
                                "options": [
                                    {
                                        "id": option.id,
                                        "statement": option.statement
                                    } for option in question.options
                                ],
                            }
                            for question in quiz.questions
                        ],
                        "done": current_user in (score.user for score in quiz.scores)
                    }
                    for quiz in db.session.execute(select(Quiz)).scalars()
                ]
            }
        )

    @jwt_required()
    def post(self):
        try:
            quiz = request.get_json()

            questions = quiz.pop("questions")
            quiz = Quiz(
                name=quiz["name"],
                remarks=quiz["remarks"],
                subject_id=int(quiz["subject"]),
                chapter_id=int(quiz["chapter"]),
                date_of_quiz=datetime.strptime(
                    quiz["date_of_quiz"], "%Y-%m-%d"
                ).date(),
                hours=int(quiz["hh"]),
                minutes=int(quiz["mm"]),
            )

            db.session.add(quiz)
            db.session.commit()
            for question in questions:
                options = question.pop("options")
                answer = question.pop("answer")
                question = Question(
                    statement=question["statement"], quiz_id=quiz.id,
                    correct=0
                )
                db.session.add(question)
                db.session.commit()
                options = [
                    Option(
                        statement=option['statement'],
                        question_id=question.id,
                    )
                    for option in options
                ]
                db.session.add_all(options)
                db.session.commit()
                db.session.execute(update(Question).where(
                    Question.id == question.id).values(correct=options[answer].id))
                db.session.commit()
            return {"message": "Quiz created successfully"}, 201
        except IntegrityError as error:
            print(error)
            return {"message": "Failed to create quiz!"}, 500
        except Exception as error:
            print(error)
            raise error
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


class QuizSubmit(Resource):
    @jwt_required()
    def post(self):
        try:
            quiz_data = request.get_json()

            current_user = db.session.execute(select(User).where(
                User.email == get_jwt_identity())).scalar()
            quiz = db.session.execute(select(Quiz).where(
                Quiz.id == quiz_data["quiz_id"])).scalar()

            user_score = 0
            for question in quiz.questions:
                if question.correct == quiz_data["selected"][str(question.id)]:
                    user_score += 1
            user_score = Score(user_id=current_user.id, quiz_id=quiz.id,
                               user_score=user_score, total_score=len(quiz.questions))
            db.session.add(user_score)
            db.session.commit()

            return {"message": "User score updated!"}, 201
        except IntegrityError as error:
            print(error)
            return {"message": "Failed to delete quiz!"}, 500
        except Exception as error:
            print(error)
            return {"message": "Unknown error"}, 500


class UserScores(Resource):
    @jwt_required()
    def get(self):
        try:
            current_user = db.session.execute(
                select(User).where(User.email == get_jwt_identity())).scalar()
            return jsonify({
                "scores": [
                    {
                        "total": score.total_score,
                        "correct": score.user_score,
                        "date_of_quiz": score.quiz.date_of_quiz,
                        "id": score.id
                    }
                    for score in current_user.scores
                ]
            })
        except IntegrityError as error:
            print(error)
            return {"message": "Failed to delete quiz!"}, 500
        except Exception as error:
            print(error)
            return {"message": "Unknown error"}, 500
