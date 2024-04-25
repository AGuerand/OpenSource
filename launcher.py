import subprocess
import os

if __name__ == "__main__":

    flask = subprocess.Popen(['python', 'Flask.py'])

    main = subprocess.Popen(['python', 'main.py'])

    flask.wait()
    main.wait()