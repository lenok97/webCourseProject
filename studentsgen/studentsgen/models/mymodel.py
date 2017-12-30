from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    Date,
    ForeignKey
)
from sqlalchemy.schema import Table

from .meta import Base

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    def __repr__(self):
        return "<Student(%r)>" % (self.name)

class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    def __repr__(self):
        return "<Teacher(%r)>" % (self.name)

class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    def __repr__(self):
        return "<Subject(%r)>" % (self.name)

class Work(Base):
    __tablename__ = 'work'
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey('subject.id'))
    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    name = Column(String)
    max_point= Column(Integer)
    def __repr__(self):
        return "<Work(%r)>" % (self.name)

RecordBook = Table('record_book', Base.metadata,
    Column('student_id', Integer, ForeignKey('student.id')),
    Column('work_id', Integer, ForeignKey('work.id')),
    Column('date', Date),
    Column('point', Integer)
)