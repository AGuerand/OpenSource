from monitor import Monitor
from database import *
import os
from right import *
import threading


db_path = "path.db"

def main():
    if os.path.exists(db_path):
        pass
    else :
        Create_Database("path.db")

    paths = get_path("path.db")

    monitor_thread = threading.Thread(target=Monitor, args=("path.db",))
    monitor_thread.daemon = True
    monitor_thread.start()

    while True :
        whattodo = input("Change Right = 1, add path = 2, delete path = 3, exit = 0\n")

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
            Insert_Path("path.db", path)
            print_database("path.db")
        
        elif int(whattodo) == 0 :
            print("exit")
            break
            
        else :
            print("womp womp")

main()