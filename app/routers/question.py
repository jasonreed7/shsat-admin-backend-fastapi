from typing import Union
from fastapi import APIRouter, Depends

from app.database import SessionLocal, get_db
from app.repositories import question_repository
from app.schemas import question as question_schemas


router = APIRouter()


@router.post("/fillInQuestion/")
def create_fill_in_question(question: question_schemas.FillInQuestionCreate, db: SessionLocal = Depends(get_db)) -> question_schemas.FillInQuestion:
    return question_repository.create_fill_in_question(db, question)


@router.post("/multipleChoiceQuestion/")
def create_fill_in_question(question: question_schemas.MultipleChoiceQuestionCreate, db: SessionLocal = Depends(get_db)) -> question_schemas.MultipleChoiceQuestion:
    return question_repository.create_multiple_choice_question(db, question)


@router.get("/questions", response_model=list[question_schemas.QuestionWithAnswers])
def get_questions(db: SessionLocal = Depends(get_db)):
    return question_repository.get_questions(db)
