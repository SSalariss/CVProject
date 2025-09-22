# tkinter
import tkinter as tk
from tkinter import PhotoImage

from PIL import Image as ImageFactory, ImageTk, ImageSequence
from PIL.Image import Image, Resampling

# ABC
from abc import ABC
from abc import abstractmethod

# Typing
from typing import Optional

# Custom classes
from custom_data_type.adaptcanvas import AdaptCanvas, CanvasImage

class GifCanvasABC(AdaptCanvas, ABC):
    """
    Canvas contenente una GIF.

    Questa classe si divide in due parti:
    - Estende `AdaptCanvas` e quindi ha un'immagine
        che si ridimensione automaticamente ogni qual volta viene
        invocato l'evento `<Configure>`
    - Contiene al suo interno un `AdaptCanvas` che, invece di una
        semplice immagine, contiene una GIF gestita internamente
        da questa classe.
    Essa quindi non e' altro che un `AdaptCanvas` ma che contieen al suo interno
    un ulteriore `AdaptCanvas` che viene gestito cone delle GIF.
    """

    # GIF Attributes
    _gif: CanvasImage

    # Animation attributes
    _frame_list: list[Image]
    _counter: int

    def __init__(self, master: tk.Widget, image_path: str, gif_path: str, thickness: Optional[int] = 0) -> None:
        # Supercostruttore
        super().__init__(master, image_path, thickness)
        
        # init
        self.__init_gif__(gif_path)
        self.__init_frame_list__()
        self.__animate__()

    def __init_gif__(self, gif_path):
        # Apro l'immagine puntata dal path
        gif_image = self.__open_image__(gif_path)

        # Converto l'Image in PhotoImage
        gif_pi = ImageTk.PhotoImage(gif_image)

        # Ottengo l'id della GIF
        gif_id = self.create_image(0, 0, image=gif_pi, anchor="se")

        # Creo un CanvasImage con le informazioni della GIF
        self._gif = CanvasImage(gif_path, gif_image, gif_pi, gif_id, self.__gif_resize__)
        self._childs.append(self._gif)

    def __init_frame_list__(self):
        self._counter = 0
        self._frame_list = list()
        #self._frame_list = list(frame.copy() for frame in ImageSequence.Iterator(self._gif.image()))
        self.__load_frames__(self._gif.path())

    def __load_frames__(self, path: str) -> list[Image]:
        with ImageFactory.open(path) as im:
            for frame in ImageSequence.Iterator(im):
                # Converti sempre in RGBA (così la trasparenza è rispettata)
                f = frame.convert("RGBA")
                
                # Crea un canvas trasparente grande quanto l'immagine
                new_frame = ImageFactory.new("RGBA", im.size, (0, 0, 0, 0))
                
                # Incolla sopra il frame (rispettando il canale alpha)
                new_frame.paste(f, (0, 0), f)
                
                self._frame_list.append(new_frame)

    @abstractmethod
    def __next_frame__(self): ...

    @abstractmethod
    def __animate__(self): ...

    @abstractmethod
    def __gif_resize__(self, ci: CanvasImage, size: tuple[int, int]): ...


class GifCanvas(GifCanvasABC):

    def __init__(self, master: tk.Widget, image_path: str, gif_path: str, thickness: Optional[int] = 0):
        super().__init__(master, image_path, gif_path, thickness)
        
    
    # @overload from AdaptCanvas
    def __gif_resize__(self, ci: CanvasImage, size: tuple[int, int]):
        # Estraggo le dimensioni x ed y
        # del widget master.
        x, y = size

        # Proporzioni
        X_PROP = 0.125
        Y_PROP = 0.25

        # Margine in base al valore
        # attuale di x
        MARGIN = x / 20

        # Calcolo le nuove dimensioni della GIF.
        new_size = (int(x * X_PROP), int(y * Y_PROP))
        
        # Ottengo una copia dell'immagine
        # della GIF ridimensionata
        new_gif: Image = self._frame_list[self._counter].resize(new_size, Resampling.LANCZOS)

        # Converto l'immagine ridimensionata in PhotoImage
        # ed aggiorno l'attributo di classe
        new_pi = ImageTk.PhotoImage(new_gif)
        ci.set_current_pi(new_pi)
        
        # Aggiorno l'immagine della GIF 
        self.itemconfig(ci.id(), image=ci.current_pi())

        # Aggiorno le coordinate della GIF
        self.coords(ci.id(), x-MARGIN, y)
        

    # @overload
    def __next_frame__(self):
        frame = self._frame_list[self._counter]
        self._counter = (self._counter + 1) % len(self._frame_list)
        return frame

    # @overload
    def __animate__(self):
        # Ottengo il prossimo frame
        next_frame = self.__next_frame__()
        
        # Estraggo la dimensione attuale della GIF
        size = (self._gif.current_pi().width(), self._gif.current_pi().height())

        # Eseguo un resize in quanto next_frame ritorna
        # soltanto l'immagine originale, dunque bisogna
        # eseguire un resize in caso l'immagine
        # fosse di dimensioni diverse.
        next_frame = next_frame.resize(size, Resampling.LANCZOS)

        new_pi = ImageTk.PhotoImage(next_frame)

        self._gif.set_current_pi(new_pi)

        # Aggiorno l'immagine attuale
        self.itemconfig(self._gif.id(), image=self._gif.current_pi())

        # Configuro il timer
        self.after(40, self.__animate__)
    
        