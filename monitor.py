import pyinotify
import logging
import os
import pwd

pathArray = []

def Monitor(path):

    pathArray.append(path)
    print(pathArray)
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='log.log')

    mask = pyinotify.IN_ATTRIB | pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_MODIFY | pyinotify.IN_MOVED_FROM | pyinotify.IN_MOVED_TO | pyinotify.IN_MOVE_SELF

    class EventHandler(pyinotify.ProcessEvent):
        def process_default(self, event):
            if event.mask & pyinotify.IN_ATTRIB:
                attribs = os.lstat(event.pathname)
                username = pwd.getpwuid(attribs.st_uid).pw_name
                permissions_octal = oct(attribs.st_mode & 0o777) 
                logging.info(f"\n")
                logging.info(f"Attributs modifiés pour {event.pathname}:")
                logging.info(f"    Mode (permissions): {permissions_octal}")
                logging.info(f"    Utilisateur: {username}")
                logging.info(f"    Groupe propriétaire: {attribs.st_gid}")
                logging.info(f"    Taille: {attribs.st_size} bytes")
                logging.info(f"    Dernier accès: {attribs.st_atime}")
                logging.info(f"    Dernière modification: {attribs.st_mtime}")
                
        def process_IN_CREATE(self, event):
            logging.info(f"Nouveau fichier créé: {event.pathname}")

        def process_IN_DELETE(self, event):
            logging.debug(f"Fichier supprimé: {event.pathname}")

        def process_IN_MODIFY(self, event):
            logging.info(f"Fichier modifié: {event.pathname}")

        def process_IN_MOVED_FROM(self, event):
            logging.info(f"Fichier déplacé de: {event.pathname}")

        def process_IN_MOVED_TO(self, event):
            logging.info(f"Fichier déplacé vers: {event.pathname}")

        def process_IN_MOVE_SELF(self, event):
            logging.info(f"Fichier/Dossier observé a été déplacer: {event.pathname}")

    handler = EventHandler()
    wm = pyinotify.WatchManager()

    watcher = pyinotify.Notifier(wm, handler)
    wm.add_watch(path, mask, rec=True)

    print("Surveillance ...")

    watcher.loop()
