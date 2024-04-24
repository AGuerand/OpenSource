import sqlite3  # SQLite database module

def Create_Database(database_name):
    # Connect to the database
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS file_paths
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       pathname TEXT UNIQUE NOT NULL)''')

    conn.commit()  # Commit changes to the database
    conn.close()  # Close database connection

    print(f"Database '{database_name}' created successfully.")  # Print success message


def Insert_Path(database_name, pathname, queue):
    # Connect to the database
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    try:
        # Insert path into file_paths table
        cursor.execute('''INSERT INTO file_paths (pathname) VALUES (?)''', (pathname,))
        print(f"Path '{pathname}' inserted")  # Print success message if insertion is successful
    except sqlite3.IntegrityError:
        print(f"Path '{pathname}' already exists")  # Print message if path already exists

    conn.commit()  # Commit changes to the database
    conn.close()  # Close database connection

    print(f"Path '{pathname}' inserted ")  # Print completion message
    
    queue.put("Path Added")


def print_database(database_name):
    # Connect to the database
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Retrieve all rows from file_paths table
    cursor.execute('''SELECT * FROM file_paths''')
    rows = cursor.fetchall()

    print("ID\tPathname")
    for row in rows:
        print(f"{row[0]}\t{row[1]}")  # Print ID and pathname for each row

    conn.close()  # Close database connection


def get_path(database_name):
    # Connect to the database
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Select all pathnames from file_paths table
    cursor.execute("SELECT pathname FROM file_paths")
    paths = [row[0] for row in cursor.fetchall()]  # Fetch all pathnames and store in a list

    conn.close()  # Close database connection
    return paths  # Return list of pathnames


def Delete_Path(database_name, pathname, queue):
    # Connect to the database
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    try:
        # Delete pathname from file_paths table
        cursor.execute('''DELETE FROM file_paths WHERE pathname = ?''', (pathname,))
        if cursor.rowcount > 0:
            print(f"'{pathname}' deleted.")  # Print deletion success message if row was affected
        else:
            print(f"'{pathname}' not found.")  # Print message if pathname not found
    except sqlite3.Error as e:
        print("error:", e)  # Print error message if an error occurs

    queue.put("file deleted")

    conn.commit()  # Commit changes to the database
    conn.close()  # Close database connection
