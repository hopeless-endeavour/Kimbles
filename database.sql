CREATE TABLE  students(
  id UNIQUE PRIMARY KEY,  # student user (brocla) ??
  firstName VARCHAR NOT NULL,
  lastName VARCHAR NOT NULL,
  class VARCHAR NOT NULL,
  tokens INTEGER DEFAULT 0
);

CREATE TABLE teachers (
  id SERIAL PRIMARY KEY,
  firstName VARCHAR NOT NULL,
  lastName VARCHAR NOT NULL
);

CREATE TABLE transactions(
  id SERIAL PRIMARY KEY,
  sender REFERENCES teachers(id),
  recipient REFERENCES students(id),
  amount INTEGER NOT NULL
)

INSERT INTO students (firstName, lastName, year) VALUES ('Lucas', 'Brown', 12)
INSERT INTO teachers (firstName, lastName) VALUES ('Barry', 'Harris')
