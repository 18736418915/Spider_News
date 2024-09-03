
import pymysql
from pymysql.cursors import DictCursor
from config import Config

def get_db_connection():
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        charset='utf8mb4',
        cursorclass=DictCursor
    )

def fetch_all_from_table(table_name):
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                sql = f"SELECT * FROM {table_name}"
                cursor.execute(sql)
                return cursor.fetchall()
    except pymysql.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    return []


def get_all_tables():
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                # 针对 MySQL 的查询
                sql = """
                show tables
                """
                cursor.execute(sql)
                tables = cursor.fetchall()
                return [list(table.values())[0] for table in tables]
    except pymysql.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    return []

# 使用示例
if __name__ == "__main__":
    # results = fetch_all_from_table('')
    # for row in results:
    #     print(row)
    tables = get_all_tables()
    for table in tables:
        print(table)