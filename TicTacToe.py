import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic-Tac-Toe")
        self.master.configure(bg="#FFD700")
        
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(master, text="", font=("Comic Sans MS", 24, "bold"), width=6, height=2, command=lambda i=i, j=j: self.make_move(i, j), bg="#00CED1", fg="#FFFFFF")
                self.buttons[i][j].grid(row=i, column=j)
                
        self.reset_button = tk.Button(master, text="Reset", font=("Arial", 12), command=self.reset_game, bg="#FF6347", fg="#FFFFFF")
        self.reset_button.grid(row=3, columnspan=3, pady=10)
        
    def make_move(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            if self.check_winner():
                messagebox.showinfo("Congratulations!", f"Player {self.current_player} wins!")
                self.reset_game()
            elif self.check_draw():
                messagebox.showinfo("It's a Draw!", "The game is a draw.")
                self.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.current_player == "O":
                    self.bot_move()
    
    def bot_move(self):
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ""]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.make_move(row, col)
    
    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                self.highlight_winner(i, 0, i, 1, i, 2)
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                self.highlight_winner(0, i, 1, i, 2, i)
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            self.highlight_winner(0, 0, 1, 1, 2, 2)
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            self.highlight_winner(0, 2, 1, 1, 2, 0)
            return True
        return False
    
    def check_draw(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    return False
        return True
    
    def reset_game(self):
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="")
                self.buttons[i][j].config(bg="#00CED1")
                
    def highlight_winner(self, *coords):
        for i in range(0, len(coords), 2):
            row, col = coords[i], coords[i+1]
            self.buttons[row][col].config(bg="#FF8C00", fg="#FFFFFF")
                

def main():
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
