import tkinter as tk
from PIL import ImageTk

from Utils import ImageUtils

from strutture_dati import BackgroundImage

import os


main_window = tk.Tk(className="Offside detector")
main_window.geometry("800x600")
main_window.configure()


BackgroundImage(main_window, "resources\\background.png")



main_window.mainloop()