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
#=================== DO NOT EDIT ABOVE =====================================
#create_connection("postgres", "postgres", "postgres")


#====================== PYTHON SQL =================================


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

def select_ability_types():
    query = """
        SELECT * FROM ability_types
    """
    list_of_ability_types = execute_query(query).fetchall()
    for record in list_of_ability_types:
        print(record[1])

#========= INSERT HERO ============
def insert_new_hero():
    input("Press Enter to Create a New Hero")
    name = input('Enter Name: ')
    about = input('Write About Me for Hero: ')
    bio = input('Write a bio for your Hero: ')

    query = """
        INSERT INTO heroes 
            (name,about_me,biography)
        VALUES (%s,%s,%s);
    """    
    execute_query(query,(name,about,bio)) 
    #query,(name,) 

#========== REMOVE HERO ===============
#DELETE FROM table_name WHERE condition;

def delete_hero():
    input('Press Enter to see Hero Numbers')
    command_dict['All_Numbers']()
    hero_id = input('Delete Hero by Number: ')
    query = """
        DELETE FROM heroes WHERE id = %s
    """
    execute_query(query,(hero_id,))

#========= Heros & Ability =======
def select_hero_ability_type():
    query = """
        SELECT DISTINCT heroes.id,heroes.name, string_agg(ability_types.name,' ')
        FROM heroes
        JOIN abilities ON heroes.id = abilities.hero_id
        JOIN ability_types ON ability_types.id = abilities.ability_type_id
        GROUP BY heroes.id   
    """
    list_of_heros_ability = execute_query(query).fetchall()
    for record in list_of_heros_ability:
        print('\n',record[0],'  ',record[1],'  ',record[2])
    print('\n')
#======== Command list ============         

command_dict = {
    'All': select_all_heros,
    'All_Numbers': select_all_heros_numbers,
    'All_About': select_heros_about,
    'All_Bio': select_heros_bio,
    'Ability_Types': select_ability_types,
    'New_Hero': insert_new_hero,
    'Delete_Hero': delete_hero,
    'Hero_Ability': select_hero_ability_type
}
# command_dict[command]()
def input_func():
    command = input("ENTER COMMAND: ")
    for key in command_dict:
        if command in command_dict:
            command_dict[command]()
            input_func()
        else:
            print('---- Not A Valid Command -----')
            input_func()

input_func()