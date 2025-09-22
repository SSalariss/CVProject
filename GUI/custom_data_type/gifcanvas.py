# tkinter
import tkinter as tk
from tkinter import PhotoImage

from PIL import Image as ImageFactory, ImageTk, ImageSequence
from PIL.Image import Image

# ABC
from abc import ABC
from abc import abstractmethod

# Typing
from typing import Optional

# Custom classes
from custom_data_type.adaptcanvas import AdaptCanvas

class GifCanvasABC(AdaptCanvas, ABC):
    """
    Gestisce canvas contenenti GIF.

    La classe rappresenta un'estensione di `tk.Canvas`, precisamente
    estende la classe `AdaptCanvas` e ne impone la gestione di GIF.
    """
    _gif: Image
    _frame_list: list[Image]
    _current_frame: int
    _counter: int

    def __init__(self, master: tk.Widget, image_path: str, gif_path: str, thickness: Optional[int] = 0) -> None:
        # Supercostruttore
        super().__init__(master, image_path, thickness)
        
        # init
        self.__init_gif__(gif_path)
        self.__init_frame_list__()
        #self._animate()

    def __init_gif__(self, gif_path):
        self._gif = ImageFactory.open(gif_path)

    def __init_frame_list__(self):
        self._current_frame = 0
        self._counter = 0
        self._frame_list = list(frame.copy() for frame in ImageSequence.Iterator(self._gif))


    @abstractmethod
    def __next_frame__(self): ...

    @abstractmethod
    def __animate__(self): ...


class GifCanvas(GifCanvasABC):

    def __init__(self, master: tk.Widget, image_path: str, gif_path: str, thickness: Optional[int] = 0):
        super().__init__(master, image_path, gif_path, thickness)
        
    def start_animation(self):
        self._animate()

    # @overload
    def __next_frame__(self):
        frame = self._frame_list[self._counter]
        self._counter = (self._counter + 1) % len(self._frame_list)
        return frame

    # @overload
    """
    Non posso utilizzare _set_frame in quanto cambia l'immagine
    a tutto il widget, dovrei creare un GifCanvas ed utilizzarlo
    per la gif inserendolo in qualche angolo dello schermo.
    """
    def __animate__(self):
        next_frame = self.__next_frame__()
        self._set_image(next_frame)
        self.after(100, self.__animate__)

    
        