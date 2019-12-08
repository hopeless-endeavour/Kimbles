import os

from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
# app = Flask(__name__)

# @app.route('/')
# def index():
#     headline = 'Welcome to Kimbles'
#     return render_template('index.html', headline=headline)

students = db.execute('SELECT * students').fetchall()
for i in students:
    print(i.firstName, i.lastName)
