import pymysql, csv
from . import config

connection = pymysql.connect(host='localhost',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor, **config.MYSQL)
csv_name = "Group Recommender - Data Collection (Responses) - Form Responses 1.csv"

try:
    with connection.cursor() as cursor:
        creation = ["drop database if exists grs", "create database grs"]
        for query in creation:
            cursor.execute(query)
finally:
    connection.close()
    
def read_csv(csv_file_name):
    with open(csv_file_name, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            print(', '.join(row))

read_csv(csv_name)