import os

def perm(path, user, group, other):

    try:
        os.chmod(path, (user * 8 * 8) + (group * 8) + other)
        print("Autorisations définies avec succès pour le fichier", path)
    except Exception as e:
        print("Une erreur s'est produite lors de la définition des autorisations:", str(e))

