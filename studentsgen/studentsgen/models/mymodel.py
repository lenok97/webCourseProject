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
from sqlalchemy.orm import relationship

import bcrypt


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('group.id'))
    name = Column(String(100), nullable=False)

    ratings = relationship('Rating', backref='student')

    def __repr__(self):
        return "<Student(%r)>" % (self.name)

class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    students = relationship('Student', backref='group')
    courses = relationship('Course', backref='group')

    def __repr__(self):
        return "<Group(%r)>" % (self.name)

class Professor(Base):
    __tablename__ = 'professor'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    courses = relationship('Course', backref='professor')

    def __repr__(self):
        return "<Professor(%r)>" % (self.name)

class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    courses = relationship('Course', backref='subject')

    def __repr__(self):
        return "<Subject(%r)>" % (self.name)

class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey('subject.id'))
    group_id = Column(Integer, ForeignKey('group.id'))
    professor_id = Column(Integer, ForeignKey('professor.id'))

    works = relationship('Work', backref='course')

    def __repr__(self):
        return "<Course>"

class Work(Base):
    __tablename__ = 'work'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'))
    name = Column(String)
    max_point= Column(Integer)

    ratings = relationship('Rating', backref='work')
    
    def __repr__(self):
        return "<Work(%r)>" % (self.name)

class Rating(Base):
    __tablename__ = 'record_book'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    work_id = Column(Integer, ForeignKey('work.id'))
    date = Column(DateTime, default=datetime.datetime.utcnow)
    point = Column(Integer)
    
    def __repr_(self):
        return "<Rating(%r, %r)>" % (self.data, point)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    role = Column(Text, nullable=False)
    password_hash = Column(Text)

    def set_password(self, pw):
        pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        self.password_hash = pwhash.decode('utf8')

    def set_role(self, role):
        self.role = role

    def check_password(self, pw):
        if self.password_hash is not None:
            expected_hash = self.password_hash.encode('utf8')
            return bcrypt.checkpw(pw.encode('utf8'), expected_hash)
        return False