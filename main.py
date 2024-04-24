# Import necessary modules
import sqlite3 
from monitor import Monitor  # Module for monitoring
from database import *  # Functions related to database operations
import os  # Operating System module
from right import *  # Functions for handling permissions
import threading  # Threading for concurrent execution
from security import *  # Security-related functions
import subprocess  # Subprocess module for executing external commands
import sys  # System-specific parameters and functions
from double_auth import *  # Double authentication module
import queue

# Path to the database
db_path = "path.db"

# Function to install dependencies
def install_dependencies():
    dependencies = ["argon2-cffi"]  # List of dependencies to install

    # Loop through dependencies and install each one
    for package in dependencies:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Main function
def main():
    # Check if the database file exists, if not, create it
    if os.path.exists(db_path):
        pass
    else:
        Create_Database("path.db")

    # Get paths from the database
    paths = get_path("path.db")

    # Perform password and double authentication checks
    if password() == True:
        if double_auth() == True:
            pass
        else:
            os._exit(0)  # Exit if double authentication fails
    else:
        os._exit(0)  # Exit if password check fails

    update_queue = queue.Queue()
    # Start monitoring thread
    monitor_thread = threading.Thread(target=Monitor, args=("path.db", update_queue))
    monitor_thread.daemon = True
    monitor_thread.start()

    while True:
        while not update_queue.empty():
            message = update_queue.get()
            if message == "PathAdded":
                print("Path added. Restarting monitoring...")
            elif message == "PathDeleted":
                print("Path deleted. Restarting monitoring...")


        # Prompt user for action
        whattodo = input("Changer droit = 1, Ajouter chemin = 2, Suprimer chemin = 3, Fin = 0\n")

        if int(whattodo) == 1:
            conn = sqlite3.connect("path.db")
            cursor = conn.cursor()
            # Change permissions
            print_database("path.db")
            try:
                choix_id = int(input("Veuillez saisir l'ID du chemin de fichier que vous souhaitez sélectionner : "))
                cursor.execute("SELECT id FROM file_paths WHERE id=?", (choix_id,))
                chemin_exist = cursor.fetchone()
                if chemin_exist:
                    cursor.execute("SELECT pathname FROM file_paths WHERE id=?", (choix_id,))
                    chemin = cursor.fetchone()
                else:
                    print("L'ID saisi n'existe pas. Veuillez saisir un ID valide.")
            except ValueError:
                print("Veuillez saisir un ID valide.")
    
            user = input("User Right\n")
            group = input("Group Right\n")
            other = input("Other Right\n")
            perm(chemin[0], int(user), int(group), int(other))

        elif int(whattodo) == 2:
            # Add path to the database
            path = input("path :")
            Insert_Path("path.db", path, update_queue)
            print_database("path.db")
           

        elif int(whattodo) == 3:
            # Delete path from the database
            path = input("path :")
            Delete_Path("path.db", path, update_queue)
            print_database("path.db")
            
        
        elif int(whattodo) == 0:
            # Exit the program
            print("exit")
            os._exit(0)
            
        else:
            # Invalid input
            print("womp womp")

# Install dependencies before running main function
install_dependencies()
main()