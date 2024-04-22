import os

def perm(path, permissions, permissions, permissions):

    try:
        os.chmod(path, (permissions * 8 * 8) + (permissions * 8) + permissions)
        print("Autorisations changées", path)
    except Exception as e:
        print("Erreur :", str(e))

