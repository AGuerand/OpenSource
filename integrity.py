import os
import sqlite3
import hashlib

def create_database():
    """Create a SQLite database to store file hashes."""
    conn = sqlite3.connect('file_integrity.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_hashes (
            file_path TEXT PRIMARY KEY,
            hash TEXT
        )
    ''')
    conn.commit()
    conn.close()

def load_previous_integrity_report():
    """Load previous integrity report from SQLite database."""
    integrity_report = {}
    conn = sqlite3.connect('file_integrity.db')
    cursor = conn.cursor()
    cursor.execute('SELECT file_path, hash FROM file_hashes')
    rows = cursor.fetchall()
    for row in rows:
        integrity_report[row[0]] = row[1]
    conn.close()
    return integrity_report

def save_current_integrity_report(integrity_report):
    """Save current integrity report to SQLite database."""
    conn = sqlite3.connect('file_integrity.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM file_hashes')  # Clear previous data
    for file_path, hash_value in integrity_report.items():
        cursor.execute('INSERT INTO file_hashes (file_path, hash) VALUES (?, ?)', (file_path, hash_value))
    conn.commit()
    conn.close()

def calculate_hash(file_path):
    """Calculate the SHA256 hash of a file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(65536)  # 64KB chunks
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

def check_integrity(directory):
    """Check the integrity of files in a directory and store hashes in SQLite database."""
    integrity_report = {}
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_hash = calculate_hash(file_path)
            integrity_report[file_path] = file_hash
    
    # Enregistrer les empreintes de hachage dans la base de données
    save_current_integrity_report(integrity_report)
    
    return integrity_report

def detect_unauthorized_changes(previous_integrity, current_integrity):
    """Detect unauthorized changes between previous and current integrity reports."""
    unauthorized_changes = {}
    for file_path, current_hash in current_integrity.items():
        if file_path not in previous_integrity:
            unauthorized_changes[file_path] = "New File"
        elif current_hash != previous_integrity[file_path]:
            unauthorized_changes[file_path] = "Modified"
    
    for file_path, previous_hash in previous_integrity.items():
        if file_path not in current_integrity:
            unauthorized_changes[file_path] = "Deleted"

    return unauthorized_changes

def use_integrity():
    # Exemple d'utilisation:
    create_database()
    conn = sqlite3.connect("path.db")
    cursor = conn.cursor()

    # Retrieve all rows from file_paths table
    cursor.execute('''SELECT * FROM file_paths''')
    rows = cursor.fetchall()
    for row in rows:
        directory_path = row[1]
        previous_integrity = load_previous_integrity_report()
        current_integrity = check_integrity(directory_path)
        changes = detect_unauthorized_changes(previous_integrity, current_integrity)

    # Traiter les modifications non autorisées détectées
    for file_path, change_type in changes.items():
        print(f"{file_path}: {change_type}")

use_integrity()