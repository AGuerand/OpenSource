import logging
import os
import pwd
import pyinotify
import threading
import time
from database import get_path, is_path_in_database

def Monitor(database_name, queue):
    def is_path_in_monitored_paths(pathname, monitored_paths):
        for monitored_path in monitored_paths:
            if pathname.startswith(monitored_path):
                return True
        return False


    def update_watch_manager(wm, current_paths, new_paths):
        
        paths_to_add = [path for path in new_paths if path not in current_paths]
        for path in paths_to_add:
            if os.path.exists(path):  
                wm.add_watch(path, mask, rec=True)
                current_paths.append(path)
                print(f"New path added to monitoring: {path}")
            else:
                print(f"Path does not exist: {path}")

        
        paths_to_remove = [path for path in current_paths if path not in new_paths]
        for path in paths_to_remove:
            wm.rm_watch(wm.get_wd(path))
            current_paths.remove(path)
            print(f"Path removed from monitoring: {path}")

    
    paths = get_path(database_name)

    
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='log.log')

    
    mask = (pyinotify.IN_ATTRIB | pyinotify.IN_CREATE |
            pyinotify.IN_DELETE | pyinotify.IN_MODIFY |
            pyinotify.IN_MOVED_FROM | pyinotify.IN_MOVED_TO |
            pyinotify.IN_MOVE_SELF)

    
    class EventHandler(pyinotify.ProcessEvent):
        def process_default(self, event):
            
            if not is_path_in_database(event.pathname, "path.db"):
                return
                
            
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

    
    for path in paths:
        wm.add_watch(path, mask, rec=True)

    
    watcher = pyinotify.Notifier(wm, handler)

    
    print("Surveillance ...")
    queue.put("Update")
    
    
    def start_watcher_loop():
        watcher.loop()

    
    watcher_thread = threading.Thread(target=start_watcher_loop)
    watcher_thread.start()
    
    
    while True:
        try:
            time.sleep(1)  
            new_paths = get_path(database_name)
            update_watch_manager(wm, paths, new_paths)
        except Exception as e:
            print(f"Error: {e}")
