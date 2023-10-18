from typing import List

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import Session

from create_table import Question


engine = create_engine(
    "postgresql+psycopg2://bewise_user:mysecretpassword@localhost:8080/bewise"
)
session = Session(bind=engine)


def write_object_in_db(data: List[dict]) -> bool:
    """
    Проверяет наличие полученного от API вопроса в БД,
    делает запись, если такого нет.
    """
    for quest_obj in data:
        id = quest_obj["id"]
        if session.query(Question).get(id) is None:
            session.add(
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
        session.commit()
        return True


def get_object_from_db() -> dict:
    """
    Запрашивает у БД два последних созданных вопроса,
    возвращает предпоследний.
    """
    results = (
        session.query(Question)
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
