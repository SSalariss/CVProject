from typing import Optional

from PIL import Image as ImageFactory, ImageTk
from PIL.Image import Image, Resampling

from tkinter import PhotoImage

import os


class ImageUtils:
    """
    Classe utilitaria per la gestione di immagini.
    """

    @staticmethod
    def resize(image: Image, new_width: int, new_height: int) -> Image:
        """
        Crea una copia del parametro `image` con dimensione pari a (`new_width`x`new_height`)

        Parameters
        ----------------
        image : Image
            immagine a cui si vuole modificare la dimensione.

        new_width : int 
            la nuova larghezza dell'immagine.

        new_height : int
            la nuova lunghezza dell'immagine.

        Returns
        ----------------
        image : Image
            ritorna un'immagine con dimensione pari a (`new_width`x`new_height`)
        """

        # Creo una tupla rappresentante la nuova
        # dimensione desiderata.
        new_size: tuple[int, int] = (new_width, new_height)

        # Chiamo la funzione resize() che restituisce una copia
        # dell'immagine con dimensione new_width x new_height
        resized: Image = image.resize(new_size, Resampling.LANCZOS)

        return resized
    
    
    @staticmethod
    def open_image(path: str, valid_extension: Optional[tuple[str]] = ".png", width: Optional[int] = None, height: Optional[int] = None) -> Image:
        """
        Apre l'immagine indicata dal path.

        Crea un'immagine `Image` tramite il parametro `path` avente come dimensione
        la dimensione dell'immagine stessa oppure (`width` x `height`) se presenti.

        Parameters
        ------------
        path : str
            stringa rappresentante un percorso ad un'immagine.

        width : int | None
            larghezza dell'immagine risultante. Se None allora l'immagine avra'
            la sua larghezza di default.

        height : int | None
            lunghezza dell'immagine risultante. Se None allora l'immagine avra'
            la sua lunghezza di default.

        valid_extensions : tuple[str] | None
            rappresenta tutte le estensioni accettabili. Se None allora
            si accetteranno soltanto immagini png

        Return
        -------------
        image : Image
            immagine indicata nel percorso `path` avente le sue dimensioni standard 
            oppure `width` x `height` se presenti

        Raises
        ------------
        AttributeError
            se il path non indica alcun file oppure se il file
            non ha un estensione valida.
        """

        # Se il percorso non rappresenta un file oppure
        # il file non termina con un estensione ammessa allora
        # solleva un eccezione.
        if ( (not os.path.isfile(path)) or (not path.endswith(valid_extension)) ) :
            raise AttributeError(f"Il file {path} non e' valido.")
        
        # Apro l'immagine presente nel path
        image: Image = ImageFactory.open(path)

        # Se i parametri di width e height sono presenti
        # allora effettuo il resize dell'immagine
        if width and height:
            image = ImageUtils.resize(image, width, height)

        # Ritorno l'immagine
        return image
    
    
    @staticmethod
    def open_image_tk(path: str, valid_extension: Optional[tuple[str]] = ".png", width: Optional[int] = None, height: Optional[int] = None) -> PhotoImage:
        """
        Apre l'immagine indicata dal path.

        Crea un'immagine `PhotoImage` tramite il parametro `path` avente come dimensione
        la dimensione dell'immagine stessa oppure (`width` x `height`) se presenti.

        Parameters
        ------------
        path : str
            stringa rappresentante un percorso ad un'immagine.

        width : int | None
            larghezza dell'immagine risultante. Se None allora l'immagine avra'
            la sua larghezza di default.

        height : int | None
            lunghezza dell'immagine risultante. Se None allora l'immagine avra'
            la sua lunghezza di default.

        valid_extensions : tuple[str] | None
            rappresenta tutte le estensioni accettabili. Se None allora
            si accetteranno soltanto immagini png

        Return
        -------------
        image : PhotoImage
            immagine indicata nel percorso `path` avente le sue dimensioni standard 
            oppure `width` x `height` se presenti

        Raises
        ------------
        AttributeError
            se il path non indica alcun file oppure se il file
            non ha un estensione valida.
        """
        image = ImageUtils.open_image(path, valid_extension, width, height)
        tk_image = ImageTk.PhotoImage(image)

        return tk_image
        
