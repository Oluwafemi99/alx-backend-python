def paginate_users(connection, page_size, offset):
    cursor = connection.cursor()
    queries = """
            SELECT * FROM user_data
            ORDER BY name
            LIMIT %s OFFSET %s"""
    cursor.execute(queries, (page_size, offset))
    rows = cursor.fetctall()
    cursor.close()
    return rows


def lazy_paginate(page_size):
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield offset
        offset += page_size
