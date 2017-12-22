from sqlalchemy import create_engine, func, select
from sqlalchemy import MetaData,Column
from sqlalchemy import Integer, String, Numeric, ForeignKey, Date
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import aliased
from sqlalchemy.schema import Table

import os

metaData = MetaData()
engine = create_engine("sqlite:///studentGen.db")
base = declarative_base()

class Student(base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    def __repr__(self):
        return "<Student(%r)>" % (self.name)

class Teacher(base):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    def __repr__(self):
        return "<Teacher(%r)>" % (self.name)

class Subject(base):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    def __repr__(self):
        return "<Subject(%r)>" % (self.name)

class Work(base):
    __tablename__ = 'work'
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey('subject.id'))
    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    name = Column(String)
    max_point= Column(Integer)
    def __repr__(self):
        return "<Work(%r)>" % (self.name)

RecordBook = Table('record_book', base.metadata,
    Column('student_id', Integer, ForeignKey('student.id')),
    Column('work_id', Integer, ForeignKey('work.id')),
    Column('date', Date),
    Column('point', Integer)
)