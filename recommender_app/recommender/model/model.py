from mysql.connector import (connection)
import config


cnx = connection.MySQLConnection(user=config.MYSQL['user'],
                                 password=config.MYSQL['password'],
                                 host=config.MYSQL['host'],
                                 database='partners')

cursor = cnx.cursor()
print(cursor)

# Close all connections
cursor.close()
cnx.close()
