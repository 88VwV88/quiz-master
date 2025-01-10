from models import *
from sqlalchemy import select
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy(model_class=Base)


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        if (
            db.session.execute(select(User).where(User.email == "admin@qm.xyz")).first()
            is None
        ):
            user = User(
                name="vwv",
                email="admin@qm.xyz",
                password=generate_password_hash("admin"),
                qualification="NA",
                dob=date(2004, 5, 8),
                admin=True,
            )
            db.session.add(user)
            db.session.commit()
