from env import *
import mysql.connector

# Database class
class Database:
    try: 
        db = mysql.connector.connect(
        host = Env.DATABASE_HOST,
        user = Env.DATABASE_USER,
        password = Env.DATABASE_PASSWORD,
        database = Env.DATABASE_NAME,
        auth_plugin="mysql_native_password"
        )
        cursor = db.cursor(buffered=True)
    except Exception as e:
        print(e)
        pass
 