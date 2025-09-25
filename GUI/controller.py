import tkinter as tk

from menus.menu import MainMenu
from menus.loading import LoadingMenu

class Controller:
    """
    Classe principale della GUI, gestisce la comunicazione
    tra i vari menu.
    """
    # Class Attributes
    _main_window: tk.Tk
    

    def __init__(self):
        """
        Inizializza la classe inizializzando
        la finestra root e il menu iniziale.
        """
        self.__init_main_window__()
        self.__init_menu__()


    def __init_main_window__(self):
        """ Inizializza la finestra root. """
        WINDOW_NAME: str = " Offside Detector"
        WINDOW_START_SIZE: str = "1200x600"

        self._main_window = tk.Tk(className=WINDOW_NAME)
        self._main_window.geometry(WINDOW_START_SIZE)


    def __init_menu__(self):
        """ Inizializza il menu iniziale. """
        menu = MainMenu(self._main_window)
        self._main_window.bind("<<SIGMenu>>", self.__signal_from_menu__)


    def __clear__(self):
        """
        Rimuove tutti i widget dalla finestra roow,
        utile per quando si vuole "cambiare" menu.
        """
        for widget in self._main_window.winfo_children():
            widget.destroy()


    def __signal_from_menu__(self, event):
        """
        Si occupa della gestione degli eventi
        provenienti dal menu iniziale.

        In modo specifico, dopo un virtual event\
        scatenato dal menu, rimuove tutti i widget
        e inizializza il loading menu.
        """
        self.__clear__()
        self.__init_loading_menu__()
        

    def __init_loading_menu__(self):
        """ Inizializza il menu di caricamento. """
        LoadingMenu(self._main_window)
        





    def start(self) -> None:
        """
        Unica funzione del controller, crea e
        gestisce la GUI.
        """
        self._main_window.mainloop()