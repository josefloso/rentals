# wait_for_db.py
import os
import sys
import asyncio
from asyncpg import connect

async def check_db():
    for i in range(10):
        try:
            conn = await connect(
                host='db',
                port=5432,
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                database=os.getenv('POSTGRES_DB')
            )
            await conn.close()
            print('Database connection successful!')
            return True
        except Exception as e:
            print(f'Waiting for database... (Attempt {i+1}/10)')
            await asyncio.sleep(2)
    print('Failed to connect to database after 10 attempts')
    sys.exit(1)

if __name__ == '__main__':
    asyncio.run(check_db())