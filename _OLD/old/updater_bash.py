import os
import requests
import tarfile
import shutil

# URL dell'API di GitHub per ottenere le informazioni sull'ultima release
api_url = "https://api.github.com/repos/GiacomoGuaresi/pieDeployChainExploration/releases/latest"
response = requests.get(api_url)
release_data = response.json()

# Estrai informazioni sull'ultima release
last_release_location = release_data["tarball_url"].replace(',', '')[:-1].replace('"', '')
last_release_version = release_data["tag_name"]

# Imposta altre variabili
temp_dir = "/tmp/GingerUpdateSourceFolder"
release_folder_regex = "GiacomoGuaresi*"
current_release_version_file = "/etc/GingerAddiction.version"

# Pulisci aggiornamenti passati
shutil.rmtree(temp_dir, ignore_errors=True)
os.makedirs(temp_dir)

# Controlla l'esistenza del file contenente la versione corrente
if not os.path.isfile(current_release_version_file):
    print("Current release version file NOT found!")
    with open(current_release_version_file, "w") as version_file:
        version_file.write("v?.?.?\n")

# Controlla la versione corrente con quella dell'ultima release
with open(current_release_version_file, "r") as version_file:
    current_version = version_file.read().strip()

if last_release_version != current_version:
    print("Version not match, try update")

    # Scarica l'ultima release
    response = requests.get(last_release_location)
    with tarfile.open(fileobj=io.BytesIO(response.content), mode="r:gz") as tar:
        tar.extractall(temp_dir)

    # Installa l'ultima release
    os.chdir(release_folder_regex)
    os.system("sh deploy.sh")

    # Aggiorna la versione locale
    with open(current_release_version_file, "w") as version_file:
        version_file.write(last_release_version)
else:
    print("No need to update")
    print(last_release_version)