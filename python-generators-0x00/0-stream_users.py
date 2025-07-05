# Stream rows one after the other
def stream_users():
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM TABLE user_data')
    for row in cursor:
        yield row
    cursor.close()
