from monitor import Monitor
from database import *
import os
from right import *
import threading
from security import *
import subprocess
import sys


db_path = "path.db"

def install_dependencies():
    dependencies = ["argon2-cffi"]

    for package in dependencies:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():

    if os.path.exists(db_path):
        pass
    else :
        Create_Database("path.db")

    paths = get_path("path.db")

    if password() == True :
        pass
    else :
        os._exit(0)

    monitor_thread = threading.Thread(target=Monitor, args=("path.db",))
    monitor_thread.daemon = True
    monitor_thread.start()


    while True :
        whattodo = input("Changer droit = 1, Ajouter chemin = 2, Suprimer chemin = 3, Fin = 0\n")

        if int(whattodo) == 1 :
            user= input("User Right\n")
            group= input("Group Right\n")
            other= input("Other Right\n")
            perm(path,int(user),int(group),int(other))

        elif int(whattodo) == 2 :
            path = input("path :")
            Insert_Path("path.db", path)
            print_database("path.db")

        elif int(whattodo) == 3 :
            path = input("path :")
            Delete_Path("path.db", path)
            print_database("path.db")
        
        elif int(whattodo) == 0 :
            print("exit")
            os._exit(0)
            
        else :
            print("womp womp")
install_dependencies()

main()