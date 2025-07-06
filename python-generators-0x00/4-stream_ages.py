def stream_user_ages(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:
        yield age
    cursor.close()


def calculate_average_age(connection):
    total_age = 0
    count = 0
    for age in stream_user_ages(connection):
        total_age += age
        count += 1
    if count == 0:
        return 0
    average_age = total_age/count
    print(average_age)
