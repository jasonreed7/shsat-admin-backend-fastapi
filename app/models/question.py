from datetime import datetime
import enum
from typing import List, Optional
from sqlalchemy import Boolean, CheckConstraint, Column, ForeignKey, Integer, Numeric, Text, func
from sqlalchemy.dialects.postgresql import ENUM, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

# see https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#using-python-enum-or-pep-586-literal-types-in-the-type-map for enum info
class QuestionType(enum.Enum):
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    FILL_IN = "FILL_IN"

class QuestionUsage(enum.Enum):
    OFFICIAL_TEST_QUESTION = "OFFICIAL_TEST_QUESTION"
    TEST_QUESTION = "TEST_QUESTION"
    PROBLEM_SET_QUESTION = "PROBLEM_SET_QUESTION"

class Question(Base):
    __tablename__ = 'question'

    id: Mapped[int] = mapped_column(primary_key=True)
    official_test_id: Mapped[Optional[int]] = mapped_column(ForeignKey('official_test.id'))
    official_test_question_number: Mapped[Optional[int]]
    question_text: Mapped[str]
    q_type: Mapped[QuestionType]
    explanation: Mapped[str]
    usage: Mapped[Optional[QuestionUsage]]
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    __mapper_args__ = {
        "polymorphic_on": "q_type",
    }

class FillInAnswer(Base):
    __tablename__ = 'fill_in_answer'
    
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"), primary_key=True)
    answer: Mapped[float] = mapped_column(Numeric(7, 3))
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

class MultipleChoiceAnswer(Base):
    __tablename__ = 'multiple_choice_answer'
    
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"), primary_key=True)
    choice_number: Mapped[int] = mapped_column(CheckConstraint('choice_number BETWEEN 1 AND 4'), primary_key=True)
    answer_text: Mapped[str]
    is_correct: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

class FillInQuestion(Question):
    __tablename__ = "fill_in_answer"
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"), primary_key=True)
    answer: Mapped[float] = mapped_column(Numeric(7, 3))
    
    __mapper_args__ = {
        "polymorphic_identity": QuestionType.FILL_IN
    }

class MultipleChoiceQuestion(Question):
    __tablename__ = "question"
    answers: Mapped[List[MultipleChoiceAnswer]] = relationship()

    __mapper_args__ = {
        "polymorphic_identity": QuestionType.MULTIPLE_CHOICE
    }