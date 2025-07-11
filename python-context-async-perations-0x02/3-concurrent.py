import aiosqlite
import asyncio
DB_NAME = 'user_db'


async def async_fetch_users():
    # connecting to the database
    async with aiosqlite.connect(DB_NAME) as db:
        # fetch all users
        async with db.execute('SELECT * FROM users') as cursor:
            rows = await cursor.fetchall()
            # print all users
            for row in rows:
                print(f'All Users: {row}')
            return rows


async def async_fetch_older_users():
    # connecting to the database
    async with aiosqlite.connect(DB_NAME) as db:
        # fetcting data from database
        async with db.execute('SELECT * FROM users WHERE age > 40') as cursor:
            rows = await cursor.fetchall()
            # print Users older than 40
            for row in rows:
                print(f'Older Users: {row}')
            return rows


# Print results simultaneosly 
async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
