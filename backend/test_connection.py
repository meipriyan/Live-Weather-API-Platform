from sqlalchemy import text
from backend.database import engine

try:
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT DATABASE(), VERSION()")
        )

        database_name, mysql_version = result.fetchone()

        print("MySQL Connection Successful!")
        print("Database:", database_name)
        print("MySQL Version:", mysql_version)

except Exception as error:
    print("MySQL Connection Failed!")
    print("Error:", error)