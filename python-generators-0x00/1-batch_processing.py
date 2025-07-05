# fetch and process data in batches
def stream_users_in_batches(batch_size):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM TABLE user_data')
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows
    cursor.close()
