# tkinter
import tkinter as tk
from tkinter import PhotoImage, Event

# PIL
from PIL import Image as ImageFactory, ImageTk
from PIL.Image import Image, Resampling

# ABC
from abc import ABC
from abc import abstractmethod

# typing
from typing import Optional, Callable, Self

# os
import os

class CanvasImage():
    
    _path: str
    _image: Image
    _current_pi: PhotoImage
    _id: int
    _resize_func: Callable[[tuple[int, int]], Image]


    def __init__(self, path: str, image: Image, current_pi: PhotoImage, id: int, resize_func: Callable[[Self, tuple[int, int]], None]):
        self._path = path
        self._image = image
        self._current_pi = current_pi
        self._id = id
        self._resize_func = resize_func

    def path(self):
        return self._path

    def image(self):
        return self._image
    
    def current_pi(self):
        return self._current_pi
    
    def id(self):
        return self._id
    
    def set_current_pi(self, pi: PhotoImage):
        self._current_pi = pi

    def resize(self, size: tuple[int, int]) -> None:
        self._resize_func(self, size)
    
    def __repr__(self):
        return f"image: {self._path}, id: {self._id}"




class AdaptCanvasABC(tk.Canvas, ABC):
    """
    Classe `tk.Canvas` con ridimensionamento.

    Questa classe e' un estensione della classe `tk.Canvas`,
    impone la gestione del ridimensionamento
    per ogni Widget, con immagine interna, che la estende.
    L'init di questa classe aggiunge al widget che la estende
    un binding a `<Configure>` che pero' non e' gestita da questa classe
    ma da un metodo astratto non implementato, tocca quindi alla sottoclasse
    implementarlo.
    """
    # Widget attributes
    _master: tk.Widget

    # childs
    _childs: list[CanvasImage]

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
        super().__init__(master, highlightthickness=thickness)

        # Configura la classe master in cui si trova
        self._master = master
        self._childs = list()

        # Esegue il bind all'evento <Configure>
        self.bind("<Configure>", self.on_configure)


    def __open_image__(self, path: str) -> Image:
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
        # Se il percorso non rappresenta un file
        # solleva un eccezione.
        if not os.path.isfile(path) :
            raise AttributeError(f"Il file {path} non e' valido.")
        
        # Genero l'Image tramite il path
        return ImageFactory.open(path)
    
    @abstractmethod
    def on_configure(self, event: Event) -> None: ...


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

        # Apro l'immagine indicata dal path
        image = self.__open_image__(image_path)

        # Converto l'image in una PhotoImage
        photo_image = ImageTk.PhotoImage(image)

        # Ottengo l'id dell'immagine creata
        id = self.create_image(0, 0, image=photo_image, anchor="nw")

        # Creo un CanvasImage in cui salvo i dati del background
        # appena creato
        self._background = CanvasImage(image_path, image, photo_image, id, resize_func=self.__whole_screen_resize__)

        # Salvo il background come figlio
        self._childs.append(self._background)

    # @overload
    def on_configure(self, event):
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
        # Estra la nuova dimensione del widget master
        new_size: tuple[int, int] = (event.width, event.height)

        # Per ogni figlio:
        for child in self._childs:

            child.resize(new_size)

    def __whole_screen_resize__(self, ci: CanvasImage, size: tuple[int, int]) -> Image:
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
        new_image : `Image`
            ritorna l'immagine ridimensionata presente nel widget.
        """
        # Prendo una copia dell'immagine e la ridimensiono
        # in base alla nuova dimensione `size` passata alla funzione.
        new_image = ci.image().resize(size, Resampling.LANCZOS)
        new_pi = ImageTk.PhotoImage(new_image)
        ci.set_current_pi(new_pi)
        self.itemconfig(ci.id(), image=ci.current_pi())


