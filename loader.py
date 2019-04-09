import pymysql, config, input_reader, sys

column_types = {'user': {'user_id': 'int primary key', 'name': 'varchar(25) NOT NULL', 'email': 'varchar(255) NOT NULL',
                         'phone_number': 'varchar(100) NULL', 'year': 'int NOT NULL', 'grade': 'double(4,1)'},
                'skill': {'skill_id': 'int primary key', 'skill_name': 'varchar(255) NOT NULL'},
                'skillset': {'user_id': 'int NOT NULL', 'skill_id': 'int NOT NULL', 'value': 'varchar(25) NOT NULL'},
                'interest_id': {'interest_id': 'int primary key', 'interest_name': 'varchar(100) NOT NULL'},
                'user_interest': {'user_id': 'int NOT NULL', 'interest_id': 'int NOT NULL'},
                'team_preference': {'user_id': 'int NOT NULL', 'user_prefers': 'int NOT NULL'},
                'team': {'user_id': 'int NOT NULL', 'group_id': 'int NOT NULL'},
                'availability': {'availability_id': 'int primary key', 'user_id': 'int',
                                 'day': "ENUM('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')",
                                 'start': 'TIME', 'end': 'TIME'},
                'project_group': {'group_id': 'int primary key', 'group_name': 'varchar(25)'},
                'group_member': {'group_id': 'int', 'user_id': 'int'}

                }

connection = pymysql.connect(host='localhost',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor, **config.MYSQL)

try:
    with connection.cursor() as cursor:
        creation = ["DROP DATABASE IF EXISTS partners", "CREATE database partners", "USE partners"]


        def execute(q):
            try:
                cursor.execute(q)
            except Exception as e:
                print(e, ':', q)
                connection.close()
                sys.exit(1)


        for query in creation:
            execute(query)
        for name, table in input_reader.read_csv(config.csv_name).items():
            type = lambda col: col + ' ' + column_types[name][col]
            columns = ', '.join([type(col.lower()) for col in table.columns])
            table_creation = ["DROP TABLE IF EXISTS {}".format(name),
                              "CREATE TABLE {} ({})".format(name, columns)]
            for query in table_creation:
                execute(query)
            sval = lambda val: "'" + val + "'" if isinstance(val, str) else str(val)
            values = ', '.join(['(' + ', '.join([sval(val) for val in list(row.values)]) + ')'
                                for _, row in table.iterrows()])
            value_inserter = "INSERT INTO {} VALUES {}".format(name, values)
            try:
                cursor.execute(value_inserter)
            except Exception as e:
                print(e, ':', value_inserter)
                print(table)
                connection.close()
                sys.exit(1)

finally:
    if connection.open:
        connection.close()
