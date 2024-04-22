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

    path = input("path :")
    Insert_Path("path.db", path)
    print_database("path.db")

    whattodo = input("monitor = 1, change right = 2\n")
    time.sleep(1)
    if int(whattodo) == 1 :
        Monitor(path)
    elif int(whattodo) == 2 :
        user= input("user right\n")
        group= input("group right\n")
        other= input("other right\n")
        perm(path,int(user),int(group),int(other))

main()