from PIL import Image as ImageFactory, ImageTk
from PIL.Image import Image, Resampling

import tkinter as tk
from tkinter import PhotoImage, Event

from abc import ABC
from abc import abstractmethod

from typing import Optional
from sound import SoundManager

import os




class AdaptCanvasABC(ABC):
    """
    Questa classe astratta impone la gestione del ridimensionamento
    per ogni Widget, con immagine interna, che la estende.
    L'init di questa classe aggiunge al widget che la estende
    un binding a `<Configure>` che pero' non e' gestita da questa classe
    ma da un metodo astratto non implementato, tocca quindi alla sottoclasse
    implementarlo.
    """
    # Widget attributes
    _master: tk.Widget
    _canvas: tk.Canvas

    # AdaptCanvas attributes
    _path: str
    _image: Image
    _photo_image: PhotoImage

    # Canvas attributes
    _background_id: int

    def __init__(self, master: tk.Widget, image_path: str, thickness: Optional[int] = 0) -> None:
        """
        Inizializza la classe Adapt

        La classe obbliga un binding all'evento
        `<Configure>` gestita dalla funzione `resize` implementata dalla sottoclasse
        affinche' ogni sottoclasse possa gestire il ridimensionamento del widget.

        Notare che la classe non applica alcun `config` al widget, obbliga soltanto
        la gestione dell'evento `<Configure>` tramite la funzione `resize`.

        Parameters
        --------------
        master : `tk.Widget`
            Finestra master del widget.

        image_path: `str`
            Percorso dell'immagine presente nel widget.

        thickness : int | None
            Imposta lo spessore del bordo del widget.
        """
        self.__init_images__(image_path)

        self._master = master
        self._canvas = tk.Canvas(self._master, highlightthickness=thickness)
        self._canvas.bind("<Configure>", self.on_configure)


    def __init_images__(self, path: str) -> None:
        """
        Apre l'immagine indicata dal path

        Crea un `Image` per l'attributo `self._image` ed una `PhotoImage` per l'attributo
        `self._photo_image`

        Parameters
        --------------
        path : str
            Percorso valido ad un immagine

        Raises
        ------------
        AttributeError
            se il path non indica alcun file oppure se il file
            non ha un estensione valida.
        """

        # Setto l'attributo path
        self._path = path

        # Se il percorso non rappresenta un file
        # solleva un eccezione.
        if not os.path.isfile(path) :
            raise AttributeError(f"Il file {path} non e' valido.")
        
        # Genero l'Image tramite il path
        self._image = ImageFactory.open(path)

        # Genero la PhotoImage tramite l'Image precedente
        self._photo_image = ImageTk.PhotoImage(image=self._image)
    
    def on_configure(self, event: Event) -> None:
        """
        Gestisce l'evento `<Configure>`

        Quando la label `master` subisce un ridimensionamento
        essa chiamera' questa funzione che, a sua volta, chiamera
        la funzione `resize` passando la nuova dimensione della label master
        come argomento.
        Cio' significa che qualsiasi classe che estende `Adapt` deve implementare
        una funzione `resize` che
        gestisce il ridimensionamento del widget `self`
        """
        new_size: tuple[int, int] = (event.width, event.height)
        self.resize(new_size)


    def canvas(self):
        return self._canvas
    

    @abstractmethod
    def resize(self, new_size: tuple[int, int]) -> None: ...

    @abstractmethod
    def set_image(self, new_image: PhotoImage) -> None: ...


