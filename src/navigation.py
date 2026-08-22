# navigation.py

class GridNavigator:
    def __init__(self, root, cards, rows=3, cols=4):
        self.root = root
        self.cards = cards
        self.rows = rows
        self.cols = cols
        self.current_index = 0

        self._bind_keys()

    def _bind_keys(self):
        self.root.bind("<Up>", lambda e: self.move("Up"))
        self.root.bind("<Down>", lambda e: self.move("Down"))
        self.root.bind("<Left>", lambda e: self.move("Left"))
        self.root.bind("<Right>", lambda e: self.move("Right"))
        self.root.bind("<Return>", lambda e: self.execute_selected())
        self.root.bind("<KP_Enter>", lambda e: self.execute_selected())

    def move(self, direction):
        row = self.current_index // self.cols
        col = self.current_index % self.cols
        old_index = self.current_index

        if direction == "Up" and row > 0:
            row -= 1
        elif direction == "Down" and row < self.rows - 1:
            row += 1
        elif direction == "Left" and col > 0:
            col -= 1
        elif direction == "Right" and col < self.cols - 1:
            col += 1

        new_index = row * self.cols + col

        if 0 <= new_index < len(self.cards) and new_index != old_index:
            self.cards[old_index].deselect()
            self.current_index = new_index
            self.cards[self.current_index].select()

    def execute_selected(self):
        if self.cards and self.current_index < len(self.cards):
            self.cards[self.current_index].invoke()