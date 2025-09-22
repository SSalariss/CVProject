import tkinter as tk
from playsound import playsound
import winsound

from typing import Optional

from custom_data_type.adaptcanvas import AdaptCanvas
from custom_data_type.borderbutton import BorderButton

class BackgroundCanvas(AdaptCanvas):
    def __init__(self, master: tk.Widget, image_path: str, thickness: Optional[int] = 0) -> None:
        """
        Inizializza la classe

        Inizializza la classe estraendo `Image` e `PhotoImage` dal `path` ed 
        inizializzando la superclasse `Adapt`.

        Parameters
        -------------
        master : `tk.Widget`
            Label master del widget.

        image_path : `str`
            Percorso all'immagine background che si vuole inserire.

        thickness : `int` | `None`
            Imposta lo spessore del bordo del widget.
        """

        # Inizializza la superclasse
        super().__init__(master, image_path, thickness)



class MainMenu():
    """
    Menu principale dell'applicazione

    Questa classe rappresenta il menu principale
    del progetto.
    """

    # Class attributes
    _master: tk.Widget
    _background: tk.Canvas
    _BACKGROUND_PATH: str = "resources\\menus\\main_menu\\background.png"

    def __init__(self, master):
        self._master = master
        self.__init_background__()
        self.__init_music__()
        self.__init_buttons__()


    def __init_background__(self):
        """
        Inizializza il background.

        Crea e configura il background del menu.
        """
        self._background = BackgroundCanvas(self._master, self._BACKGROUND_PATH)
        self._background.pack(fill="both", expand=True)

        self._background.columnconfigure(0, weight=5)
        self._background.columnconfigure(1, weight=1)
        self._background.columnconfigure(2, weight=5)
        self._background.rowconfigure(0, weight=25)
        self._background.rowconfigure(1, weight=1)
        self._background.rowconfigure(2, weight=7)

    def __init_buttons__(self):
        """
        Inizializza i pulsanti.

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
        winsound.PlaySound("resources\\sounds\\menu\\music.wav", winsound.SND_LOOP | winsound.SND_ASYNC)