class AdaptCanvas(AdaptCanvasABC):
    """
    Questa classe implementa tutti i metodi richiesti da `AdaptCanvasABC`

    Questa classe implementa il metodo `resize`, in modo generico,
    della classe `AdaptCanvasABC`: ogni sottoclasse non dovra'
    preoccuparsi di implementare alcun metodo in quanto e' tutto
    gestito.
    
    Se si vuole scrivere un proprio metodo `resize` allora
    bisogna implementare la classe `AdaptCanvasABC` e non questa.

    """

    def __init__(self, master: tk.Widget, image_path: str, thickness: Optional[int] = 0) -> None:
        """
        Inizializza la classe AdaptCanvas

        La classe implementa una sua configurazione standard
        per il metodo `resize` richiesto dalla superclasse `AdaptCanvasABC`,
        dunque non e' richiesto di implementare alcun metodo.

        Parameters
        --------------
        master : `tk.Widget`
            Finestra master del widget.

        image_path : `str`
            Percorso dell'immagine presente nel widget.

        thickness : `int` | `None`
            Imposta lo spessore del bordo del widget.
        """
        # Inizializza la superclasse
        super().__init__(master, image_path, thickness)

        # La superclasse generica non
        # imposta alcuna immagine, quindi
        # tocca a questa classe settarla.
        self._background_id = self._canvas.create_image(0, 0, image=self._photo_image, anchor="nw")

    
    # @override
    def resize(self, size: tuple[int, int]) -> None:
        """
        Ridimensiona il widget.

        Ridimensiona il widget in base alla nuova dimensione
        del widget master.

        Parameters
        ------------
        size: `tuple[int, int]`
            dimensione che il widget deve assumere

        Returns
        ------------
        photo_image : `PhotoImage`
            ritorna l'immagine ridimensionata presente nel widget.
        """
        # Prendo una copia dell'immagine e la ridimensiono
        # in base alla nuova dimensione `size` passata alla funzione.
        new_image: Image = self._image.resize(size, Resampling.LANCZOS)

        # Imposta la nuova immagine
        self.set_image(new_image)
        

    # @override
    def set_image(self, new_image: Image):
        # Imposto la nuova immagine
        self._image = new_image

        # Creo la nuova PhotoImage dalla nuova immagine
        new_photo_image: PhotoImage = ImageTk.PhotoImage(new_image)

        # Imposto la nuova PhotoImage
        self._photo_image = new_photo_image

        # Imposto la PhotoImage come nuova immagine del canvas
        self._canvas.itemconfig(self._background_id, image=self._photo_image)





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


class BorderButton(tk.Button):
    """
    Crea un `tk.Button` con bordo.

    Essendo che la classe `tk.Button` non possiede alcun metodo per
    modificare il colore del bordo, la classe crea un `tk.Frame` ed
    inserisce il pulsante al suo interno con un certo padding affinche'
    simuli un bordo.
    La classe e' un `tk.Button`, per ottenere il frame che la contiene vedi `get_frame`.

    Notare che la classe inserisce `master` come widget padre di `tk.Frame` e `tk.Frame` come 
    padre di `tk.Button`, se `tk.Button` viene inserito in modo automatico dalla classe nel `tk.Frame` tramite
    `pack`, cio' non accade con `tk.Frame`, infatti sara' poi l'utente ad inserirlo tramite `pack` o `grid` nel
    `master`. Ricorda che per modificare il `tk.Frame` che contiene il `tk.Button` bisogna utilizzare il metodo `get_frame`
    """
    # Frame attributes
    _outline: tk.Frame
    
    # Button attributes
    _button_color_on_enter: str
    _button_color_on_leave: str


    # Border attributes
    _border_color_on_enter: str
    _border_color_on_leave: str

    # On click events
    _on_click_events: set[str]

    def __init__(self, master=None, bd_width: Optional[int] = 1, bd_color: Optional[str] = "#FFFFFF", cnf={}, **kw) -> None:
        """
        Inizializza la classe

        A differenza del normale `tk.Button`, questa classe possiede un bordo, bisogna
        quindi specificarne la dimensione `bd_width` e il colore `bd_color`, e'
        modificare qualsiasi altro parametro presente nella classe `tk.Button`.

        Parameters
        --------------
        master : `tk.Widget` | None
            Il widget nel quale verra' inserito il `tk.Frame` che contiene il `tk.Button`

        bd_width : `int` | `None`
            Spessore del bordo

        bd_color : `str` | `None`
            Colore del bordo, sono accettati colori come "red" o "#FF0000"

        cnf : `dict[str, Any]` | None
            Dizionario utilizzato per compatibilita', vedi `tk.Button`

        **kw : `dict[str, Any] | None`
            Dizionario standard utilizzato per la configurazione della classe, vedi `tk.Button`
        """
        self._outline = tk.Frame(master, padx=bd_width, pady=bd_width, background=bd_color)
        kw["borderwidth"] = kw.get("borderwidth", 0)
        kw["command"] = kw.get("command", self._on_click)

        super().__init__(self._outline, cnf, **kw)

        self._on_click_events = set()

        self._border_color_on_enter = bd_color
        self._border_color_on_leave = bd_color

        self._button_color_on_enter = self.cget("bg")
        self._button_color_on_leave = self.cget("bg")

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

        self.pack(expand=True, fill="both")



    def get_frame(self) -> tk.Frame:
        """
        Ritorna il frame

        Returns
        ----------
        frame : `tk.Frame`
            Ritorna il frame nel quale e' contenuto il `tk.Button`
        """
        return self._outline
    
    def add_event_on_click(self, virtual_event: str):
        self._on_click_events.add(virtual_event)

    def _on_click(self):
        SoundManager.reproduce("resources\sounds\effects\mouse_click_effect.wav", False)
        for event in self._on_click_events:
            self.event_generate(event)

    def btn_bd_on_enter(self, color: str):
        self._border_color_on_enter = color

    def btn_bd_on_leave(self, color: str) :
        self._border_color_on_leave = color
    
    def btn_bg_on_enter(self, color: str):
        self._button_color_on_enter = color

    def btn_bg_on_leave(self, color: str):
        self._button_color_on_leave = color

    def on_enter(self, _):
        self.config(background=self._button_color_on_enter)
        self._outline.config(background=self._border_color_on_enter)

    def on_leave(self, _):
        self.config(background=self._button_color_on_leave)
        self._outline.config(background=self._border_color_on_leave)
    







