from datetime import datetime
import os
from typing import Final, List

from dotenv import load_dotenv
from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
import requests
from sqlalchemy import Integer, String, DateTime, Text, desc
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


load_dotenv()

URL: Final[str] = "https://jservice.io/api/random?count="
MESSAGE_ERROR: Final[str] = "Значение должно быть целочисленным!"

USER: Final[str] = os.getenv("POSTGRES_USER", "postgres_user")
PASSWORD: Final[str] = os.getenv("POSTGRES_PASSWORD", "my_password")
POSTGRE_DB: Final[str] = os.getenv("POSTGRES_DB", "postgres")

HOST: Final[str] = os.getenv("DB_HOST", "localhost")
PORT: Final[int] = os.getenv("DB_PORT", 5432)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{POSTGRE_DB}"
db.init_app(app)


class Question(db.Model):
    question_id: Mapped[int] = mapped_column(
        Integer, nullable=False, primary_key=True
    )
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    answer_text: Mapped[str] = mapped_column(String, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, nullable=False)
    creation_date: Mapped[datetime] = mapped_column(
        DateTime,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )

    def __repr__(self):
        return (
            f"<Question: question_id - {self.question_id},"
            f"  created_at - {self.created_at}>"
        )


def write_object_in_db(data: List[dict]) -> bool:
    """
    Проверяет наличие полученного от API вопроса в БД,
    делает запись, если такого нет.
    """
    for quest_obj in data:
        id = quest_obj["id"]
        if db.session.query(Question).get(id) is None:
            db.session.add(
                Question(
                    question_id=id,
                    question_text=quest_obj["question"],
                    answer_text=quest_obj["answer"],
                    category_id=quest_obj["category_id"],
                    creation_date=quest_obj["created_at"],
                )
            )
        else:
            return False

    else:
        db.session.commit()
        return True


def get_object_from_db() -> dict:
    """
    Запрашивает у БД два последних созданных вопроса,
    возвращает предпоследний.
    """
    results = (
        db.session.query(Question)
        .order_by(desc(Question.created_at))
        .limit(2)
        .all()
    )
    data = []
    for i in results:
        query = i.__dict__
        del query["_sa_instance_state"]
        data.append(query)

    if len(data) != 2:
        return []
    return data[-1]


@app.route(
    "/quiz/",
    methods=[
        "POST",
    ],
)
def quiz_view() -> Response:
    count_value = request.get_json()["questions_num"]
    if not count_value.isdigit():
        return (MESSAGE_ERROR, 404)

    while True:
        response = requests.get(URL + f"{count_value}")
        if write_object_in_db(response.json()):
            break
        print("duplicate")

    resp = get_object_from_db()
    return (resp, 200)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.debug = False
    app.run(host="0.0.0.0")
