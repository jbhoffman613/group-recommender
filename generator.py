import pymysql

connection = pymysql.connect(host='localhost',
                             user='hbp',
                             password='hbp2018',
                             db='dogDB',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
