import sqlite3
import hashlib
import os

# Function to calculate hash of a file
def calculate_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

# Function to check integrity and update database
def check_integrity(db_file_path, integrity_db_file):
    conn = sqlite3.connect(db_file_path)
    c = conn.cursor()

    # Connect to integrity database
    conn_integrity = sqlite3.connect(integrity_db_file)
    c_integrity = conn_integrity.cursor()

    # Ensure file_hashes table exists
    c_integrity.execute('''CREATE TABLE IF NOT EXISTS file_hashes
                           (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            file_path_id INTEGER NOT NULL,
                            hash TEXT NOT NULL,
                            modified INTEGER DEFAULT 0,
                            FOREIGN KEY(file_path_id) REFERENCES file_paths(id))''')

    # Retrieve paths from path.db
    c.execute('SELECT id, pathname FROM file_paths')
    rows = c.fetchall()

    changes_detected = []

    for row in rows:
        path_id, path = row
        modified = False

        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_hash = calculate_hash(file_path)

                    c_integrity.execute('SELECT hash FROM file_hashes WHERE file_path_id=?', (path_id,))
                    existing_hash = c_integrity.fetchone()

                    if not existing_hash:
                        c_integrity.execute('INSERT INTO file_hashes (file_path_id, hash, modified) VALUES (?, ?, ?)', (path_id, file_hash, 1))
                    elif existing_hash[0] != file_hash:
                        modified = True
                        c_integrity.execute('UPDATE file_hashes SET hash=?, modified=? WHERE file_path_id=?', (file_hash, 1, path_id))

        elif os.path.isfile(path):
            file_hash = calculate_hash(path)

            c_integrity.execute('SELECT hash FROM file_hashes WHERE file_path_id=?', (path_id,))
            existing_hash = c_integrity.fetchone()

            if not existing_hash:
                c_integrity.execute('INSERT INTO file_hashes (file_path_id, hash, modified) VALUES (?, ?, ?)', (path_id, file_hash, 1))
            elif existing_hash[0] != file_hash:
                modified = True
                c_integrity.execute('UPDATE file_hashes SET hash=?, modified=? WHERE file_path_id=?', (file_hash, 1, path_id))

        changes_detected.append((path_id, path, modified))

    conn_integrity.commit()
    conn_integrity.close()

    return changes_detected
    
def use_integrity(db_file_path, integrity_db_file):
    changes_detected = check_integrity(db_file_path, integrity_db_file)

    if changes_detected is None:
        return []  # Return an empty list if no changes are detected

    integrity_results = []
    for path_id, path, modified in changes_detected:
        integrity_results.append((path_id, path, modified))

    return integrity_results
