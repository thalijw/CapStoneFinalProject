#!/usr/bin/python
# _*_ coding: utf-8 _*_

import psycopg2
import sys
import getpass
from subprocess import call
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import connect
from psycopg2 import extras

# Getting the user's default device username
user = getpass.getuser()

con = None

# call (["ls"])
# call (["pwd"])
# call (["lunchy start postgres"])
# call (["createdb testDB"])
# call (["psql testDB"])

def Add_Row(table):

	query = "SELECT * FROM " + table
	cur.execute(query)
	col_names = [cn[0] for cn in cur.description]
	Col_number = 0
	for cn in cur.description:
		Col_number += 1
	Entry_List = []
	for i in range(Col_number-1):
		var = raw_input("Please enter a value for " + col_names[i+1] + " : ")
		Entry_List.append(var)

	query = "SELECT MAX(id) FROM cars"
	cur.execute(query)
	answer = cur.fetchall()
	Next_ID = int(answer[0][0]) + 1

	#print Entry_List
	query = "INSERT INTO " + table + " ( id, "
	for i in range(Col_number-1):
		if i < Col_number-2:
			query = query +  col_names[i+1] + ","
		else:
			query = query +  col_names[i+1]
	query = query + ") VALUES (" + str(Next_ID) + ","

	#query = "INSERT INTO " + table + " VALUES ("
	for i in range(Col_number-1):
		if i < Col_number -2:
			query = query + "'" + Entry_List[i] + "'" + ","
		else:
			query = query + "'" + Entry_List[i]+ "'" 
	query = query + ")"
	cur.execute(query)
	con.commit()

	query = "SELECT * FROM " + table
	cur.execute(query)
	col_names = [cn[0] for cn in cur.description]

	for i in range(Col_number ):
		print "%-*s"%(15,col_names[i]),
	print "\n------------------------------------------------------------"
	rows = cur.fetchall()
	for row in rows:
		for i in range(Col_number ):
			print "%-*s"%(15,row[i]),
		print "\n"

def Edit_Row(table):

	query = "SELECT * FROM " + table
	cur.execute(query)
	col_names = [cn[0] for cn in cur.description]
	Col_number = 0
	for cn in cur.description:
		Col_number += 1
	for i in range(Col_number):
		print "%-*s"%(15,col_names[i]),
	print "\n------------------------------------------------------------"
	rows = cur.fetchall()
	for row in rows:
		for i in range(Col_number):
			print "%-*s"%(15,row[i]),
		print "\n"
	Col_ID = raw_input("Please enter the column ID : ")
	Update_col = raw_input("Please enter the column name to Update : ")
	Update_val = raw_input("Please enter the new value : ")

	# for row in rows:
	# 	if row[0] == Col_ID:

	# for i in range(Col_number):
	# 	var = raw_input("Please enter a value for " + col_names[i] + " : ")
	# 	Entry_List.append(var)

	if Update_val.isdigit():
		query = "UPDATE " + table + " SET " + Update_col + "=" + Update_val + " WHERE " + col_names[0] + "='" + Col_ID + "'" 
	else:
		query = "UPDATE " + table + " SET " + Update_col + "='" + Update_val + "' WHERE " + col_names[0] + "='" + Col_ID + "'" 
	cur.execute(query)
	con.commit()

	query = "SELECT * FROM " + table
	cur.execute(query)
	col_names = [cn[0] for cn in cur.description]

	for i in range(Col_number ):
		print "%-*s"%(15,col_names[i]),
	print "\n------------------------------------------------------------"
	rows = cur.fetchall()
	for row in rows:
		for i in range(Col_number ):
			print "%-*s"%(15,row[i]),
		print "\n"

def Delete_Row(table):

	query = "SELECT * FROM " + table
	cur.execute(query)
	col_names = [cn[0] for cn in cur.description]
	Col_number = 0
	for cn in cur.description:
		Col_number += 1
	for i in range(Col_number):
		print "%-*s"%(15,col_names[i]),
	print "\n------------------------------------------------------------"
	rows = cur.fetchall()
	for row in rows:
		for i in range(Col_number):
			print "%-*s"%(15,row[i]),
		print "\n"
	Row_ID = raw_input("Please enter the row ID to be deleted: ")

	query = "DELETE FROM " + table + " WHERE id =" + Row_ID 

	cur.execute(query)
	con.commit()
	if cur.rowcount > 0:
		print str(cur.rowcount) + "Row has been deleted!"
	else:
		print "No matching rows to delete !!"

	query = "SELECT * FROM " + table
	cur.execute(query)
	col_names = [cn[0] for cn in cur.description]

	for i in range(Col_number ):
		print "%-*s"%(15,col_names[i]),
	print "\n------------------------------------------------------------"
	rows = cur.fetchall()
	for row in rows:
		for i in range(Col_number ):
			print "%-*s"%(15,row[i]),
		print "\n"

