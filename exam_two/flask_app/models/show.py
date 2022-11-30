from flask_app.config.connector import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import user


class tvShow:
	DB = "tv_shows"
	def __init__(self,data):
		self.id = data['id']
		self.title = data['title']
		self.network = data['network']
		self.release_date = data['release_date']
		self.description = data['description']
		self.likes = data['likes']
		self.created_at = data['created_at']
		self.updated_at = data['updated_at']
		self.user_id = data['user_id']

		self.creator = None


	@classmethod
	def likes(cls,data,counter):
		query = "INSERT INTO show (likes) VALUES (%(counter)s) WHERE id = %(id)s;"
		result = connectToMySQL(cls.DB).query_db(query,data)
		return result


	@classmethod
	def save(cls,data):
		query = "INSERT INTO shows (title, network, release_date, description, created_at, user_id) VALUES ( %(title)s, %(network)s, %(release_date)s, %(description)s, NOW(), %(user_id)s );"
		result = connectToMySQL(cls.DB).query_db(query,data)
		return result

	@classmethod
	def get_by_id(cls,show_id):
		query = "SELECT * FROM shows WHERE id = %(id)s;"
		result = connectToMySQL(cls.DB).query_db(query,show_id)
		if result:
			show = cls(result[0])
			return show
		return False


	@classmethod
	def get_all_by_user(cls):
		query = "SELECT * FROM users JOIN shows ON users.id = shows.id WHERE user.id = %(id)s;"
		result = connectToMySQL(cls.DB).query_db(query)
		show_list = []
		for row in result:
			show_list.append(cls(row))

		return show_list


	@classmethod
	def get_all(cls):
		query = "SELECT * FROM shows;"

		result = connectToMySQL(cls.DB).query_db(query)
		show_list = []
		for row in result:
			show_list.append(cls(row))
		return show_list


	@classmethod
	def update(cls,data):
		print(data)
		query = "UPDATE shows SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, description = %(description)s WHERE id = %(id)s;"

		result = connectToMySQL(cls.DB).query_db(query,data)
		return result

	@classmethod
	def delete(cls,data):
		query = "DELETE FROM shows WHERE id = %(id)s;"
		result = connectToMySQL(cls.DB).query_db(query,data)
		return result


	@classmethod
	def show(cls,data):
		query = "SELECT * FROM shows WHERE id = %(id)s;"
		result = connectToMySQL(cls.DB).query_db(query,data)
		return result



	# "created_at": row['created_at'] and "updated_at": row['updated_at'] were causing the issue. users.created_at and users.updated_at had to be changed for the error to go away. Why? still not sure. idk if this is my issue for if the learn platform has an error. either way, it works now i guess.
	@classmethod
	def get_shows_with_creator(cls):
		query = "SELECT * FROM shows LEFT JOIN users ON shows.user_id = users.id;"
		result = connectToMySQL("tv_shows").query_db(query)
		all_shows = []
		print(result)
		for row in result:
			one_show = cls(row)

			one_show_user_info = {
				"id": row['users.id'],
				"first_name": row['first_name'],
				"last_name": row['last_name'],
				"email": row['email'],
				"password": row['password'],
				"created_at": row['users.created_at'],
				"updated_at": row['users.updated_at']
			}

			author = user.User(one_show_user_info)

			one_show.creator = author

			all_shows.append(one_show)
		return all_shows
