import os  # Operating System module

def perm(path, user, group, other):
    try:
        # Calculate the new permissions and apply them to the file or directory
        os.chmod(path, (user * 8 * 8) + (group * 8) + other)
        print("Succès\n", path)  # Print success message
    except Exception as e:
        print("Erreur:\n", str(e))  # Print error message if an exception occurs
