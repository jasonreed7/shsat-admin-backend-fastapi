from datetime import datetime
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

from app.data.question_enums import PassageType, Section, SubSection
from app.models.question import QuestionType, UsageType
from app.schemas.tag import Tag, TagReference


class QuestionBase(BaseModel):
    official_test_id: int
    official_test_question_number: int
    q_type: QuestionType
    usage: Optional[UsageType]
    section: Optional[Section]
    sub_section: Optional[SubSection]

    class Config:
        orm_mode = True


class QuestionUpdate(BaseModel):
    official_test_id: Optional[int]
    official_test_question_number: Optional[int]
    usage: Optional[UsageType]
    section: Optional[Section]
    sub_section: Optional[SubSection]
    tags: Optional[List[TagReference]]


class QuestionCreate(QuestionBase):
    tags: List[TagReference]


class Question(QuestionBase):
    id: int
    tags: List[Tag]
    created_at: datetime
    updated_at: datetime


class TextQuestionBase(QuestionBase):
    question_text: str
    explanation: str


class TextQuestionUpdate(QuestionUpdate):
    question_text: Optional[str]
    explanation: Optional[str]


class TextQuestionCreate(TextQuestionBase, QuestionCreate):
    pass


class TextQuestion(TextQuestionBase, Question):
    pass


class FillInQuestionCreate(TextQuestionCreate):
    answer: float


class FillInQuestionUpdate(TextQuestionUpdate):
    answer: Optional[float]


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


class MultipleChoiceAnswerUpdate(BaseModel):
    choice_number: Optional[int]
    answer_text: Optional[str]
    is_correct: Optional[bool]


class MultipleChoiceAnswer(MultipleChoiceAnswerBase):
    question_id: int
    created_at: datetime
    updated_at: datetime


class MultipleChoiceQuestionCreate(TextQuestionCreate):
    answers: list[MultipleChoiceAnswerCreate]


class MultipleChoiceQuestionUpdate(TextQuestionUpdate):
    answers: Optional[list[MultipleChoiceAnswerCreate]]


class MultipleChoiceQuestion(TextQuestion):
    q_type: Literal[QuestionType.MULTIPLE_CHOICE]
    answers: list[MultipleChoiceAnswer]


class ImageQuestionBase(QuestionBase):
    question_image_s3_key: str
    answer_image_s3_key: str


class ImageQuestionCreate(ImageQuestionBase, QuestionCreate):
    pass


class ImageQuestionUpdate(QuestionUpdate):
    question_image_s3_key: Optional[str]
    answer_image_s3_key: Optional[str]


class ImageQuestion(ImageQuestionBase, Question):
    pass


class FillInImageQuestionCreate(ImageQuestionCreate):
    answer: float


class FillInImageQuestionUpdate(ImageQuestionUpdate):
    answer: Optional[float]


class FillInImageQuestion(ImageQuestion):
    q_type: Literal[QuestionType.FILL_IN_IMAGE]
    answer: float


class MultipleChoiceImageQuestionCreate(ImageQuestionCreate):
    correct_choice: int


class MultipleChoiceImageQuestionUpdate(ImageQuestionUpdate):
    correct_choice: Optional[int]


class MultipleChoiceImageQuestion(ImageQuestion):
    q_type: Literal[QuestionType.MULTIPLE_CHOICE_IMAGE]
    correct_choice: int


# For returning list of either FillInQuestion or MultipleChoiceQuestion from route
# See https://stackoverflow.com/questions/73945126/how-to-return-a-response-with-a-list-of-different-pydantic-models-using-fastapi # noqa: E501


class QuestionWithAnswers(BaseModel):
    __root__: Union[
        FillInQuestion,
        MultipleChoiceQuestion,
        FillInImageQuestion,
        MultipleChoiceImageQuestion,
    ] = Field(..., discriminator="q_type")

    class Config:
        orm_mode = True


class PassageBase(BaseModel):
    official_test_id: Optional[int]
    p_type: PassageType
    title: str
    usage: Optional[UsageType]
    section: Optional[Section]
    sub_section: Optional[SubSection]

    class Config:
        orm_mode = True


class PassageUpdate(BaseModel):
    official_test_id: Optional[int]
    title: Optional[str]
    usage: Optional[UsageType]
    section: Optional[Section]
    sub_section: Optional[SubSection]


class PassageCreate(PassageBase):
    pass


class Passage(PassageBase):
    id: int
    created_at: datetime
    updated_at: datetime


class ImagePassageBase(PassageBase):
    passage_image_s3_key: str


class ImagePassageCreate(ImagePassageBase, PassageCreate):
    pass


class ImagePassageUpdate(PassageUpdate):
    passage_image_s3_key: Optional[str]


class ImagePassage(ImagePassageBase, Passage):
    pass


class TextPassageBase(PassageBase):
    passage_text: str


class TextPassageCreate(TextPassageBase, PassageCreate):
    pass


class TextPassageUpdate(PassageUpdate):
    passage_text: Optional[str]


class TextPassage(TextPassageBase, Passage):
    pass
