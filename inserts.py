import asyncio
import asyncpg
from datetime import datetime
from datetime import datetime, timedelta
import random

CONNECTION = "postgres://tsdbadmin:[PASSWORD]@qyfo8px5kn.t52b6zcudq.tsdb.cloud.timescale.com:34839/tsdb?sslmode=require"
#password: [PASSWORD]
#username: tsdbadmin

async def insert_example_data():
    # Connect to the PostgreSQL database
    conn = await asyncpg.connect(CONNECTION)

    # Generate random data for inserts
    inserts = []
    num_inserts = 15000  # You can change this to insert more records

    for _ in range(num_inserts):
        # Generate random timestamp within the last 30 days
        time = datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23), minutes=random.randint(0, 59))
        # Generate random sensor ID (1 to 10 for example)
        sensor_id = random.randint(1, 10)
        # Generate a random value or None
        value = random.uniform(0.0, 100.0)
        inserts.append((time, sensor_id, value))

    # Execute inserts
    for insert in inserts:
        time, sensor_id, value = insert
        await conn.execute('''
            INSERT INTO conditions (time, sensor_id, value) 
            VALUES ($1, $2, $3);
        ''', time, sensor_id, value)

    print("Inserted example data successfully.")

    # Close the connection
    await conn.close()

# Run the async function
asyncio.run(insert_example_data())
