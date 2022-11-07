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
        print('\n')
        print(record[1])

def select_all_heros_numbers():
    query = """
        SELECT * FROM heroes
    """
    list_of_heros_numbers = execute_query(query).fetchall()
    for record in list_of_heros_numbers:
        print('\n')
        print(record[0],'  ',record[1])

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
        print('\n')
        print(record[3])

def select_ability_types():
    query = """
        SELECT * FROM ability_types
    """
    list_of_ability_types = execute_query(query).fetchall()
    print('Types of Abilities')
    for record in list_of_ability_types:
        print('\n')
        print(record[1])

#========= Print Ability_type_id ==

def select_ability_types_numbers():
    query = """
        SELECT * FROM ability_types
    """
    list_of_ability_types = execute_query(query).fetchall()
    for record in list_of_ability_types:
        print('\n')
        print(record[0],'  ',record[1])

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
    print(f'HERO {name} HAS BEEN ADDED')
    #query,(name,) 

#========== INSERT Ability ============

def insert_new_ability():
    input('PRESS ENTER TO CREATE NEW ABILITY')
    name = input('Ability Name:  ')
    query = """
        INSERT INTO ability_types
            (name)
        Values(%s);
    """
    execute_query(query,(name,))
    print(f'New Ability {name} Added')
#========== Assign New Ability ========

def assign_hero_ability():
    input('PRESS ENTER TO ASSIGN A HERO A NEW ABILITY')
    
    query = """
        SELECT * FROM heroes
    """
    list_of_heros_numbers = execute_query(query).fetchall()

    query = """
        SELECT * FROM ability_types
    """
    list_of_ability_types = execute_query(query).fetchall()
    # Print out hero and ability ids and names
    print("HEROES NUMBER")
    for record in list_of_heros_numbers:
        print(record[0],'  ',record[1])
    print('\n')
    print("ABILITY NUMBER")
    for record in list_of_ability_types:
        print(record[0],'  ',record[1])

    print('\n')
    hero_id = input('ENTER A NUMBER TO PICK A HERO: ')
    ability_id = input('ENTER A NUMBER TO PICK A ABILITY: ')

    query = """
        INSERT INTO abilities (hero_id, ability_type_id)
        VALUES(%s,%s)
    """
    execute_query(query,(hero_id,ability_id)) 

    query = """
        SELECT DISTINCT heroes.id,heroes.name, string_agg(ability_types.name,' ')
        FROM heroes
        JOIN abilities ON heroes.id = abilities.hero_id
        JOIN ability_types ON ability_types.id = abilities.ability_type_id
        WHERE heroes.id = %s
        GROUP BY heroes.id
    """
    list_assigned_hero = execute_query(query,(hero_id,))
    print('\n')

    for record in list_assigned_hero:
        print(record[1],'HAS BEEN ASSIGNED',record[2], 'ABILITY')

#========== Update HERO Name ==========

def update_hero_name():
    print('PRESS ENTER TO UPDATE HEROS NAME')
    select_all_heros_numbers()
    hero_id = input('ENTER A HEROS NUMBER YOU WOULD LIKE TO CHANGE: ')
    name = input(f'ENTER HERO {hero_id}s NEW NAME: ')
    query = """
        UPDATE heroes
        SET name= %s
        WHERE id = %s
    """

    list_hero_name = execute_query(query,(name,hero_id))
    print('\n')
    select_all_heros_numbers()   


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
    # 'List_All': select_all_heros,
    'List_All_Heros': select_all_heros_numbers,
    'List_All_About': select_heros_about,
    'List_All_Bio': select_heros_bio,
    'List_Ability_Types': select_ability_types,
    'List_Hero_Ability': select_hero_ability_type,
    'List_Ability_Numbers': select_ability_types_numbers,
    'New_Hero': insert_new_hero,
    'Delete_Hero': delete_hero,
    'New_Ability':insert_new_ability,
    'Assign_Ability':assign_hero_ability,
    'Update_Hero':update_hero_name
    
}

def help_commands():
    print('===== List of Commands =====')
    for key in command_dict:
        print('\n','    ',key)
    print('\n')

# command_dict[command]()
def input_func():
    print('\n')
    command = input("ENTER COMMAND: ")
    for key in command_dict:
        if command in command_dict:
            command_dict[command]()
            input_func()
        elif command == 'help':
            help_commands()
            input_func()
        else:
            print('---- Not A Valid Command -----')
            input_func()

input_func()
