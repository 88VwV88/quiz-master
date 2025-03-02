from typing import Set
from datetime import date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    qualification: Mapped[str] = mapped_column()
    dob: Mapped[date] = mapped_column()
    admin: Mapped[bool] = mapped_column(default=False)
    scores: Mapped[Set["Score"]] = relationship(
        back_populates="user", cascade="all, delete-orphan")


class Subject(Base):
    __tablename__ = "subject"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str] = mapped_column(default="")
    chapters: Mapped[Set["Chapter"]] = relationship(
        back_populates="subject", cascade="all, delete-orphan")
    quizzes: Mapped[Set["Quiz"]] = relationship(back_populates="subject")


class Chapter(Base):
    __tablename__ = "chapter"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str] = mapped_column(default="")
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id"))
    subject: Mapped["Subject"] = relationship(back_populates="chapters")
    quizzes: Mapped[Set["Quiz"]] = relationship(
        back_populates="chapter", cascade="all, delete-orphan")


class Quiz(Base):
    __tablename__ = "quiz"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id"))
    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapter.id"))
    date_of_quiz: Mapped[date]
    duration: Mapped[str] = mapped_column(default="30:00")
    remarks: Mapped[str] = mapped_column(default="")
    subject: Mapped["Subject"] = relationship(back_populates="quizzes")
    chapter: Mapped["Chapter"] = relationship(back_populates="quizzes")
    questions: Mapped[Set["Question"]] = relationship(
        back_populates="quiz", cascade="all, delete-orphan")
    scores: Mapped[Set["Score"]] = relationship(back_populates="quiz")


class Question(Base):
    __tablename__ = "question"
    id: Mapped[int] = mapped_column(primary_key=True)
    statement: Mapped[str]
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.id"))
    quiz: Mapped["Quiz"] = relationship("Quiz")
    options: Mapped[Set["Option"]] = relationship(cascade="all, delete-orphan")


class Option(Base):
    __tablename__ = "option"
    id: Mapped[int] = mapped_column(primary_key=True)
    statement: Mapped[str]
    is_correct: Mapped[bool] = mapped_column(default=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"))


class Score(Base):
    __tablename__ = "score"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.id"))
    total_score: Mapped[int]
    user: Mapped["User"] = relationship("User")
    quiz: Mapped["Quiz"] = relationship("Quiz")
