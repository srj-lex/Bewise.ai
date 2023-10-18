from datetime import datetime
import os
from typing import Final

from dotenv import load_dotenv
from sqlalchemy import create_engine, Integer, String, Column, DateTime, Text
from sqlalchemy.orm import declarative_base

load_dotenv()

USER: Final[str] = os.getenv("POSTGRES_USER", "postgres_user")
PASSWORD: Final[str] = os.getenv("POSTGRES_PASSWORD", "my_password")
POSTGRE_DB: Final[str] = os.getenv("POSTGRES_DB", "postgres")

HOST: Final[str] = os.getenv("DB_HOST", "localhost")
PORT: Final[int] = os.getenv("DB_PORT", 5432)


engine = create_engine(
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{POSTGRE_DB}"
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
