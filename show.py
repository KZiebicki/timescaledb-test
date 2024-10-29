import asyncpg
import asyncio

CONNECTION = "postgres://tsdbadmin:[PASSWORD]@qyfo8px5kn.t52b6zcudq.tsdb.cloud.timescale.com:34839/tsdb?sslmode=require"

async def print_table_schema():
    # Connect to the PostgreSQL database
    conn = await asyncpg.connect(CONNECTION)

    # Query to get the table schema
    query = """
    SELECT column_name, data_type, is_nullable, column_default, is_identity
    FROM information_schema.columns
    WHERE table_name = 'conditions';
    """
    
    # Execute the query
    columns = await conn.fetch(query)

    # Print the table schema
    print("TABLE SCHEMA")
    print("Column Name | Data Type                       | Is Nullable | Default Value | Is Identity")
    print("-" * 90)
    for column in columns:
        # Handle None values
        column_name = column['column_name'] if column['column_name'] is not None else 'NULL'
        data_type = column['data_type'] if column['data_type'] is not None else 'NULL'
        is_nullable = column['is_nullable'] if column['is_nullable'] is not None else 'NULL'
        column_default = column['column_default'] if column['column_default'] is not None else 'NULL'
        is_identity = column['is_identity'] if column['is_identity'] is not None else 'NULL'
        
        print(f"{column_name:<12} | {data_type:<30} | {is_nullable:<12} | {column_default:<12} | {is_identity:<10}")

    print("\n\nTABLE DATA")
    select_query = "SELECT * FROM conditions;"
    rows = await conn.fetch(select_query)

    # Print the selected data
    print("Data in conditions table:")
    print("Time                  | Sensor ID | Value")
    print("-" * 40)
    for row in rows:
        print(f"{row['time']} | {row['sensor_id']:<10} | {row['value']}")

    # Close the connection
    await conn.close()

# Run the async function
asyncio.run(print_table_schema())
