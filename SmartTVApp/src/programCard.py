import customtkinter as ctk
from PIL import Image


class programCard(ctk.CTkButton):
    def __init__(self, master, command=None, image_path=None, **kwargs):

        kwargs.setdefault("text", "")
        kwargs.setdefault("fg_color", "black")
        kwargs.setdefault("hover_color", "black")
        kwargs.setdefault("corner_radius", 20)
        kwargs["state"] = "disabled"

        super().__init__(master, **kwargs)

        self.command_obj = command
        self.image_path = image_path
        self.pil_image_original = None
        self.ctk_image = None
        self.last_size = (0, 0)


        if self.image_path:
            try:
                self.pil_image_original = Image.open(self.image_path)
            except Exception as e:
                print(f"Errore caricamento immagine {self.image_path}: {e}")


        self.bind("<Configure>", self._update_image_size)

    def execute(self):

        if self.command_obj:
            self.command_obj.execute()



    def select(self):
        self.is_hovered = True
        self.configure(fg_color="#B01A1A")

    def deselect(self):
        self.is_hovered = False
        self.configure(fg_color="black")



    def _update_image_size(self, event):
        if not self.pil_image_original:
            return

        # Sottraiamo un piccolo margine (padding) per non toccare i bordi del bottone
        padding = 12
        target_w = max(10, event.width - (padding * 2))
        target_h = max(10, event.height - (padding * 2))


        # Evitiamo di ricalcolare per variazioni minime di pixel
        if abs(self.last_size[0] - target_w) < 3 and abs(self.last_size[1] - target_h) < 3:
            return

        self.last_size = (target_w, target_h)

        # Creiamo l'immagine specificando la DIMENSIONE REALE (size=...)
        self.ctk_image = ctk.CTkImage(
            light_image=self.pil_image_original,
            dark_image=self.pil_image_original,
            size=(target_w, target_h)  # <--- Questo ingrandisce l'immagine
        )

        # Applichiamo l'immagine direttamente al CTkButton (senza CTkLabel)
        self.configure(image=self.ctk_image)