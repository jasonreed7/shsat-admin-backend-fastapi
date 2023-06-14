import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectin_polymorphic

from app.data.question_enums import PassageType
from app.database import SessionLocal
from app.exceptions.exceptions import TagNotFoundException
from app.models import question as question_models
from app.models import tag as tag_models
from app.schemas import question as question_schemas


def get_questions(db: SessionLocal):
    loader_opt = selectin_polymorphic(
        question_models.Question,
        [question_models.FillInQuestion, question_models.MultipleChoiceQuestion],
    )
    stmt = (
        select(question_models.Question)
        .order_by(question_models.Question.id)
        .options(loader_opt)
    )
    result = db.scalars(stmt).all()
    return result


def create_fill_in_question(
    db: SessionLocal, question: question_schemas.FillInQuestionCreate
):
    question_model = question_models.FillInQuestion(
        official_test_id=question.official_test_id,
        official_test_question_number=question.official_test_question_number,
        question_text=question.question_text,
        q_type=question_models.QuestionType.FILL_IN,
        explanation=question.explanation,
        usage=question.usage,
        answer=question.answer,
        passage_id=question.passage_id,
        tags=get_tags(db, question),
    )

    db.add(question_model)
    db.commit()

    return question_model


def create_multiple_choice_question(
    db: SessionLocal, question: question_schemas.MultipleChoiceQuestionCreate
):
    question_model = question_models.MultipleChoiceQuestion(
        official_test_id=question.official_test_id,
        official_test_question_number=question.official_test_question_number,
        question_text=question.question_text,
        q_type=question_models.QuestionType.MULTIPLE_CHOICE,
        section=question.section,
        sub_section=question.sub_section,
        explanation=question.explanation,
        usage=question.usage,
        passage_id=question.passage_id,
        tags=get_tags(db, question),
    )

    for answer in question.answers:
        answer_model = question_models.MultipleChoiceAnswer(
            choice_number=answer.choice_number,
            answer_text=answer.answer_text,
            is_correct=answer.is_correct,
        )

        question_model.answers.append(answer_model)

    db.add(question_model)
    db.commit()

    return question_model


def create_fill_in_image_question(
    db: SessionLocal, question: question_schemas.FillInImageQuestionCreate
):
    question_model = question_models.FillInImageQuestion(
        official_test_id=question.official_test_id,
        official_test_question_number=question.official_test_question_number,
        q_type=question_models.QuestionType.FILL_IN_IMAGE,
        usage=question.usage,
        section=question.section,
        sub_section=question.sub_section,
        question_image_s3_key=question.question_image_s3_key,
        answer_image_s3_key=question.answer_image_s3_key,
        answer=question.answer,
        passage_id=question.passage_id,
        tags=get_tags(db, question),
    )

    db.add(question_model)
    db.commit()

    return question_model


def create_multiple_choice_image_question(
    db: SessionLocal, question: question_schemas.MultipleChoiceImageQuestionCreate
):
    question_model = question_models.MultipleChoiceImageQuestion(
        official_test_id=question.official_test_id,
        official_test_question_number=question.official_test_question_number,
        q_type=question_models.QuestionType.MULTIPLE_CHOICE_IMAGE,
        usage=question.usage,
        section=question.section,
        sub_section=question.sub_section,
        question_image_s3_key=question.question_image_s3_key,
        answer_image_s3_key=question.answer_image_s3_key,
        correct_choice=question.correct_choice,
        passage_id=question.passage_id,
        tags=get_tags(db, question),
    )

    db.add(question_model)
    db.commit()

    return question_model


# See https://sqlmodel.tiangolo.com/tutorial/fastapi/update/#create-the-update-path-operation # noqa: E501
# For the type[question_models.Question] see https://mypy.readthedocs.io/en/stable/kinds_of_types.html#the-type-of-class-objects # noqa: E501
def update_question(
    db: SessionLocal,
    question_id: int,
    question_update: question_schemas.QuestionUpdate,
    question_class: type[question_models.Question],
) -> question_models.Question:
    question_model = db.get(question_class, question_id)
    if not question_model:
        raise HTTPException(400, f"Question not found, id: {question_id}")
    question_data = question_update.dict(exclude_unset=True)
    for key, value in question_data.items():
        if key != "tags" and key != "answers":
            setattr(question_model, key, value)

    # if tags field is sent, replace all existing tags with the sent tags
    if question_update.tags:
        question_model.tags = get_tags(db, question_update)

    db.add(question_model)

    # Handling multiple choice answers- maybe we should split this out
    if (
        question_class == question_models.MultipleChoiceQuestion
        and question_update.answers
    ):
        # If answers are sent, replace all existing answers with the sent answers
        question_model.answers.clear()
        # If we don't flush here a SQL update is run which can trigger
        # the only one correct answer check constraint
        db.flush()

        question_model.answers.extend(
            [
                question_models.MultipleChoiceAnswer(
                    choice_number=answer.choice_number,
                    answer_text=answer.answer_text,
                    is_correct=answer.is_correct,
                )
                for answer in question_update.answers
            ]
        )

    db.commit()
    return question_model


def get_tags(
    db: SessionLocal,
    question: question_schemas.QuestionCreate | question_schemas.QuestionUpdate,
) -> List[tag_models.Tag]:
    tag_ids = []
    if question.tags:
        tag_ids = [tag.id for tag in question.tags]
    tags = db.query(tag_models.Tag).filter(tag_models.Tag.id.in_(tag_ids)).all()
    if len(tags) != len(tag_ids):
        message = f"Could not find all tags in database- requested tag IDs: {tag_ids}"
        logging.warning(message)
        raise TagNotFoundException(message)
    return tags


def get_passages(db: SessionLocal) -> list[question_models.Passage]:
    loader_opt = selectin_polymorphic(
        question_models.Passage,
        [question_models.ImagePassage, question_models.TextPassage],
    )
    stmt = (
        select(question_models.Passage)
        .order_by(question_models.Passage.id)
        .options(loader_opt)
    )
    result = db.scalars(stmt).all()
    return result


def create_image_passage(
    db: SessionLocal, passage: question_schemas.ImagePassageCreate
) -> question_models.ImagePassage:
    passage_model = question_models.ImagePassage(
        official_test_id=passage.official_test_id,
        title=passage.title,
        p_type=PassageType.IMAGE,
        passage_image_s3_key=passage.passage_image_s3_key,
        usage=passage.usage,
        section=passage.section,
        sub_section=passage.sub_section,
    )

    db.add(passage_model)
    db.commit()

    return passage_model


def create_text_passage(
    db: SessionLocal, passage: question_schemas.TextPassageCreate
) -> question_models.TextPassage:
    passage_model = question_models.TextPassage(
        official_test_id=passage.official_test_id,
        title=passage.title,
        p_type=PassageType.TEXT,
        passage_text=passage.passage_text,
        usage=passage.usage,
        section=passage.section,
        sub_section=passage.sub_section,
    )

    db.add(passage_model)
    db.commit()

    return passage_model


def update_passage(
    db: SessionLocal,
    passage_id: int,
    passage_update: question_schemas.PassageUpdate,
    passage_class: type[question_models.Passage],
) -> question_models.Passage:
    passage_model = db.get(passage_class, passage_id)
    if not passage_model:
        raise HTTPException(400, f"Passage not found, id: {passage_id}")
    passage_data = passage_update.dict(exclude_unset=True)
    for key, value in passage_data.items():
        setattr(passage_model, key, value)

    db.add(passage_model)

    db.commit()
    return passage_model
