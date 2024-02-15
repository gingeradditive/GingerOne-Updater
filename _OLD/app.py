import os
import subprocess
import tarfile
import threading
import time
from urllib.request import urlretrieve

import tkinter as tk
from tkinter import scrolledtext, ttk
from PIL import Image, ImageTk

GINGER_RED = "#8b0000"
GINGER_WHITE = "#ffffff"
GINGER_GRAY = "#FFF2F2"
GINGER_BLACK = "#000"

class App:
    #variabili per la grafica
    temp_dir = ""
    last_release_location = ""
    exit_value = -1
    download_thread = None
    new_release_data = {}
    current_release_version = ""
    
    def __init__(self, master, temp_dir, last_release_location, release_data, current_version):
        self.master = master
        master.title("App Full Screen")
        master.attributes('-fullscreen', True)
        master.configure(bg=GINGER_WHITE)

        self.temp_dir = temp_dir
        self.last_release_location = last_release_location
        self.new_release_data = release_data
        self.current_release_version = current_version

        width_percentage = 80
        screen_width, screen_height = 800, 480
        box_width, box_height = (screen_width * width_percentage) // 100, screen_height

        x_coordinate, y_coordinate = (screen_width - box_width) // 2, 0
        self.load_mainPage(master, y_coordinate, x_coordinate, box_height, box_width)

# -------------------------------------------------------

    def load_mainPage(self, master, y_coordinate, x_coordinate, box_height, box_width):
        self.create_background()

        self.create_label("A new firmware has been recently released.\r Do you want update it?", 11, GINGER_BLACK, 241, 145, 319, 29)
        currentVersion = self.current_release_version
        newVersion = self.new_release_data.get("tag_name","v0.0.0")
        self.create_label(f"Current version: {currentVersion}\n New version: {newVersion}", 9, GINGER_BLACK, 342, 216, 133, 26)

        self.create_button("Update now.", 202, 315, self.update_btn)
        self.create_button("Ask me later.", 417, 315, self.close_btn)

    def load_progressPage(self, master, y_coordinate, x_coordinate, box_height, box_width):
        # Aggiorna i task in sospeso prima di distruggere gli elementi
        master.update_idletasks()

        # Distruggi gli elementi presenti sulla pagina corrente
        for widget in self.master.winfo_children():
            widget.destroy()

        self.create_background()

        self.create_label("Installing the new version...\n Please do not power off the machine!", 11, GINGER_BLACK, 241, 145, 319, 29)
        
        # Creare e posizionare la progress bar determinata con uno stile personalizzato
        progress_bar_width = 378
        custom_style = ttk.Style()
        custom_style.configure("CustomHorizontal.TProgressbar",
                               thickness=10, troughcolor=GINGER_WHITE, troughrelief='flat',
                               troughborderwidth=0, background=GINGER_RED, bordercolor=GINGER_WHITE, troughpadding=0)
        custom_style.layout("CustomHorizontal.TProgressbar",
                            [('CustomHorizontal.Progressbar.trough',
                              {'sticky': 'nswe',
                               'children': [('CustomHorizontal.Progressbar.pbar',
                                              {'side': 'left', 'sticky': 'ns'})]})])
        self.progress_bar = ttk.Progressbar(master, length=progress_bar_width, mode="determinate", style="CustomHorizontal.TProgressbar")
        self.progress_bar.place(x=211, y=211)

        # Avvia il download in un thread separato
        self.download_thread = threading.Thread(target=self.download_file)
        self.download_thread.start()

    def load_restartPage(self, master, y_coordinate, x_coordinate, box_height, box_width):
        # Aggiorna i task in sospeso prima di distruggere gli elementi
        master.update_idletasks()

        # Distruggi gli elementi presenti sulla pagina corrente
        for widget in self.master.winfo_children():
            widget.destroy()

        self.create_background()

        self.create_label("Update completed.\n What's new?", 11, GINGER_BLACK, 241, 145, 319, 29)
        self.create_scrollTextArea(self.new_release_data.get("body","No change"), 252, 176, 295, 141)
        self.create_button("Start printer.", 336, 362, self.restart_btn)
        
