-- Function for use in triggers to automatically update updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Enums
CREATE TYPE question_type AS ENUM (
    'MULTIPLE_CHOICE',
    'FILL_IN',
    'MULTIPLE_CHOICE_IMAGE',
    'FILL_IN_IMAGE'
);

CREATE TYPE usage_type AS ENUM (
    'OFFICIAL_TEST_QUESTION',
    'TEST_QUESTION',
    'PROBLEM_SET_QUESTION'
);

CREATE TYPE passage_type AS ENUM ('IMAGE', 'TEXT') CREATE TYPE section AS ENUM ('MATH', 'ENGLISH');

CREATE TYPE sub_section AS ENUM (
    'REVISING_EDITING',
    'READING_COMPREHENSION',
    'MATH_FILL_IN',
    'MATH_MULTIPLE_CHOICE'
);

-- Official Test Table
CREATE TABLE official_test (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    year INT NOT NULL,
    form CHAR NOT NULL,
    created_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL,
    UNIQUE(year, form)
);

CREATE TRIGGER update_updated_at_official_test BEFORE
UPDATE
    ON official_test FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

-- Question Table
CREATE TABLE question (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    official_test_id BIGINT REFERENCES official_test(id),
    official_test_question_number INT,
    q_type question_type NOT NULL,
    usage usage_type,
    section section,
    sub_section sub_section,
    created_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL
);

CREATE TRIGGER update_updated_at_question BEFORE
UPDATE
    ON question FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

CREATE TABLE text_question (
    question_id BIGINT PRIMARY KEY REFERENCES question(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    explanation TEXT NOT NULL
);

-- Fill In Question Table
CREATE TABLE fill_in_question (
    question_id BIGINT PRIMARY KEY REFERENCES text_question(question_id) ON DELETE CASCADE,
    answer NUMERIC(7, 3) NOT NULL
);

-- Multiple Choice Answer Table
CREATE TABLE multiple_choice_answer (
    question_id BIGINT REFERENCES question(id) ON DELETE CASCADE,
    choice_number INT CHECK (
        choice_number BETWEEN 1
        AND 4
    ),
    answer_text TEXT NOT NULL,
    is_correct BOOLEAN,
    created_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL,
    PRIMARY KEY (question_id, choice_number)
);

CREATE TRIGGER update_updated_at_multiple_choice_answer BEFORE
UPDATE
    ON multiple_choice_answer FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

-- Check that there is exactly one correct choice per question 
CREATE OR REPLACE FUNCTION check_correct_choices()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT COUNT(*) FROM multiple_choice_answer WHERE question_id = NEW.question_id AND is_correct = TRUE) > 1 THEN
        RAISE EXCEPTION 'More than one correct choice for question %', NEW.question_id;
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER check_correct_choices_trigger BEFORE
INSERT
    OR
UPDATE
    ON multiple_choice_answer FOR EACH ROW EXECUTE PROCEDURE check_correct_choices();

-- Image Question Table
CREATE TABLE image_question (
    question_id BIGINT PRIMARY KEY REFERENCES question(id) ON DELETE CASCADE,
    question_image_s3_key TEXT NOT NULL,
    answer_image_s3_key TEXT NOT NULL
);

-- Fill In Image Question Table
CREATE TABLE fill_in_image_question (
    question_id BIGINT PRIMARY KEY REFERENCES image_question(question_id) ON DELETE CASCADE,
    answer NUMERIC(7, 3) NOT NULL
);

-- Multiple Choice Image Question Table
CREATE TABLE multiple_choice_image_question (
    question_id BIGINT PRIMARY KEY REFERENCES image_question(question_id) ON DELETE CASCADE,
    correct_choice INT NOT NULL CHECK (
        correct_choice BETWEEN 1
        AND 4
    )
);

-- Category Table
CREATE TABLE category (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL
);

CREATE TRIGGER update_updated_at_category BEFORE
UPDATE
    ON category FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

-- Subcategory Table
CREATE TABLE subcategory (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    category_id BIGINT REFERENCES category(id) NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL
);

CREATE TRIGGER update_updated_at_subcategory BEFORE
UPDATE
    ON subcategory FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

-- Tag Table
CREATE TABLE tag (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    -- TODO: Consider delete cascade?
    subcategory_id BIGINT REFERENCES subcategory(id) NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL
);

CREATE TRIGGER update_updated_at_tag BEFORE
UPDATE
    ON tag FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

-- Resource Table
CREATE TABLE resource (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    tag_id BIGINT REFERENCES tag(id),
    name TEXT,
    url TEXT NOT NULL,
    link_text TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL
);

CREATE TRIGGER update_updated_at_resource BEFORE
UPDATE
    ON resource FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

-- Question Tag Table
CREATE TABLE question_tag (
    question_id BIGINT REFERENCES question(id) ON DELETE CASCADE,
    tag_id BIGINT REFERENCES tag(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL,
    PRIMARY KEY (question_id, tag_id)
);

CREATE TRIGGER update_updated_at_question_tag BEFORE
UPDATE
    ON question_tag FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

CREATE TABLE passage (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    official_test_id BIGINT REFERENCES official_test(id),
    title TEXT NOT NULL,
    p_type passage_type NOT NULL,
    usage usage_type,
    section section,
    sub_section sub_section,
    created_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL
);

CREATE TRIGGER update_updated_at_passage BEFORE
UPDATE
    ON passage FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

CREATE TABLE text_passage (
    passage_id BIGINT PRIMARY KEY REFERENCES passage(id) ON DELETE CASCADE,
    passage_text TEXT NOT NULL
);

CREATE TABLE image_passage (
    passage_id BIGINT PRIMARY KEY REFERENCES passage(id) ON DELETE CASCADE,
    passage_image_s3_key TEXT NOT NULL
);