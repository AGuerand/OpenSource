import pyinotify
import logging

# Configurer le journal système
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='log.log')

# Définir les événements que nous voulons surveiller
mask = pyinotify.IN_ATTRIB | pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_MODIFY | pyinotify.IN_MOVED_FROM | pyinotify.IN_MOVED_TO

# Définir la classe de gestionnaire d'événements
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


# Créer un gestionnaire d'événements et un observateur
handler = EventHandler()
wm = pyinotify.WatchManager()

# Ajouter le répertoire à surveiller
watcher = pyinotify.Notifier(wm, handler)
wm.add_watch('New', mask, rec=True)

print("Surveillance en cours...")

# Démarrer la surveillance
watcher.loop()
