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


def Insert_Path(database_name, pathname, queue):
   
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    try:
        
        cursor.execute('''INSERT INTO file_paths (pathname) VALUES (?)''', (pathname,))
        print(f"Path '{pathname}' inserted")  
    except sqlite3.IntegrityError:
        print(f"Path '{pathname}' already exists")  

    conn.commit()  
    conn.close()  

    
    
    queue.put("Path Added")


def print_database(database_name):
  
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

 
    cursor.execute('''SELECT * FROM file_paths''')
    rows = cursor.fetchall()

    print("ID\tPathname")
    for row in rows:
        print(f"{row[0]}\t{row[1]}")  

    conn.close()  


def get_path(database_name):
    
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    
    cursor.execute("SELECT pathname FROM file_paths")
    paths = [row[0] for row in cursor.fetchall()]  

    conn.close()  
    return paths  


def Delete_Path(database_name, pathname, queue):
    
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    try:
        
        cursor.execute('''DELETE FROM file_paths WHERE pathname = ?''', (pathname,))
        if cursor.rowcount > 0:
            print(f"'{pathname}' deleted.")  
        else:
            print(f"'{pathname}' not found.") 
    except sqlite3.Error as e:
        print("error:", e) 
    queue.put("file deleted")

    conn.commit()  
    conn.close()  

def is_path_in_database(path, database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM file_paths WHERE pathname=?", (path,))
    path_exists = cursor.fetchone() is not None
    conn.close()
    return path_exists