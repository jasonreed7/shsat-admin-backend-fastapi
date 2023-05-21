from datetime import datetime
from typing import Literal, Optional, Union

from pydantic import BaseModel, Field

from app.models.question import QuestionType, QuestionUsage


class QuestionBase(BaseModel):
    official_test_id: int
    official_test_question_number: int
    q_type: QuestionType
    usage: Optional[QuestionUsage]

    class Config:
        orm_mode = True


class QuestionCreate(QuestionBase):
    pass


class Question(QuestionBase):
    id: int
    created_at: datetime
    updated_at: datetime


class TextQuestionBase(QuestionBase):
    question_text: str
    explanation: str


class TextQuestionCreate(TextQuestionBase):
    pass


class TextQuestion(TextQuestionBase, Question):
    pass


class FillInQuestionCreate(TextQuestionCreate):
    answer: float


class FillInQuestion(TextQuestion):
    q_type: Literal[QuestionType.FILL_IN]
    answer: float


class MultipleChoiceAnswerBase(BaseModel):
    choice_number: int
    answer_text: str
    is_correct: bool

    class Config:
        orm_mode = True


class MultipleChoiceAnswerCreate(MultipleChoiceAnswerBase):
    pass


class MultipleChoiceAnswer(MultipleChoiceAnswerBase):
    question_id: int
    created_at: datetime
    updated_at: datetime


class MultipleChoiceQuestionCreate(TextQuestionCreate):
    answers: list[MultipleChoiceAnswerCreate]


class MultipleChoiceQuestion(TextQuestion):
    q_type: Literal[QuestionType.MULTIPLE_CHOICE]
    answers: list[MultipleChoiceAnswer]


# For returning list of either FillInQuestion or MultipleChoiceQuestion from route
# See https://stackoverflow.com/questions/73945126/how-to-return-a-response-with-a-list-of-different-pydantic-models-using-fastapi # noqa: E501


class QuestionWithAnswers(BaseModel):
    __root__: Union[FillInQuestion, MultipleChoiceQuestion] = Field(
        ..., discriminator="q_type"
    )

    class Config:
        orm_mode = True
