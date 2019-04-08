import pymysql, config, input_reader, pandas as pd

connection = pymysql.connect(host='localhost',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor, **config.MYSQL)

try:
    with connection.cursor() as cursor:
        creation = ["DROP DATABASE IF EXISTS partners", "CREATE database partners", "USE partners"]
        for query in creation:
            cursor.execute(query)
        for name, table in input_reader.read_csv(config.csv_name).items():
            type = lambda col: col + ' ' + config.column_types[name][col]
            columns = ', '.join([type(col.lower()) for col in table.columns])
            table_creation = ["DROP TABLE IF EXISTS {}".format(name),
                              "CREATE TABLE {} ({})".format(name, columns)]
            print(table_creation)
            print(len(table.columns))
            for query in table_creation:
                cursor.execute(query)
            sval = lambda val: "'" + val + "'" if isinstance(val, str) else str(val)
            values = ', '.join(['(' + ', '.join([sval(val) for val in list(row.values)]) + ')'
                                for _, row in table.iterrows()])
            value_inserter = "INSERT INTO {} VALUES {}".format(name, values)
            print(value_inserter)
            cursor.execute(value_inserter)
            break

finally:
    connection.close()