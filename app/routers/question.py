import logging
import os

from fastapi import APIRouter, Depends, HTTPException, UploadFile

from app.data.env_consts import SHSAT_IMAGE_BUCKET
from app.data.question_enums import QuestionOrAnswer
from app.database import SessionLocal, get_db
from app.repositories import question_repository
from app.schemas import question as question_schemas
from utils.file_utils import (
    generate_official_question_local_image_path,
    generate_official_question_s3_image_path,
)
from utils.image_utils import process_images
from utils.s3_utils import upload_file

router = APIRouter()


@router.get("/questions", response_model=list[question_schemas.QuestionWithAnswers])
def get_questions(db: SessionLocal = Depends(get_db)):
    return question_repository.get_questions(db)


@router.post("/fillInQuestion/")
def create_fill_in_question(
    question: question_schemas.FillInQuestionCreate, db: SessionLocal = Depends(get_db)
) -> question_schemas.FillInQuestion:
    return question_repository.create_fill_in_question(db, question)


@router.post("/multipleChoiceQuestion/")
def create_multiple_choice_question(
    question: question_schemas.MultipleChoiceQuestionCreate,
    db: SessionLocal = Depends(get_db),
) -> question_schemas.MultipleChoiceQuestion:
    return question_repository.create_multiple_choice_question(db, question)


@router.post("/fillInImageQuestion/")
def create_fill_in_image_question(
    question: question_schemas.FillInImageQuestionCreate,
    db: SessionLocal = Depends(get_db),
) -> question_schemas.FillInImageQuestion:
    return question_repository.create_fill_in_question(db, question)


@router.post("/multipleChoiceImageQuestion/")
def create_multiple_image_choice_question(
    question: question_schemas.MultipleChoiceImageQuestionCreate,
    db: SessionLocal = Depends(get_db),
) -> question_schemas.MultipleChoiceImageQuestion:
    return question_repository.create_multiple_choice_image_question(db, question)


@router.post(
    "/imageQuestion/image/{official_test_year}/{official_test_form}/"
    + "{question_or_answer}/{question_number}"
)
async def create_image_question(
    files: list[UploadFile],
    official_test_year: int,
    official_test_form: str,
    question_or_answer: QuestionOrAnswer,
    question_number: int,
):
    local_image_path = generate_official_question_local_image_path(
        official_test_year, official_test_form, question_or_answer, question_number
    )
    try:
        await process_images(files, local_image_path)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Error processing image")

    image_s3_key = generate_official_question_s3_image_path(
        official_test_year, official_test_form, question_or_answer, question_number
    )

    try:
        await upload_file(local_image_path, os.getenv(SHSAT_IMAGE_BUCKET), image_s3_key)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Error uploading image to S3")

    return {"image_s3_key": image_s3_key}
