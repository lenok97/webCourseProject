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
Base = declarative_base()

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('group.id'))
    name = Column(String(100), nullable=False)
    def __repr__(self):
        return "<Student(%r)>" % (self.name)

class Professor(Base):
    __tablename__ = 'professor'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    def __repr__(self):
        return "<Professor(%r)>" % (self.name)

class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    def __repr__(self):
        return "<Subject(%r)>" % (self.name)

class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    def __repr__(self):
        return "<Group(%r)>" % (self.name)

class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey('subject.id'))
    group_id = Column(Integer, ForeignKey('group.id'))
    professor_id = Column(Integer, ForeignKey('professor.id'))
    def __repr__(self):
        return "<Course>"

class Work(Base):
    __tablename__ = 'work'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'))
    name = Column(String)
    max_point= Column(Integer)
    def __repr__(self):
        return "<Work(%r)>" % (self.name)

class Rating(Base):
    __tablename__ = 'record_book'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    work_id = Column(Integer, ForeignKey('work.id'))
    data = Column(Date)
    point = Column(Integer)
    def __repr_(self):
        return "<Rating(%r, %r)>" % (self.data, point)