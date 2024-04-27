import os

def perm(path, user, group, other):
    try:
        os.chmod(path, (user * 8 * 8) + (group * 8) + other)
        print("Succès\n", path)  
    except Exception as e:
        print("Erreur:\n", str(e)) 
