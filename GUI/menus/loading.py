import tkinter as tk

from custom_data_type.gifcanvas import GifCanvas

class LoadingMenu:

    _master: tk.Widget
    _background: tk.Canvas
    _BACKGROUND_PATH: str = "resources\\menus\\loading_menu\\background.png"
    _GIF_PATH: str = "resources\\menus\\loading_menu\\loading.gif"


    def __init__(self, master: tk.Widget):
        self._background = GifCanvas(master, self._BACKGROUND_PATH, self._GIF_PATH)
        self._background.pack(expand=True, fill="both")



    def __init_background__(self): ...

