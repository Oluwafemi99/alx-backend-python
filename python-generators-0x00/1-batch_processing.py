# fetch and process data in batches
def stream_users_in_batches(batch_size):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM user_data')
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows
    cursor.close()


def batch_processing():
    for batch in stream_users_in_batches():
        filter_user = [user for user in batch if user['age'] > 25]
        for user in filter_user:
            print(f'User: {user['name']}, Age: {user['age']}')
