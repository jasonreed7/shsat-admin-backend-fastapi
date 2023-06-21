import os
from pathlib import Path

from app.data.env_consts import IMAGE_DIR, PROCESSED_IMAGE_DIR
from app.data.question_enums import QuestionOrAnswer


def generate_official_question_local_image_path(test_year: int, test_form: str, question_or_answer: QuestionOrAnswer, question_number: int) -> Path:
    relative_path = generate_official_question_image_path(
        test_year, test_form, question_or_answer, question_number)
    return Path(os.getenv(IMAGE_DIR)).joinpath(os.getenv(PROCESSED_IMAGE_DIR)).joinpath(relative_path).expanduser()

def generate_official_question_s3_image_path(test_year: int, test_form: str, question_or_answer: QuestionOrAnswer, question_number: int) -> str:
    return f"test-images/{test_year}/{test_form}/{question_or_answer.value}/{question_number}.png"

def generate_official_question_image_path(test_year: int, test_form: str, question_or_answer: QuestionOrAnswer, question_number: int) -> Path:
    return Path(str(test_year)).joinpath(test_form).joinpath(question_or_answer.value).joinpath(f"{question_number}.png")

def generate_official_passage_local_image_path(test_year: int, test_form: str, first_question_number: int, last_question_number: int) -> Path:
    relative_path = generate_official_passage_image_path(
        test_year, test_form, first_question_number, last_question_number)
    return Path(os.getenv(IMAGE_DIR)).joinpath(os.getenv(PROCESSED_IMAGE_DIR)).joinpath(relative_path).expanduser()

def generate_official_passage_s3_image_path(test_year: int, test_form: str, first_question_number: int, last_question_number: int) -> str:
    return f"test-images/{test_year}/{test_form}/passage/{first_question_number}_{last_question_number}.png"

def generate_official_passage_image_path(test_year: int, test_form: str, first_question_number: int, last_question_number: int) -> Path:
    return Path(str(test_year)).joinpath(test_form).joinpath("passage").joinpath(f"{first_question_number}_{last_question_number}.png")