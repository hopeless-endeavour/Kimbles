from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    firstName = Column(String)
    lastName = Column(String)
    classCode = Column(String)
    # user = lastName[:2]+firstName[:2]
    tokens = Column(Integer)

    def __repr__(self):
        return "<Student(firstName='{}', lastName='{}', classCode='{}', tokens='{}')>"\
                .format(self.firstName, self.lastName, self.classCode, self.tokens)


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    firstName = Column(String)
    lastName = Column(String)
    # user = lastName[:2]+firstName[:2]

    def __repr__(self):
        return "<Teacher(firstName='{}', lastName='{}')>"\
                .format(self.firstName, self.lastName)


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    sender = Column(String)  # ForeignKey() schema
    recipient = Column(String)
    amount = Column(Integer)

    def __repr__(self):
        return "<Transaction(sender='{} recipient='{}', amount='{}')>"\
                .format(self.sender, self.recipient, self.amount)