class MainMenu():
    """
    Menu principale dell'applicazione

    Questa classe rappresenta il menu principale
    del progetto.
    """

    # Class attributes
    _master: tk.Widget
    _background: BackgroundCanvas
    _BACKGROUND_PATH: str = "resources\\menu\\background.png"

    def __init__(self, master):
        self._master = master
        self.__init_background__()
        self.__init_buttons__()


    def __init_background__(self):
        """
        Inizializza il background.

        Crea e configura il background del menu.
        """
        self._background = BackgroundCanvas(self._master, self._BACKGROUND_PATH)
        self._background.canvas().pack(fill="both", expand=True)

        self._background.canvas().columnconfigure(0, weight=5)
        self._background.canvas().columnconfigure(1, weight=1)
        self._background.canvas().columnconfigure(2, weight=5)
        self._background.canvas().rowconfigure(0, weight=25)
        self._background.canvas().rowconfigure(1, weight=1)
        self._background.canvas().rowconfigure(2, weight=7)

    def __init_buttons__(self):
        """
        Inizializza i pulsanti.

        Crea e configura i pulsanti del menu.
        """
        button = BorderButton(self._background.canvas(), 1, "#23AECA", text="Let's start!", font=("Aerial", 20))
        button.btn_bd_on_enter("#14414E")           # Border color on enter
        button.btn_bg_on_enter("#E0E0E0")           # Background color on enter
        button.config(activebackground="#CCCCCC")   # Background color on press

        button.get_frame().grid(row=1, column=1, sticky="nswe")
        button.add_event_on_click("<<SIGMenu>>")


class Main:
    _main_window: tk.Tk
    
    def __init__(self):
        self.__init_main_window__()
        self.__init_menu__()


    def __init_main_window__(self):
        WINDOW_NAME: str = " Offside Detector"
        WINDOW_START_SIZE: str = "1200x600"

        self._main_window = tk.Tk(className=WINDOW_NAME)
        self._main_window.geometry(WINDOW_START_SIZE)


    def __init_menu__(self):
        menu = MainMenu(self._main_window)
        self._main_window.bind("<<SIGMenu>>", self.__signal_from_menu__)


    def __signal_from_menu__(self, event):
        print("Devo cambiare pagina")
        
        




    def start(self) -> None:
        self._main_window.mainloop()