import MySQLdb

# mysql --user=root -p
def connection():
    conn = MySQLdb.connect(	host="db4free.net", 	# your host, usually localhost
                     		user="expenseadmin", 		# your username
                     		passwd="abcd1234", 		# your password
                     		db="expensemonitor" ) 		# name of the data base
    c = conn.cursor()

    return c, conn

# # mysql --user=root -p
# def connection():
#     conn = MySQLdb.connect(	host="localhost", 	# your host, usually localhost
#                      		user="root", 		# your username
#                      		passwd="root", 		# your password
#                      		db="test" ) 		# name of the data base
#     c = conn.cursor()

#     return c, conn


# def connection():
#     conn = MySQLdb.connect(	host="sql12.freemysqlhosting.net", 	# your host, usually localhost
#                      		user="sql12253990", 		# your username
#                      		passwd="hWcveisvbL", 		# your password
#                      		db="sql12253990" ) 		# name of the data base
#     c = conn.cursor()

#     return c, conn