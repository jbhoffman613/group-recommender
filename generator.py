import pymysql, config

connection = pymysql.connect(host='localhost',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor, **config.MYSQL)



