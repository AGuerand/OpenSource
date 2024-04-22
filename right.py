import os

def perm(file_path, user_permissions, group_permissions, other_permissions):

    try:
        os.chmod(file_path, (user_permissions * 8 * 8) + (group_permissions * 8) + other_permissions)
        print("Autorisations définies avec succès pour le fichier", file_path)
    except Exception as e:
        print("Une erreur s'est produite lors de la définition des autorisations:", str(e))