def Select_Table():

	cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
	rows = cur.fetchall()
	count = 1
	for row in rows:
		print row[0]
		count += 1
	#print "Number of rows: %d" % cur.rowcount
	print "\n"
	table =  raw_input("Select a table name : ")
	for row in rows:
		if row[0] == table:
			#print "View", table
			query = "SELECT * FROM " + table
			cur.execute(query)
			Col_number = 0
			for cn in cur.description:
				Col_number += 1
			col_names = [cn[0] for cn in cur.description]
			for i in range(Col_number):
				print "%-*s"%(15,col_names[i]),
			print "\n------------------------------------------------------------"
			rows = cur.fetchall()
			for row in rows:
				for i in range(Col_number):
					print "%-*s"%(15,row[i]),
				print "\n"
	exit_table = 0
	while exit_table == 0:
		print "Select from the following menu:"
		print "1. Add a row"
		print "2. Edit a row"
		print "3. Delete a row"
		print "4. Exit"
		Select_choice =  int(raw_input("Enter Choice (1,2 or 3): "))

		if Select_choice == 1:
			Add_Row(table)
		elif Select_choice == 2:
			Edit_Row(table)
		elif Select_choice == 3:
			Delete_Row(table)
		elif Select_choice == 4:
			# Exit_Funciton()
			exit_table = 1
		else:
			print "Invalid Input !!"

def Drop_Table():

	cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
	rows = cur.fetchall()
	count = 1
	for row in rows:
		print row[0]
		count += 1
	table =  raw_input("Select a table name to delete : ")
	delete_flag = 0
	for row in rows:
		if row[0] == table:
			delete_flag += 1

	if delete_flag == 1:
		query = "DROP TABLE " + table
		cur.execute(query)
		con.commit
		print "The table (" + table + ") Successfully deleted!"
	else:
		print "No matching table to delete!"

	cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
	rows = cur.fetchall()
	count = 1
	for row in rows:
		print row[0]
		count += 1

def Create_Table():
	print "create table here!"
	print "Create table example:"
	print "CREATE TABLE {table name} (" 
	print "ID      int,"                
	print "name    varchar(80),"        
	print "date    date,"        		
	print "count   int )" 

	Table_name = raw_input("Enter Table name: ")
	Num_columns = int(raw_input("Enter the number of columns: "))
	Column_names = []
	Column_types = []
	for i in range(Num_columns):
		var1 = raw_input("Enter Column name: ")
		Column_names.append(var1)
		var2 = raw_input("Enter Column type: ")
		Column_types.append(var2)

	query = "CREATE TABLE " + Table_name + "( ID   SERIAL PRIMARY KEY, "

	for i in range(Num_columns):
		if i < Num_columns -1:
			query = query + Column_names[i] + "   " + Column_types[i] + ","
		else:
			query = query + Column_names[i] + "   " + Column_types[i]
	query = query + ");"
	cur.execute(query)
	con.commit()

	cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
	rows = cur.fetchall()
	count = 1
	for row in rows:
		print row[0]
		count += 1

def Exit_Funciton():
	print "Exit Program here, Goodby!"
	sys.exit(0)

try:

	dbname = "postgresdb3"
	con = connect(dbname = dbname , user=user, host = 'localhost')

	

	con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
	#query = "SELECT * from pg_catalog.pg_database where datname =" + dbname 
	cur.execute("select * from pg_database where datname = %(dname)s", {'dname': dbname })
	answer = cur.fetchall()

	if len(answer) > 0:
		print "Database exists"
		
	else:
		cur.execute('CREATE DATABASE ' + dbname + " OWNER " + user)
	# cur.close()
	# con.close()
	cur.execute("SELECT * FROM pg_catalog.pg_tables WHERE tablename  = 'weather'")
	answer = cur.fetchall()

	if len(answer) > 0:
		print "Weather table exists"
		
	else:
		print "Weather table does not exist"
		query = "CREATE TABLE weather ( ID   SERIAL PRIMARY KEY, city varchar(80), temp int, prcp real, date date);"
		cur.execute(query)
		path = "/Users/"+user+"/Desktop/weather.txt"
		query = "COPY weather FROM '" + path + "';"
		print "weather Path "+ path
		#query = "INSERT INTO weather (city,temp,prcp,date) VALUES ('San Fransisco', 30, 0.10, '2005-10-09')"
		cur.execute(query)

	cur.execute("SELECT * FROM pg_catalog.pg_tables WHERE tablename  = 'cars'")
	answer = cur.fetchall()

	if len(answer) > 0:
		print "cars table exists"
		
	else:
		print "cars table does not exist"
		query = "CREATE TABLE cars ( ID   SERIAL PRIMARY KEY, name varchar(80), model int, year int);"
		cur.execute(query)
		path = "/Users/"+user+"/Desktop/cars.txt"
		print "car Path "+ path
		query = "COPY cars FROM '" + path + "';"
		cur.execute(query)

	cur.execute("SELECT * FROM pg_catalog.pg_tables WHERE tablename  = 'states'")
	answer = cur.fetchall()

	if len(answer) > 0:
		print "states table exists"
		
	else:
		print "states table does not exist"	
		query = "CREATE TABLE states ( ID   SERIAL PRIMARY KEY, name varchar(80), population int, capital varchar(80));"
		cur.execute(query)
		path = "/Users/"+user+"/Desktop/states.txt"
		query = "COPY states FROM '" + path + "';"
		cur.execute(query)

	con.commit()
	# con = psycopg2.connect(database=dbname, user=user)
	# cur = con.cursor()
	exit_app = 0
	while exit_app == 0:
		print "\nPlease select an option from the menu:"
		print "1. View database tables"
		print "2. Create a table"
		print "3. Delete a table"
		print "4. Exit"
		choice = int(raw_input('Enter choice: '))

		if choice == 1:
			Select_Table()
		elif choice == 2:
			Create_Table()
		elif choice == 3:
			Drop_Table()
		elif choice == 4:
			Exit_Funciton()
		else:
			print "Invalid Input !!"

except psycopg2.DatabaseError, e:

	if con:
		con.rollback()

	print 'Error %s' % e
	sys.exit(1)

finally:

	if con:
		con.close()