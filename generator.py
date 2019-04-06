import pymysql, config, csv

connection = pymysql.connect(host='localhost',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor, **config.MYSQL)

try:
    with connection.cursor() as cursor:
        creation = ["drop database if exists grs", "create database grs"]
        for query in creation:
            cursor.execute(query)
finally:
    connection.close()
