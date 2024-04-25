import pyinotify
import logging
import os
import pwd
from database import get_path
import time
import threading

def Monitor(database_name, queue):
    def update_watch_manager(wm, current_paths, new_paths):
        # Find paths to be added
        paths_to_add = [path for path in new_paths if path not in current_paths]
        for path in paths_to_add:
            wm.add_watch(path, mask, rec=True)
            current_paths.append(path)
            print(f"New path added to monitoring: {path}")

        # Find paths to be removed
        paths_to_remove = [path for path in current_paths if path not in new_paths]
        for path in paths_to_remove:
            wm.rm_watch(wm.get_wd(path))
            current_paths.remove(path)
            print(f"Path removed from monitoring: {path}")

    # Get initial paths from the database
    paths = get_path(database_name)


    # Configure logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='log.log')

    # Define mask for monitoring events
    mask = pyinotify.IN_ATTRIB | pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_MODIFY | pyinotify.IN_MOVED_FROM | pyinotify.IN_MOVED_TO | pyinotify.IN_MOVE_SELF

    # Define event handler class
    class EventHandler(pyinotify.ProcessEvent):
        def process_default(self, event):
            if event.mask & pyinotify.IN_ATTRIB:
                # Get file attributes
                attribs = os.lstat(event.pathname)
                # Get username associated with the file
                username = pwd.getpwuid(attribs.st_uid).pw_name
                # Convert permissions to octal representation
                permissions_octal = oct(attribs.st_mode & 0o777) 
                # Log attribute changes
                logging.info(f"\n")
                logging.info(f"Attributs modifiés pour {event.pathname}:")
                logging.info(f"    Mode (permissions): {permissions_octal}")
                logging.info(f"    Utilisateur: {username}")
                logging.info(f"    Groupe propriétaire: {attribs.st_gid}")
                logging.info(f"    Taille: {attribs.st_size} bytes")
                logging.info(f"    Dernier accès: {attribs.st_atime}")
                logging.info(f"    Dernière modification: {attribs.st_mtime}")
                
        def process_IN_CREATE(self, event):
            # Log file creation event
            logging.info(f"Nouveau fichier créé: {event.pathname}")

        def process_IN_DELETE(self, event):
            # Log file deletion event
            logging.debug(f"Fichier supprimé: {event.pathname}")

        def process_IN_MODIFY(self, event):
            # Log file modification event
            logging.info(f"Fichier modifié: {event.pathname}")

        def process_IN_MOVED_FROM(self, event):
            # Log file moved from event
            logging.info(f"Fichier déplacé de: {event.pathname}")

        def process_IN_MOVED_TO(self, event):
            # Log file moved to event
            logging.info(f"Fichier déplacé vers: {event.pathname}")

        def process_IN_MOVE_SELF(self, event):
            # Log event when observed file/directory is moved
            logging.info(f"Fichier/Dossier observé a été déplacer: {event.pathname}")

    # Initialize event handler and watch manager
    handler = EventHandler()
    wm = pyinotify.WatchManager()

    # Add paths to watch manager
    for path in paths:
        wm.add_watch(path, mask, rec=True)

    # Initialize notifier
    watcher = pyinotify.Notifier(wm, handler)

    # Start monitoring
    print("Surveillance ...")
    queue.put("Update")
    
    # Function to start the watcher loop in a separate thread
    def start_watcher_loop():
        watcher.loop()

    # Start the watcher loop in a separate thread
    watcher_thread = threading.Thread(target=start_watcher_loop)
    watcher_thread.start()
    
    # Periodically check for new paths and add them to watch manager
    while True:
        try:
            time.sleep(1)  # Check every 1 second for updates
            new_paths = get_path(database_name)
            update_watch_manager(wm, paths, new_paths)
        except Exception as e:
            print(f"Error: {e}")