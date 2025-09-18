import tkinter as tk
from PIL import ImageTk

from Utils import ImageUtils

import os



main_window = tk.Tk(className="Offside detector")
main_window.geometry("800x600")
main_window.configure()



background_image = ImageUtils.open_image("resources\\background.png")
background_image = ImageTk.PhotoImage(background_image)

background_window = tk.Label(main_window, image=background_image)
background_window.pack()



main_window.mainloop()