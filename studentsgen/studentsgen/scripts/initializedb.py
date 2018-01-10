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
        student1 = Student(name='Vovan', group_id=group1.id)
        student2 = Student(name='Petya', group_id=group1.id)
        student3 = Student(name='Serega', group_id=group2.id)
        student4 = Student(name='Kolyan', group_id=group2.id)

        dbsession.add(student1)
        dbsession.add(student2)
        dbsession.add(student3)
        dbsession.add(student4)

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
        course1 = Course(group_id=group1.id, professor_id=prof1.id, subject_id=sub1.id)
        course2 = Course(group_id=group1.id, professor_id=prof2.id, subject_id=sub2.id)
        course3 = Course(group_id=group2.id, professor_id=prof3.id, subject_id=sub3.id)
        course4 = Course(group_id=group2.id, professor_id=prof4.id, subject_id=sub4.id)

        dbsession.add(course1)
        dbsession.add(course2)
        dbsession.add(course3)
        dbsession.add(course4)

        dbsession.flush()
        work1 = Work(course_id=course1.id, max_point=25, name='Control Work 1')
        work2 = Work(course_id=course1.id, max_point=30, name='Control Work 2')

        dbsession.add(work1)
        dbsession.add(work2)

        dbsession.flush()
        rating1 = Rating(student_id=student1.id, work_id=work1.id, point=25)
        rating2 = Rating(student_id=student1.id, work_id=work2.id, point=25)

        dbsession.add(rating1)
        dbsession.add(rating2)