# -------------------------------------------------------
        
    def update_progress(self, num_blocks, block_size, total_size):
        percent = int((num_blocks * block_size) / total_size * 100)
        self.progress_bar["value"] = percent
        self.master.update()

    def download_file(self):
        url = self.last_release_location
        destination = f"{self.temp_dir}/downloaded.tar.gz"  # Specifica il percorso di destinazione

        # Scarica il file
        urlretrieve(url, destination, reporthook=self.update_progress)

        # Estrai il file 
        self.extract_file()
        
        # Esegui il deploy
        self.run_deploy()

        # Carica pagina restart dopo che ha finito il download e l'installazione
        self.load_restartPage(self.master, 0, 0, self.master.winfo_screenheight(), self.master.winfo_screenwidth())

        # Termina il thread
        return 
   
    def extract_file(self):
        # self.percent_label["text"] = f"Estrazione dell'aggiornamento in corso..."
        try:
            with tarfile.open(f"{self.temp_dir}/downloaded.tar.gz" , 'r:gz') as tar:
                tar.extractall(f"{self.temp_dir}/downloaded" )
            print(f"Estrazione completata in: {self.temp_dir}/downloaded")
        except Exception as e:
            self.close_program(3)

    def run_deploy(self):
        # Trova il nome della cartella di rilascio
        elenco_cartelle = [d for d in os.listdir(os.path.join(self.temp_dir, "downloaded"))]

        if elenco_cartelle:
            nome_cartella_rilascio = elenco_cartelle[0]
            percorso_script = os.path.join(self.temp_dir, "downloaded", nome_cartella_rilascio, "deploy.sh")

            # Verifica se lo script deploy.sh esiste prima di avviarlo
            if os.path.exists(percorso_script):
                # Avvia lo script deploy.sh
                 # Avvia lo script deploy.sh
                if os.name == 'nt':  # Verifica se il sistema operativo è Windows
                    subprocess.run([percorso_script], shell=True)
                else:
                    subprocess.run(["bash", percorso_script])
            else:
                print(f"Lo script {percorso_script} non esiste.")
        else:
            print(f"Nessuna cartella di rilascio trovata.")
         
    def close_program(self, master, exitValue):

        # Chiudi l'interfaccia grafica
        self.exit_value = exitValue
        master.destroy()

# -------------------------------------------------------

    def create_background(self):
        # Carica l'immagine
        image = Image.open("./Logo.png")
        photo = ImageTk.PhotoImage(image)

        # Crea un widget Label per visualizzare l'immagine
        background_label = tk.Label(self.master, image=photo, bg=GINGER_WHITE)
        background_label.image = photo  # Mantiene un riferimento all'immagine per evitare la garbage collection

        # Posiziona l'immagine alle coordinate specificate
        background_label.place(x=33, y=23)

    def create_label(self, text, font_size, fg_color, x_coordinate, y_coordinate, box_width, height):
        label = tk.Label(self.master, text=text, font=("Arial", font_size), fg=fg_color, bg=GINGER_WHITE)
        label.place(x=x_coordinate, y=y_coordinate, width=box_width, height=height)

    def create_button(self, text, x, y, command_function):
        # Carica l'immagine
        image = Image.open("Button.png")
        photo = ImageTk.PhotoImage(image)

        # Crea un widget Label per visualizzare l'immagine con il testo sopra
        button_label = tk.Label(self.master, image=photo, text=text, compound=tk.CENTER, font=("Arial", 11), bg=GINGER_WHITE, fg=GINGER_RED)
        button_label.image = photo  # Mantiene un riferimento all'immagine per evitare la garbage collection

        # Collega l'evento di clic alla funzione specificata
        button_label.bind("<Button-1>", lambda event: command_function())

        # Posiziona il pulsante alle coordinate specificate
        button_label.place(x=x, y=y)
   
    def create_scrollTextArea(self, text, x_coordinate, y_coordinate, width, height):
        # Crea un Frame con sfondo grigio e angoli arrotondati
        frame = ttk.Frame(self.master, style="GrayFrame.TFrame")
        frame.place(x=x_coordinate, y=y_coordinate, width=width, height=height)

        # Aggiungi uno stile tematico per il Frame con sfondo grigio e angoli arrotondati
        style = ttk.Style()
        style.configure("GrayFrame.TFrame", background=GINGER_GRAY, borderwidth=5, relief="ridge", corner_radius=10)

        # Crea un widget Text all'interno del Frame per il testo scrollabile
        text_widget = tk.Text(frame, wrap="word", bg=GINGER_GRAY, borderwidth=0, highlightthickness=0, font=("Arial", 9))
        text_widget.insert("1.0", text)
        text_widget.config(state="disabled")  # Imposta lo stato a "disabled" per rendere il testo non modificabile
        text_widget.pack(expand=True, fill="both")
# -------------------------------------------------------

    def update_btn(self):
        self.load_progressPage(self.master, 0, 0, self.master.winfo_screenheight(), self.master.winfo_screenwidth())

    def close_btn(self):
        self.close_program(self.master, 1)

    def restart_btn(self):
        self.close_program(self.master, 0)
