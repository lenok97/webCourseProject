import datetime
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    DateTime,
    ForeignKey,
    Unicode
)
from sqlalchemy.schema import Table
from .meta import Base
from passlib.apps import custom_app_context as pwd_context


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

    def set_maxpoint(self, point):
        self.max_point = point


class Rating(Base):
    __tablename__ = 'record_book'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    work_id = Column(Integer, ForeignKey('work.id'))
    date = Column(DateTime, default=datetime.datetime.utcnow)
    point = Column(Integer)
    def __repr_(self):
        return "<Rating(%r, %r)>" % (self.data, point)

    def set_point(self, point):
        self.point = point

    def set_student(self, id):
        self.student_id = id

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), nullable=False)
    last_logged = Column(DateTime, default=datetime.datetime.utcnow)

    def verify_password(self, password):
        # is it cleartext?
        if password == self.password:
            self.set_password(password)

        return "<User(%r, %r)>" %(password, self.password)

    def set_password(self, password):
        password_hash = pwd_context.encrypt(password)
        self.password = password_hash