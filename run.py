import sys
import psycopg2
import psycopg2.extras



host_name = "localhost"
database = "test"
username = "hudak.pavol"
pwd = ""
port_id = 5432



def start():
    print("Start")
    conn = None

    # CONNECTION TO DATABASE
    try:
        conn = psycopg2.connect(
            host = host_name,
            database = database,
            user = username,
            password = pwd,
            port = port_id
        )
        print("Database connected")

        # CREATE DATABASE TABLE
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("DROP TABLE IF EXISTS users")
        create_script = '''
        CREATE TABLE IF NOT EXISTS users (
            id int PRIMARY KEY,
            name varchar(100) NOT NULL,
            surname varchar(100)
        )
        '''
        cur.execute(create_script)
        conn.commit()

        #INSERT DATA INTO USERS TABLE
        insert_script = '''
        INSERT INTO users (id, name, surname) values (%s, %s, %s)
        '''
        insert_values = [(1, "Pavol", "Hudak"), (2, "Matej", "Hudak")]
        for insert_value in insert_values:
            cur.execute(insert_script, insert_value)
        conn.commit()


        #SELECT DATA FROM USERS TABLE
        cur.execute('SELECT * FROM users')
        records = cur.fetchall()
        print("Data: \n")
        for record in records:
            print(record)
        print()

        #UPDATE DATA FROM USERS TABLE
        update_script = '''
        UPDATE users SET surname = 'Hudakovci' WHERE id = 1
        '''
        cur.execute(update_script)
        conn.commit()

        #SELECT DATA FROM USERS TABLE
        cur.execute('SELECT * FROM users')
        records = cur.fetchall()
        print("Data: \n")
        for record in records:
            print(record)
        print()

        #DELETE DATA FROM USERS TABLE
        delete_script = '''
        DELETE FROM users WHERE name = %s
        '''
        delete_id = ('Pavol',)
        cur.execute(delete_script, delete_id)
        conn.commit()

        #SELECT DATA FROM USERS TABLE
        cur.execute('SELECT * FROM users')
        records = cur.fetchall()
        print("Data: \n")
        for record in records:
            print(record)
        print()

    except Exception as error:
        print("Error:", error)

    finally:
        if conn is not None:
            conn.close()
            print("Database disconnected")

def init():
    print("Init")




if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        commad = sys.argv[1]
        if commad == "start":
            start()
        elif commad == "init":
            init()
    else:
        print("usage:\n\n\trun.py [ start | init ]")
