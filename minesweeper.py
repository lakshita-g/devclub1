import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper")
        self.rows = 10
        self.cols = 10
        self.mines = 10
        self.buttons = []
        self.mines_positions = []
        self.game_over = False
        self.flags_placed = 0
        self.cells_revealed = 0
        
        # Create mine counter label
        self.mine_label = tk.Label(master, text=f"Mines: {self.mines - self.flags_placed}")
        self.mine_label.grid(row=0, column=0, columnspan=self.cols)
        
        # Create game board
        self.create_board()
        self.place_mines()
        
    def create_board(self):
        # Create buttons for each cell
        for row in range(self.rows):
            button_row = []
            for col in range(self.cols):
                button = tk.Button(self.master, width=2, height=1)
                button.bind('<Button-1>', lambda e, r=row, c=col: self.click(r, c))
                button.bind('<Button-3>', lambda e, r=row, c=col: self.place_flag(r, c))
                button.grid(row=row+1, column=col)
                button_row.append({
                    'button': button,
                    'mine': False,
                    'value': 0,
                    'revealed': False,
                    'flagged': False
                })
            self.buttons.append(button_row)
    
    def place_mines(self):
        # Randomly place mines
        mines_placed = 0
        while mines_placed < self.mines:
            row = random.randint(0, self.rows-1)
            col = random.randint(0, self.cols-1)
            if not self.buttons[row][col]['mine']:
                self.buttons[row][col]['mine'] = True
                self.mines_positions.append((row, col))
                mines_placed += 1
                
        # Calculate numbers for adjacent cells
        for row, col in self.mines_positions:
            for r in range(max(0, row-1), min(self.rows, row+2)):
                for c in range(max(0, col-1), min(self.cols, col+2)):
                    if not self.buttons[r][c]['mine']:
                        self.buttons[r][c]['value'] += 1
    
    def click(self, row, col):
        if self.game_over or self.buttons[row][col]['flagged']:
            return
        
        if self.buttons[row][col]['mine']:
            # Game Over
            self.game_over = True
            self.reveal_all_mines()
            messagebox.showinfo("Game Over", "You hit a mine!")
            return
        
        self.reveal_cell(row, col)
        
        # Check for win
        if self.cells_revealed == (self.rows * self.cols - self.mines):
            self.game_over = True
            messagebox.showinfo("Congratulations!", "You won!")
    
    def reveal_cell(self, row, col):
        if (row < 0 or row >= self.rows or 
            col < 0 or col >= self.cols or 
            self.buttons[row][col]['revealed'] or 
            self.buttons[row][col]['flagged']):
            return
        
        self.buttons[row][col]['revealed'] = True
        self.cells_revealed += 1
        cell = self.buttons[row][col]
        
        if cell['value'] == 0:
            cell['button'].configure(text="", relief=tk.SUNKEN, bg='lightgray')
            # Reveal adjacent cells
            for r in range(max(0, row-1), min(self.rows, row+2)):
                for c in range(max(0, col-1), min(self.cols, col+2)):
                    if not self.buttons[r][c]['revealed']:
                        self.reveal_cell(r, c)
        else:
            cell['button'].configure(text=str(cell['value']), relief=tk.SUNKEN)
    
    def place_flag(self, row, col):
        if self.game_over or self.buttons[row][col]['revealed']:
            return
        
        cell = self.buttons[row][col]
        if not cell['flagged'] and self.flags_placed < self.mines:
            cell['button'].configure(text="🚩", fg='red')
            cell['flagged'] = True
            self.flags_placed += 1
        elif cell['flagged']:
            cell['button'].configure(text="")
            cell['flagged'] = False
            self.flags_placed -= 1
            
        self.mine_label.configure(text=f"Mines: {self.mines - self.flags_placed}")
    
    def reveal_all_mines(self):
        for row, col in self.mines_positions:
            self.buttons[row][col]['button'].configure(text="💣", bg='red')

def main():
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()

if __name__ == "__main__":
    main() 