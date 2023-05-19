from sqlalchemy import select
from sqlalchemy.orm import selectin_polymorphic
from app.database import SessionLocal
from app.models import question as question_models
from app.schemas import question as question_schemas

def get_questions(db: SessionLocal):
    loader_opt = selectin_polymorphic(question_models.Question, [question_models.FillInQuestion, question_models.MultipleChoiceQuestion])
    stmt = select(question_models.Question).order_by(question_models.Question.id).options(loader_opt)
    result = db.scalars(stmt).all()
    return result

def create_fill_in_question(db: SessionLocal, question: question_schemas.FillInQuestionCreate):
    question_model = question_models.FillInQuestion(
        official_test_id=question.official_test_id,
        official_test_question_number=question.official_test_question_number,
        question_text=question.question_text,
        q_type=question.q_type,
        explanation=question.explanation,
        usage=question.usage,
        answer=question.answer
    )

    db.add(question_model)
    db.commit()

    return question_model

def create_multiple_choice_question(db: SessionLocal, question: question_schemas.MultipleChoiceQuestionCreate):
    question_model = question_models.MultipleChoiceQuestion(
        official_test_id=question.official_test_id,
        official_test_question_number=question.official_test_question_number,
        question_text=question.question_text,
        q_type=question.q_type,
        explanation=question.explanation,
        usage=question.usage
    )

    for answer in question.answers:
        answer_model = question_models.MultipleChoiceAnswer(
            choice_number=answer.choice_number,
            answer_text = answer.answer_text,
            is_correct = answer.is_correct
        )

        question_model.answers.append(answer_model)
        
    db.add(question_model)
    db.commit()

    return question_model

