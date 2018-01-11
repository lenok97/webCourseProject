import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models import Student, Professor, Subject, Group, Course, Work, Rating


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        group1 = Group(name='Group 1')
        group2 = Group(name='Group 2')

        dbsession.add(group1)
        dbsession.add(group2)

        dbsession.flush()
        student=[]
        student.append(Student(name='Vovan', group_id=group1.id))
        student.append(Student(name='Petya', group_id=group1.id))
        student.append(Student(name='Serega', group_id=group1.id))
        student.append(Student(name='Kolyan', group_id=group1.id))
        student.append(Student(name='Harry', group_id=group1.id))
        student.append(Student(name='Petya', group_id=group2.id))
        student.append(Student(name='Serega', group_id=group2.id))
        student.append(Student(name='Kolyan', group_id=group2.id))
        student.append(Student(name='Harry', group_id=group2.id))
        student.append(Student(name='Vasiliy', group_id=group2.id))

        for s in student:
            dbsession.add(s)

        dbsession.flush()
        prof1 = Professor(name='Mr White')
        prof2 = Professor(name='Mr Black')
        prof3 = Professor(name='Mr Brown')
        prof4 = Professor(name='Mr Pink')

        dbsession.add(prof1)
        dbsession.add(prof2)
        dbsession.add(prof3)
        dbsession.add(prof4)

        sub1 = Subject(name='Math')
        sub2 = Subject(name='Physics')
        sub3 = Subject(name='Programming')
        sub4 = Subject(name='History')

        dbsession.add(sub1)
        dbsession.add(sub2)
        dbsession.add(sub3)
        dbsession.add(sub4)

        dbsession.flush()
        course=[]
        course.append(Course(group_id=group1.id, professor_id=prof1.id, subject_id=sub1.id))
        course.append(Course(group_id=group1.id, professor_id=prof2.id, subject_id=sub2.id))
        course.append(Course(group_id=group1.id, professor_id=prof3.id, subject_id=sub3.id))
        course.append(Course(group_id=group1.id, professor_id=prof4.id, subject_id=sub4.id))
        course.append(Course(group_id=group1.id, professor_id=prof1.id, subject_id=sub1.id))
        course.append(Course(group_id=group2.id, professor_id=prof2.id, subject_id=sub2.id))
        course.append(Course(group_id=group2.id, professor_id=prof3.id, subject_id=sub3.id))
        course.append(Course(group_id=group2.id, professor_id=prof4.id, subject_id=sub4.id))
        course.append(Course(group_id=group2.id, professor_id=prof1.id, subject_id=sub1.id))
        course.append(Course(group_id=group2.id, professor_id=prof4.id, subject_id=sub4.id))

        for c in course:
            dbsession.add(c)

        dbsession.flush()
        work=[]
        work.append(Work(course_id=course[0].id, max_point=25, name='Control Work 1'))
        work.append(Work(course_id=course[0].id, max_point=30, name='Control Work 2'))
        work.append(Work(course_id=course[1].id, max_point=30, name='Control Work 3'))
        work.append(Work(course_id=course[1].id, max_point=30, name='Control Work 4'))
        work.append(Work(course_id=course[2].id, max_point=30, name='Control Work 5'))
        work.append(Work(course_id=course[3].id, max_point=25, name='Control Work 6'))
        work.append(Work(course_id=course[4].id, max_point=30, name='Control Work 7'))
        work.append(Work(course_id=course[5].id, max_point=30, name='Control Work 8'))
        work.append(Work(course_id=course[6].id, max_point=30, name='Control Work 9'))
        work.append(Work(course_id=course[7].id, max_point=30, name='Control Work 10'))
        work.append(Work(course_id=course[8].id, max_point=25, name='Control Work 11'))
        work.append(Work(course_id=course[8].id, max_point=30, name='Control Work 12'))
        work.append(Work(course_id=course[9].id, max_point=30, name='Control Work 13'))
        work.append(Work(course_id=course[9].id, max_point=30, name='Control Work 14'))
        work.append(Work(course_id=course[9].id, max_point=30, name='Control Work 15'))

        for w in work:
            dbsession.add(w)

        dbsession.flush()
        rating=[]
        rating.append(Rating(student_id=student[0].id, work_id=work[0].id, point=15))
        rating.append(Rating(student_id=student[0].id, work_id=work[1].id, point=25))
        rating.append(Rating(student_id=student[1].id, work_id=work[2].id, point=24))
        rating.append(Rating(student_id=student[2].id, work_id=work[3].id, point=15))
        rating.append(Rating(student_id=student[3].id, work_id=work[4].id, point=25))
        rating.append(Rating(student_id=student[4].id, work_id=work[5].id, point=20))
        rating.append(Rating(student_id=student[4].id, work_id=work[6].id, point=25))
        for r in rating:
            dbsession.add(r)
