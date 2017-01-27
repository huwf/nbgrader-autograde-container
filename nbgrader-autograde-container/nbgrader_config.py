"""
This is a bare bones nbgrader_config file.  We assume that the student, 
instructor, and assignment will be 
"""

import os
import csv
from datetime import datetime, timedelta


print("I'm in the nbgrader config file in Docker")
c = get_config()

c.NbGrader.db_assignments = [dict(name=os.environ['ASSIGNMENT_ID'])]
c.NbGrader.db_students = [dict(id=os.environ['STUDENT_ID'])]
c.NbGrader.course_id = os.environ['COURSE_ID']
