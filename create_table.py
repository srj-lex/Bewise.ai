from datetime import datetime

from sqlalchemy import create_engine, Integer, String, Column, DateTime, Text
from sqlalchemy.orm import declarative_base


engine = create_engine(
    "postgresql+psycopg2://bewise_user:mysecretpassword@localhost:8080/bewise"
)

Base = declarative_base()


class Question(Base):
    __tablename__ = "questions"
    question_id = Column(Integer(), nullable=False, primary_key=True)
    question_text = Column(Text(), nullable=False)
    answer_text = Column(String(200), nullable=False)
    category_id = Column(Integer(), nullable=False)
    creation_date = Column(DateTime())
    created_at = Column(DateTime(), default=datetime.now)

    def __repr__(self):
        return (f"<Question: question_id - {self.question_id},"
                f"  created_at - {self.created_at}>")


Base.metadata.create_all(engine)
