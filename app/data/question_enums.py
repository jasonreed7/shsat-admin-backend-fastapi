from enum import Enum


class QuestionType(Enum):
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    FILL_IN = "FILL_IN"
    MULTIPLE_CHOICE_IMAGE = "MULTIPLE_CHOICE_IMAGE"
    FILL_IN_IMAGE = "FILL_IN_IMAGE"


class UsageType(Enum):
    OFFICIAL_TEST_QUESTION = "OFFICIAL_TEST_QUESTION"
    TEST_QUESTION = "TEST_QUESTION"
    PROBLEM_SET_QUESTION = "PROBLEM_SET_QUESTION"


class QuestionOrAnswer(str, Enum):
    QUESTION = "question"
    ANSWER = "answer"


class PassageType(Enum):
    IMAGE = "IMAGE"
    TEXT = "TEXT"
