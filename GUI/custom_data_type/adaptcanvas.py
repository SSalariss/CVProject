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
from typing import Optional

# os
import os



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
        super().__init__(master, highlightthickness=thickness)

        # Inizializza Image e PhotoImage
        self.__init_images__(image_path)

        # Configura la classe master in cui si trova
        self._master = master

        # Esegue il bind all'evento <Configure>
        self.bind("<Configure>", self.on_configure)


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
        # Estra la nuova dimensione del widget master
        new_size: tuple[int, int] = (event.width, event.height)
        
        # Esegue il ridimensionamento
        self._resize(new_size)
    

    @abstractmethod
    def _resize(self, new_size: tuple[int, int]) -> None: ...

    @abstractmethod
    def _set_image(self, new_image: PhotoImage) -> None: ...


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
        self._background_id = self.create_image(0, 0, image=self._photo_image, anchor="nw")

    
    # @override
    def _resize(self, size: tuple[int, int]) -> None:
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
        self._set_image(new_image)
        

    # @override
    def _set_image(self, new_image: Image):
        # Imposto la nuova immagine
        self._image = new_image

        # Creo la nuova PhotoImage dalla nuova immagine
        new_photo_image: PhotoImage = ImageTk.PhotoImage(new_image)

        # Imposto la nuova PhotoImage
        self._photo_image = new_photo_image

        # Imposto la PhotoImage come nuova immagine del canvas
        self.itemconfig(self._background_id, image=self._photo_image)
