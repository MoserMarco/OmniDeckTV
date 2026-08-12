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


current_index = 0
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


def move_selection(direction):
    global current_index

    row = current_index // 3  # Calcola riga attuale (0, 1 o 2)
    col = current_index % 3  # Calcola colonna attuale (0, 1 o 2)

    old_index = current_index

    if direction == "Up" and row > 0:
        row -= 1
    elif direction == "Down" and row < 2:
        row += 1
    elif direction == "Left" and col > 0:
        col -= 1
    elif direction == "Right" and col < 2:
        col += 1

    new_index = row * 3 + col
    if new_index>8 or new_index<0:
        new_index = old_index

    # Se la selezione è cambiata, aggiorna lo stato grafico
    if new_index != old_index:
        programCards[old_index].deselect()
        current_index = new_index
        programCards[current_index].select()

def execute_selected(event=None):
    """Esegue il comando del bottone attualmente selezionato."""
    if programCards and current_index < len(programCards):
        programCards[current_index].invoke()

# BINDING DEI TASTI
root.bind("<Up>", lambda e: move_selection("Up"))
root.bind("<Down>", lambda e: move_selection("Down"))
root.bind("<Left>", lambda e: move_selection("Left"))
root.bind("<Right>", lambda e: move_selection("Right"))

# Tasto Invio (sia principale che del tastierino numerico)
root.bind("<Return>", execute_selected)
root.bind("<KP_Enter>", execute_selected)

# Seleziona il primo bottone all'avvio dell'applicazione
root.after(200, lambda: programCards[0].select())

root.mainloop()