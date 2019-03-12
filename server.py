from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL
import math

app = Flask(__name__)

app.secret_key = 'dkdew23r20'
# invoke the connectToMySQL function and pass it the name of the database we're using
# connectToMySQL returns an instance of MySQLConnection, which we will store in the variable 'mysql'
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/users/api', methods=['POST'])
def users_api():
	if not len(request.form['date_from']):
		date_from = '1999-01-01'
	else:
		date_from = request.form['date_from']

	if not len(request.form['date_to']):
		date_to = '2100-01-01'
	else:
		date_to = request.form['date_to']
	
	if not len(request.form['page_number']):
		offset = 0
	else:
		offset = 5 * int(request.form['page_number'])

	query1 = """ Select * from wall_db.users where (first_name like %(starts_with)s or last_name like %(starts_with)s )
		and created_at between %(date_from)s and %(date_to)s """
	data1 = {
		"starts_with": str(request.form['starts_with']) +"%%",
		"date_from": date_from,
		"date_to": date_to

	}
	mysql = connectToMySQL('wall_db')
	users = mysql.query_db(query1, data1)
	pages = int(math.ceil(len(users)/5))

	query2 = """ Select * from wall_db.users where (first_name like %(starts_with)s or last_name like %(starts_with)s )
		and created_at between %(date_from)s and %(date_to)s Limit 5 offset %(inc)s """
	data2 = {
		"starts_with": str(request.form['starts_with']) +"%%",
		"date_from": date_from,
		"date_to": date_to,
		"inc": offset

	}
	mysql = connectToMySQL('wall_db')
	users = mysql.query_db(query2, data2)

	return render_template('success.html', users=users, pages=pages)


if __name__ == "__main__":
	app.run(debug=True)