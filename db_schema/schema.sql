-- Function for use in triggers to automatically update updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Enums
CREATE TYPE question_type AS ENUM ('MULTIPLE_CHOICE', 'FILL_IN');
CREATE TYPE question_usage AS ENUM ('OFFICIAL_TEST_QUESTION', 'TEST_QUESTION', 'PROBLEM_SET_QUESTION');

-- Official Test Table
CREATE TABLE official_test (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    year INT NOT NULL,
    form CHAR NOT NULL,
    created_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL,
    UNIQUE(year, form)
);

CREATE TRIGGER update_updated_at_official_test
BEFORE UPDATE ON official_test
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();

-- Question Table
CREATE TABLE question (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    official_test_id BIGINT REFERENCES official_test(id),
    official_test_question_number INT,
    q_type question_type NOT NULL,
    usage question_usage,
    created_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL
);

CREATE TRIGGER update_updated_at_question
BEFORE UPDATE ON question
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();

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
    choice_number INT CHECK (choice_number BETWEEN 1 AND 4),
    answer_text TEXT NOT NULL,
    is_correct BOOLEAN,
    created_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL,
    PRIMARY KEY (question_id, choice_number)
);

CREATE TRIGGER update_updated_at_multiple_choice_answer
BEFORE UPDATE ON multiple_choice_answer
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();

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

CREATE TRIGGER check_correct_choices_trigger
BEFORE INSERT OR UPDATE ON multiple_choice_answer
FOR EACH ROW
EXECUTE PROCEDURE check_correct_choices();

-- Category Table
CREATE TABLE category (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL
);

CREATE TRIGGER update_updated_at_category
BEFORE UPDATE ON category
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();

-- Tag Table
CREATE TABLE tag (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    category_id BIGINT REFERENCES category(id) NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL
);

CREATE TRIGGER update_updated_at_tag
BEFORE UPDATE ON tag
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();

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

CREATE TRIGGER update_updated_at_resource
BEFORE UPDATE ON resource
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();

-- Question Tag Table
CREATE TABLE question_tag (
    question_id BIGINT REFERENCES question(id),
    tag_id BIGINT REFERENCES tag(id),
    created_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT current_timestamp NOT NULL,
    PRIMARY KEY (question_id, tag_id)
);

CREATE TRIGGER update_updated_at_question_tag
BEFORE UPDATE ON question_tag
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();