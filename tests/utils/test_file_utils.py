import os
from pathlib import Path

from app.data.env_consts import IMAGE_DIR, PROCESSED_IMAGE_DIR
from app.data.question_enums import QuestionOrAnswer
from utils.file_utils import (
    generate_official_passage_local_image_path,
    generate_official_question_local_image_path,
)


def test_generate_official_question_local_image_path():
    os.environ[IMAGE_DIR] = "/Users/testuser/Documents/shsat-admin-docs/images/"
    os.environ[PROCESSED_IMAGE_DIR] = "processed-images"
    test_year, test_form, question_or_answer, question_number = (
        2022,
        "A",
        QuestionOrAnswer.QUESTION,
        55,
    )

    image_path = generate_official_question_local_image_path(
        test_year, test_form, question_or_answer, question_number
    )

    assert image_path == Path(
        "/Users/testuser/Documents/shsat-admin-docs/"
        + "images/processed-images/2022/A/question/55.png"
    )


def test_generate_official_passage_local_image_path():
    os.environ[IMAGE_DIR] = "/Users/testuser/Documents/shsat-admin-docs/images/"
    os.environ[PROCESSED_IMAGE_DIR] = "processed-images"
    test_year, test_form, first_question_number, last_question_number = (
        2022,
        "A",
        32,
        36,
    )

    image_path = generate_official_passage_local_image_path(
        test_year, test_form, first_question_number, last_question_number
    )

    assert image_path == Path(
        "/Users/testuser/Documents/shsat-admin-docs/"
        + "images/processed-images/2022/A/passage/32_36.png"
    )
