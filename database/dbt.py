import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='39.106.157.61',
                             user='root',
                             password='',
                             db='pyweb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * from t_test"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()