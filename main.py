from monitor import Monitor
from database import *
import os
from right import *
import time

db_path = "path.db"

def main():
    if os.path.exists(db_path):
        pass
    else :
        Create_Database("path.db")

    paths = get_path("path.db")

    whattodo = input("Monitor = 1, Change Right = 2, add path = 3\n")

    if int(whattodo) == 1 :
        Monitor("path.db")

    elif int(whattodo) == 2 :
        user= input("User Right\n")
        group= input("Group Right\n")
        other= input("Other Right\n")
        perm(path,int(user),int(group),int(other))

    elif int(whattodo) == 3 :
        path = input("path :")
        Insert_Path("path.db", path)
        print_database("path.db")
        
    else :
        print("womp womp")

main()