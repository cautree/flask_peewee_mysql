#!/usr/bin/env python2
from peewee import *

db = MySQLDatabase('students',host="localhost", port=3306)

class Student(Model):
    """A base model that will use our MySQL database"""
    username = CharField(max_length=255, unique=True)
    points = IntegerField(default=0)

    class Meta:
        database = db

def get_all_students():
	students = Student.select()

def top_student():
	student = Student.select().order_by(Student.points.desc()).get()
	return student

if __name__ =='__main__':
	db.connect()
	db.create_tables([Student], safe=True)
	#add_students()
	print ("Our top student right now is: {0.username}.".format(top_student()))
