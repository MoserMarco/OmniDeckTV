# main.py
import customtkinter as ctk
from .programCard import programCard
from .commands import NoOpCommand
from .navigation import GridNavigator
from . import config


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


root = ctk.CTk()
root.title("Program Launcher")
root.attributes("-fullscreen", True)

root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))


for i, weight in enumerate(config.COLUMN_WEIGHTS):
    root.grid_columnconfigure(i, weight=weight)

for i, weight in enumerate(config.ROW_WEIGHTS):
    root.grid_rowconfigure(i, weight=weight)


title_label = ctk.CTkLabel(
    root,
    text="HOME",
    font=("Helvetica", 40, "bold"),
    text_color="white",
    fg_color="transparent",
    anchor="center"
)
title_label.grid(row=0, column=1, columnspan=7, sticky="nsew", padx=0, pady=(20, 0))


program_cards = []
for index, item in enumerate(config.PROGRAMS_DATA):
    i = index // config.NUMBER_OF_COLUMNS
    j = index % config.NUMBER_OF_COLUMNS

    cmd = config.COMMAND_REGISTRY.get(item["name"], NoOpCommand())

    pc = programCard(
        master=root,
        image_path=item["image"],
        command=cmd,
        corner_radius=20
    )
    pc.grid(row=(i + 1) * 2, column=(1 + j * 2), sticky="nsew", padx=25, pady=25)
    program_cards.append(pc)


navigator = GridNavigator(root, program_cards, rows=config.NUMBER_OF_ROWS, cols=config.NUMBER_OF_COLUMNS)


root.after(200, lambda: program_cards[0].select())

root.mainloop()