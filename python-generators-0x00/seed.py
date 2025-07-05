import mysql.connector


def connect_db():
    return mysql.connector.connect(
        user='root',
        password='Oluwafemi1.',
        host='localhost'
    )


# Create the database
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXIST ALX_prodev")
    cursor.close


# Connect to the database
def connect_to_prodev():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Oluwafemi1.',
        database='ALX_prodev'
    )


# create Table
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXIST user_data(
        user_id(Primary Key, UUID, Indexed)
        name (VARCHAR, NOT NULL)
        email (VARCHAR, NOT NULL)
        age (DECIMAL,NOT NULL)
        ) """
    )
    connection.commit()
    cursor.close()


# Insert Data
def insert_data(connection, data):
    cursor = connection.cursor()
    queries = """
                INSERT IGNORE INTO user_data(name, email, age)
                VALUES(john, john@mail.com, 24)
                """
    cursor.excutemany(queries, data)
    connection.commit()
    cursor.close()
