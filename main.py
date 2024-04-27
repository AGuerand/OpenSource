import sqlite3 
from monitor import Monitor 
from database import *  
import os  
from right import *  
import threading  
import subprocess  
import sys  
from double_auth import *  
import queue
from integrity import *


db_path = "path.db"


def install_dependencies():
    dependencies = ["argon2-cffi","Flask"] 

    
    for package in dependencies:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def main():
    
    if not os.path.exists(db_path):
        Create_Database("path.db")

    
    paths = get_path("path.db")

   
    if password() == True:
        if double_auth() == True:
            pass
        else:
            os._exit(0)  
    else:
        os._exit(0)  

    update_queue = queue.Queue()
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


        
        whattodo = input("Changer droit = 1, Ajouter chemin = 2, Suprimer chemin = 3, Verifier l'integrité ,Fin = 0\n")

        if int(whattodo) == 1:
            conn = sqlite3.connect("path.db")
            cursor = conn.cursor()
            
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
            
            path = input("path :")
            Insert_Path("path.db", path, update_queue)
            print_database("path.db")
           

        elif int(whattodo) == 3:
            
            path = input("path :")
            Delete_Path("path.db", path, update_queue)
            print_database("path.db")

        elif int(whattodo) == 4:
            
            use_integrity("path.db", "integrity.db")
            
        
        elif int(whattodo) == 0:
            
            print("exit")
            os._exit(0)
            
        else:
            
            print("womp womp")


install_dependencies()

from security import *

main()