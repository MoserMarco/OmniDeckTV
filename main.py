import customtkinter
from commands import LaunchAppCommand, ExitCommand, PowerOffCommand, NoOpCommand
from programCard import programCard

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.title("Program Launcher")
#root.geometry("1000x700")


root.attributes("-fullscreen", True)

def close_fullscreen(event=None):
    root.attributes("-fullscreen", False)

root.bind("<Escape>", close_fullscreen)



column_weight = [1,5,1,5,1,5,1]
row_weight = [30,10,40,10,40,10,40,10]
command_registry = {
    "Kodi": LaunchAppCommand("kodi"),
    "DVD": LaunchAppCommand("dvd"),
    "Bluetooth": LaunchAppCommand("blueman-manager"),
    "Dolphin": LaunchAppCommand("dolphin-emu"),
    "Mame": LaunchAppCommand("mame"),
    "Exit": ExitCommand(root),
    "PowerOff": PowerOffCommand()
}
Programs=["Kodi", "DVD", "Bluetooth", "Dolphin", "Mame", "Extra1", "Extra2", "Exit", "PowerOff"]
Images=["Kodi.png", "DVD.png", "Bluetooth.png", "Dolphin.jpg", "Mame.jpeg", "Extra.jpeg", "Extra.jpeg", "Exit.png", "Poweroff.png"]
imagesRoot = "./Images/"
programCards = []
for i in range(7):
    root.grid_columnconfigure(i, weight=column_weight[i])

for i in range(8):
    root.grid_rowconfigure(i, weight=row_weight[i])

import customtkinter as ctk

# Sostituzione con CTkLabel
title_label = ctk.CTkLabel(
    root,
    text="HOME",
    font=("Helvetica", 40, "bold"), # Font grande e in grassetto
    text_color="white",             # Colore del testo
    fg_color="transparent",         # Sfondo trasparente
    anchor="center"                 # Centra il testo all'interno dello spazio della griglia
)

title_label.grid(row=0, column=1, columnspan=5, sticky="nsew", padx=0, pady=(20, 0))
for i in range(3):
    for j in range(3):


        pc = programCard(
            master=root,
            image_path=(imagesRoot+Images[i*3+j]),
            command= command_registry.get(Programs[i*3+j], NoOpCommand()),
            corner_radius=20

        )
        pc.grid(row=(i+1)*2, column=(1+j*2), sticky="nsew", padx=25, pady=25)
        programCards.append(pc)



root.mainloop()