import tkinter as tk

from menus.menu import MainMenu
from menus.loading import LoadingMenu
from menus.choosing import ChoosingMenu

from signals import Signals

from custom_data_type.borderbutton import FileChooser

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
        # Inizializzo la finestra root
        self.__init_main_window__()

        # Inizializzo la gestione dei segnali
        self.__init_signals_handler__()

        # Creo il main menu:
        # E' possibile crearlo tramite un sollevamento
        # di un evento virtuale ma, gli eventi virtuali,
        # possono essere sollevati soltanto dopo il mainloop
        # e quindi comporterebbe un output visivo bianco e,
        # dopo pochi millisecondi, la creazione del menu principale.
        # Per evitare cio' viene creato durante l'inizializzazione
        # della finestra root.
        # Qualsiasi altro menu che si vuole creare, compreso il main menu,
        # deve essere creato soltanto dopo un evento, questa e' l'unica eccezione. 
        self.__init_menu__(None)


    def __init_main_window__(self):
        """ Inizializza la finestra root. """
        # Costanti
        WINDOW_NAME: str = " Offside Detector"
        WINDOW_START_SIZE: str = "1200x600"

        # Inizializzo la finestra root
        self._main_window = tk.Tk(className=WINDOW_NAME)

        # Ne configuro le dimensioni
        self._main_window.geometry(WINDOW_START_SIZE)

        

    def __init_signals_handler__(self):
        """ Inizializza la gestione degli eventi virtuali. """
        
        # Esegue il bind per ogni evento virtuale associato ad un menu.
        self._main_window.bind(Signals.MAIN_MENU_SIG, self.__init_menu__)
        self._main_window.bind(Signals.LOADING_MENU_SIG, self.__init_loading_menu__)
        self._main_window.bind(Signals.CHOOSE_MENU_SIG, self.__init_choosing_menu__)
        #self._main_window.bind(Signals.FINAL_MENU_SIG, self.__init_final_menu__)

    def __init_menu__(self, _: tk.Event):
        """ Inizializza il menu iniziale. """
        self.__clear__()
        menu = MainMenu(self._main_window)
        
    
    def __init_loading_menu__(self, event: tk.Event):
        """ Inizializza il menu di caricamento. """
        LoadingMenu(self._main_window)
        

    def __init_choosing_menu__(self, event: tk.Event):
        """ 
        Inizializza il menu di selezione delle squadre. 
        
        Per inizializzare in modo corretto il menu di scelta,
        la classe che solleva l'evento virtuale associato, deve estendere
        `FileChooser`, altrimenti non sara' possibile inizializzare in modo
        corretto il menu'.
        Cio' e' conseguenza del fatto che il menu ha bisogno di un'immagine
        selezionata dall'utente.
        
        Raises
        -----------
        RuntimeError
            Se l'evento non e' stato sollevato da una sottoclasse di `FileChooser`
        """
        # Ottengo il widget che ha sollevato l'evento
        widget = event.widget

        # Se il widget non e' un istanza di FileChooser:
        # allora esso non contiene alcun file e cio' rende
        # impossibile l'inizializzazione del menu si scelta.
        if not isinstance(widget, FileChooser):
            # Solleva un errore.
            raise RuntimeError("Il menu' di caricamento non puo' essere chiamato da una classe che non estende FileChooser.")
        
        # Estraggo il file contenuto dal widget
        file = widget.file()

        # Se non abbiamo alcun file, ritorna
        if not file: return

        # Libera la finestra root da tutti i widget
        self.__clear__()

        # Inizializza il menu di scelta.
        ChoosingMenu(self._main_window, file)


    def __init_final_menu__(self, _: tk.Event):
        """ Inizializza il menu finale. """
        self.__clear__()
        #FinalMenu(self._main_window)


    def __clear__(self):
        """
        Rimuove tutti i widget dalla finestra roow,
        utile per quando si vuole "cambiare" menu.
        """
        for widget in self._main_window.winfo_children():
            widget.destroy()
        
    def start(self) -> None:
        """
        Unica funzione del controller, crea e
        gestisce la GUI.
        """
        # Inizia il mainloop
        self._main_window.mainloop()