import sqlite3

def Create_Database(database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS file_paths
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       pathname TEXT UNIQUE NOT NULL)''')

    conn.commit()
    conn.close()

    print(f"Database '{database_name}' created successfully.")


def Insert_Path(database_name, pathname):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    try:
        cursor.execute('''INSERT INTO file_paths (pathname) VALUES (?)''', (pathname,))
        print(f"Path '{pathname}' inserted")
    except sqlite3.IntegrityError:
        print(f"Path '{pathname}' already exists")


    conn.commit()
    conn.close()

    print(f"Path '{pathname}' inserted ")

def print_database(database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM file_paths''')
    rows = cursor.fetchall()

    print("ID\tPathname")
    for row in rows:
        print(f"{row[0]}\t{row[1]}")

    conn.close()
