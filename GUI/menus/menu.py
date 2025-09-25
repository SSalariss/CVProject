import tkinter as tk

import winsound

from custom_data_type.canvasitem import AdaptCanvasItem
from custom_data_type.adaptcanvas import AdaptCanvas
from custom_data_type.borderbutton import BorderButton
from resize import Resize

class MainMenu():
    """
    Menu principale dell'applicazione

    Questa classe rappresenta il menu principale
    del progetto.
    """

    # Class attributes
    _master: tk.Widget
    _background: AdaptCanvas
    _BACKGROUND_PATH: str = "resources\\menus\\main_menu\\background.png"

    def __init__(self, master):
        """ Inizializza il menu """
        self._master = master
        self.__init_background__()
        self.__init_music__()
        self.__init_buttons__()


    def __init_background__(self):
        """
        Inizializza il background.

        Crea e configura il background del menu.
        """
        # Creo il background
        self._background = AdaptCanvas(self._master)

        # Creo l'immagine con una funzione
        # di resize che occupa l'intero schermo
        self._background.add_image(self._BACKGROUND_PATH, resize_func=self.__background_resize__)
        
        # Inserisco il background nel finestra root.
        self._background.pack(fill="both", expand=True)

        # Configuro il background a griglia
        self._background.columnconfigure(0, weight=5)
        self._background.columnconfigure(1, weight=1)
        self._background.columnconfigure(2, weight=5)
        self._background.rowconfigure(0, weight=25)
        self._background.rowconfigure(1, weight=1)
        self._background.rowconfigure(2, weight=7)

    def __init_buttons__(self):
        """
        Inizializza i pulsanti del menu.

        Crea e configura i pulsanti del menu.
        """
        # Creo e configuro il pulsante avete un bordo
        button = BorderButton(self._background, 1, "#23AECA", text="Let's start!", font=("Aerial", 20))
        button.btn_bd_on_enter("#14414E")           # Border color on enter
        button.btn_bg_on_enter("#E0E0E0")           # Background color on enter
        button.config(activebackground="#CCCCCC")   # Background color on press

        # Assegno il frame tramite `grid`
        button.get_frame().grid(row=1, column=1, sticky="nswe")

        # Aggiungo gli eventi virtuali
        button.add_event_on_click("<<SIGMenu>>")


    def __init_music__(self):
        """ Inizializza la musica di sottofondo del menu. """
        winsound.PlaySound("resources\\sounds\\menu\\music.wav", winsound.SND_LOOP | winsound.SND_ASYNC)


    def __background_resize__(self, aci: AdaptCanvasItem, size: tuple[int, int]) -> None:
        """
        Funzione di resize per `AdaptCanvasItem`

        La funzione ridimensiona l'`AdaptCanvasItem` affinche'
        occupi tutto il widget master.

        Vedi anche `custom_data_tyes.canvasitem.AdaptCanvasItem`
        """
        # Prendo una copia dell'immagine e la ridimensiono
        # in base alla nuova dimensione `size` passata alla funzione.
        Resize.resize(aci, size)
        self._background.itemconfig(aci.id(), image=aci.current_pi())