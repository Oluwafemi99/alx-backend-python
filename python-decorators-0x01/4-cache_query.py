import functools
import sqlite3


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('user.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper


query_cache = []


def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)
        if query in query_cache:
            print(f'executing cached queries{query}')
            return query_cache[query]
        print(f'executing and caching {query}')
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper
