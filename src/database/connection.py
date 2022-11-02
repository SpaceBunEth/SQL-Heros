import psycopg
from psycopg import OperationalError

def create_connection(db_name, db_user, db_password, db_host = "localhost", db_port = "5432"):
    connection = None
    try:
        connection = psycopg.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_query(query, params=None):
    connection = create_connection("postgres", "postgres", "postgres")
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit()
        print("Query executed successfully")
        connection.close()
        return cursor
    except OSError as e:
        print(f"The error '{e}' occurred or the hero name is already taken")

#create_connection("postgres", "postgres", "postgres")

def select_all_heros():
    query = """
        SELECT * FROM heroes
    """
    list_of_heros = execute_query(query).fetchall()
    for record in list_of_heros:
        print(record[1])

def select_all_heros_numbers():
    query = """
        SELECT * FROM heroes
    """
    list_of_heros_numbers = execute_query(query).fetchall()
    for record in list_of_heros_numbers:
        print(record[0],record[1])

def select_heros_about():
    query = """
        SELECT * FROM heroes
    """
    list_of_about = execute_query(query).fetchall()
    for record in list_of_about:
        print(record[2])

def select_heros_bio():
    query = """
        SELECT * FROM heroes
    """
    list_of_bio = execute_query(query).fetchall()
    for record in list_of_bio:
        print(record[3])
        
select_all_heros_numbers()