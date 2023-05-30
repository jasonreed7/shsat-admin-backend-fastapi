from datetime import datetime
from typing import Any, List, Optional

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.data.question_enums import QuestionType, QuestionUsage
from app.database import Base

# see https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#using-python-enum-or-pep-586-literal-types-in-the-type-map for enum info # noqa: E501


class Question(Base):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(primary_key=True)
    official_test_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("official_test.id")
    )
    official_test_question_number: Mapped[Optional[int]]
    q_type: Mapped[QuestionType]
    usage: Mapped[Optional[QuestionUsage]]
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )

    __mapper_args__ = {
        "polymorphic_on": "q_type",
    }


class TextQuestion(Question):
    __tablename__ = "text_question"

    question_id: Mapped[int] = mapped_column(
        ForeignKey("question.id"), primary_key=True
    )
    question_text: Mapped[str]
    explanation: Mapped[str]

    __mapper_args__: dict[str, Any] = {
        "polymorphic_abstract": True,
    }


class MultipleChoiceAnswer(Base):
    __tablename__ = "multiple_choice_answer"

    question_id: Mapped[int] = mapped_column(
        ForeignKey("text_question.question_id"), primary_key=True
    )
    choice_number: Mapped[int] = mapped_column(
        CheckConstraint("choice_number BETWEEN 1 AND 4"), primary_key=True
    )
    answer_text: Mapped[str]
    is_correct: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )


class FillInQuestion(TextQuestion):
    __tablename__ = "fill_in_question"
    question_id: Mapped[int] = mapped_column(
        ForeignKey("text_question.question_id"), primary_key=True
    )
    answer: Mapped[float] = mapped_column(Numeric(7, 3))

    __mapper_args__: dict[str, Any] = {"polymorphic_identity": QuestionType.FILL_IN}


class MultipleChoiceQuestion(TextQuestion):
    answers: Mapped[List[MultipleChoiceAnswer]] = relationship()

    __mapper_args__: dict[str, Any] = {
        "polymorphic_identity": QuestionType.MULTIPLE_CHOICE
    }


class ImageQuestion(Question):
    __tablename__ = "image_question"

    question_id: Mapped[int] = mapped_column(
        ForeignKey("question.id"), primary_key=True
    )
    question_image_s3_key: Mapped[str]
    answer_image_s3_key: Mapped[str]

    __mapper_args__: dict[str, Any] = {
        "polymorphic_abstract": True,
    }


class FillInImageQuestion(ImageQuestion):
    __tablename__ = "fill_in_image_question"
    question_id: Mapped[int] = mapped_column(
        ForeignKey("image_question.question_id"), primary_key=True
    )
    answer: Mapped[float] = mapped_column(Numeric(7, 3))

    __mapper_args__: dict[str, Any] = {
        "polymorphic_identity": QuestionType.FILL_IN_IMAGE
    }


class MultipleChoiceImageQuestion(ImageQuestion):
    __tablename__ = "multiple_choice_image_question"
    question_id: Mapped[int] = mapped_column(
        ForeignKey("image_question.question_id"), primary_key=True
    )
    correct_choice: Mapped[int]

    __mapper_args__: dict[str, Any] = {
        "polymorphic_identity": QuestionType.MULTIPLE_CHOICE_IMAGE
    }
