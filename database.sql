CREATE TABLE  students(
  id SERIAL PRIMARY KEY,
  firstname VARCHAR NOT NULL,
  lastname VARCHAR NOT NULL,
  username VARCHAR UNIQUE NOT NULL,
  password TEXT NOT NULL,
  classcode VARCHAR NOT NULL,
  tokens INTEGER DEFAULT 0
);

CREATE TABLE teachers (
  id SERIAL PRIMARY KEY,
  firstname VARCHAR NOT NULL,
  lastname VARCHAR NOT NULL,
  username VARCHAR UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE transactions(
  id SERIAL PRIMARY KEY,
  sender REFERENCES teachers(id),
  recipient REFERENCES students(id),
  amount INTEGER NOT NULL
);
