import pyinotify
import logging

def main() :

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='log.log')
    
    mask = pyinotify.IN_ATTRIB | pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_MODIFY | pyinotify.IN_MOVED_FROM | pyinotify.IN_MOVED_TO


    class EventHandler(pyinotify.ProcessEvent):
        def process_IN_ATTRIB(self, event):
            logging.info(f"Attributs modifiés: {event.pathname}")

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


    handler = EventHandler()
    wm = pyinotify.WatchManager()

    watcher = pyinotify.Notifier(wm, handler)
    wm.add_watch('New', mask, rec=True)

    print("Surveillance en cours...")

    watcher.loop()

main()