# Stream rows one after the other
def stream_users(connection):
    cursor = connection.cursor()
    cursor.excute('SELECT * FROM TABLE user_data')
    for row in cursor:
        yield row
    cursor.close()
