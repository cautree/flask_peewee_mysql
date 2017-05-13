import datetime
from peewee import *
from flask.ext.login import UserMixin

DATABASE= MySQLDatabase('social',host="localhost", port=3306)

class User(UserMixin, Model):
	username = CharField(unique=True)
	email = CharField(unique=True)
	password = CharField(max_length=100)
	joined_at = DateTimeField(default=datetime.datetime.now)
	is_admin = BooleanField(default=False)


	class Meta:
		database = DATABASE
		order_by = ('-joined_at',)



