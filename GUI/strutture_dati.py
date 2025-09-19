from PIL import Image as ImageFactory, ImageTk
from PIL.Image import Image, Resampling

import tkinter as tk
from tkinter import PhotoImage
from tkinter import Event

from abc import ABC
from abc import abstractmethod

import os


class AdaptImageABC(ABC):
    _master: tk.Tk
    _label: tk.Label

    def __init__(self, master: tk.Tk) -> None:
        """
        Inizializza la classe Adapt

        La classe obbliga un binding all'evento
        `<Configure>` gestita dalla funzione `resize` implementata dalla sottoclasse
        affinche' ogni sottoclasse possa gestire il ridimensionamento del widget.

        Notare che la classe non applica alcun `config` al widget, obbliga soltanto
        la gestione dell'evento `<Configure>` tramite la funzione `resize`.

        Parameters
        --------------
        master : `tk.Tk`
            Finestra master del widget.
        """
        self._master = master

        self._label = tk.Label(self._master)
        self._label.bind("<Configure>", self.on_configure)
        self._label.pack(fill="both", expand=True)


    @abstractmethod
    def resize(self, new_size: tuple[int, int]) -> PhotoImage: ...

    
    def on_configure(self, event: Event):
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



class BackgroundImage(AdaptImageABC):
    _path: str
    _image: Image
    _photo_image: PhotoImage


    def __init__(self, master: tk.Tk, path: str) -> None:
        """
        Inizializza la classe

        Inizializza la classe estraendo `Image` e `PhotoImage` dal `path` ed 
        inizializzando la superclasse `Adapt`.

        Parameters
        -------------
        master : `tk.Tk`
            Label master del widget.

        path : `str`
            Percorso all'immagine background che si vuole inserire.
        """

        # Inizializza Image e PhotoImage
        self.__init_images__(path)

        # Inizializza la superclasse
        super().__init__(master)

        # La superclasse generica non
        # imposta alcuna immagine, quindi
        # tocca a questa classe settarla.
        self._label.config(image=self._photo_image)


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
        self.path = path

        # Se il percorso non rappresenta un file
        # solleva un eccezione.
        if not os.path.isfile(path) :
            raise AttributeError(f"Il file {path} non e' valido.")
        
        # Genero l'Image tramite il path
        self._image = ImageFactory.open(path)

        # Genero la PhotoImage tramite l'Image precedente
        self._photo_image = ImageTk.PhotoImage(image=self._image)



    # @override
    def resize(self, size: tuple[int, int]) -> PhotoImage:
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
        image: Image = self._image.resize(size, Resampling.LANCZOS)

        # Aggiorno l'attributo di classe _photo_image
        self._photo_image = ImageTk.PhotoImage(image)

        # Imposto la nuova _photo_image come nuova
        # immagine del widget
        self._label.config(image=self._photo_image)

        
