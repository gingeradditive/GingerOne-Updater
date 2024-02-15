import tkinter as tk
import os
import requests
import shutil
import platform
import sys
import json

from app import App

# URL dell'API di GitHub per ottenere le informazioni sull'ultima release
api_url = "https://api.github.com/repos/GiacomoGuaresi/pieDeployChainExploration/releases/latest"
response = requests.get(api_url)
release_data = response.json()

# Estrai informazioni sull'ultima release
last_release_location = release_data["tarball_url"]
last_release_version = release_data["tag_name"]

# Imposta altre variabili
if platform.system() == "Windows":
    temp_dir = "D:\\Users\\guare\\Documents\\GIngerTemp\\GingerUpdateSourceFolder"
    current_release_version_file = "D:\\Users\\guare\\Documents\\GIngerTemp\\GingerAddiction.config"
elif platform.system() == "Linux":
    temp_dir = "/tmp/GingerUpdateSourceFolder"
    current_release_version_file = "/etc/GingerAddiction.config"
else:
    # Gestisci altri sistemi operativi, se necessario
    sys.exit("Sistema operativo non supportato")

# Pulisci aggiornamenti passati
shutil.rmtree(temp_dir, ignore_errors=True)
os.makedirs(temp_dir)

# Controlla l'esistenza del file contenente la versione corrente
if not os.path.isfile(current_release_version_file):
    print("Current release version file NOT found!")
    with open(current_release_version_file, "w") as version_file:
        json.dump({}, version_file)

# Controlla la versione corrente con quella dell'ultima release
with open(current_release_version_file, "r") as version_file:
    current_version_data = json.load(version_file)
    current_version = current_version_data.get("tag_name", "v0.0.0")

if last_release_version != current_version:
    print("Version not match, try update")

    # Avvia interfaccia grafica
    root = tk.Tk()
    app = App(root, temp_dir, last_release_location, release_data, current_version)
    root.mainloop()

    # List exit_value
    # 0: succefully installed
    # 1: close no update
    # 2: close no update no retry
    # 3: error on tar.gz extraction 

    if app.exit_value == 0:       
        # Aggiorna la versione locale
        with open(current_release_version_file, "w") as version_file:
            json.dump(release_data, version_file)
            
else:
    print("No need to update")
    print(last_release_version)

sys.exit()