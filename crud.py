from sqlalchemy import create_engine
from models import Base

engine = create_engine("postgres://postgres:kimblesreward@localhost/KimblesDB")

Base.metadata.create_all(engine)
