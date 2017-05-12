#!/usr/bin/env python2
from peewee import *
from collections import OrderedDict 
import datetime

db = MySQLDatabase('diary',host="localhost", port=3306)




class Entry(Model):
	content = TextField()
	timestamp = DateTimeField(default= datetime.datetime.now)


	class Meta:
		database = db

def initialize():
	"""Create the database and the table if they don't exisit"""
	db.connect()
	db.create_tables([Entry], safe=True)

 
def menu_loop():
	"""Show the menu"""
	choice =None
	while choice !='q':
		print("Enter 'q' to quit")
		for key, value in menu.items():
			print ('{} {}'.format(key,value.__doc__))
		choice = input('Action: ').lower().strip()

		if choice in menu:
			menu[choice]()


def add_entry():
	"""Add an entry """

def view_entries():
	"""View previous entries"""

def delete_entry(entry):
	""" delete an entry"""

menu = OrderedDict([
	('a', add_entry),
	('v',view_entries),
	]
	)

if __name__ == '__main__':
	initialize()
	menu_loop()