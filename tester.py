

import mysql.connector
import sys


def main():
	print("COnnecting")
	cnx = mysql.connector.connect(user='matt', password='Sup3rDup3rC@li', host='3.86.145.6', database = 'dsci551', 
		auth_plugin = 'mysql_native_password')
	cursor = cnx.cursor()

	print("Connected")
	# # for param in parameters:

	# query_table = "`" + table_name + "`"

	# example
	# query = (select * from table where param between %s and %s)
	# cursor.execute(query, (firstchecker, secondchecker))
	
	# query = ("select " + param + ", COUNT(*) from " + query_table + " GROUP BY " + param + " HAVING COUNT(*) > 1 ORDER BY COUNT(*) DESC limit 5;")
	print("Query Execution")
	query = ("SELECT * FROM rent_scores limit 1;" )
	cursor.execute(query)

	print("Printing Results")
	# print(query)
	# checker = False
	for item in cursor:
		print(item)
		break
	cursor.close()
	cnx.close()

		

if __name__ == '__main__':
	main()
	# i-0ca0ce1af5e7f5c12