import pymysql, csv, pandas
import config

connection = pymysql.connect(host='localhost',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor, **config.MYSQL)
csv_name = "responses.csv"

try:
    with connection.cursor() as cursor:
        creation = ["drop database if exists grs", "create database grs"]
        for query in creation:
            cursor.execute(query)
finally:
    connection.close()
    

read_csv(csv_name)