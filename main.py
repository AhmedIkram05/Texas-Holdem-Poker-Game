try:
    import tkinter as tk
    from tkinter import simpledialog
except ModuleNotFoundError:
    print("Error: tkinter module not found. Install Tcl/Tk support (e.g., by installing Python from python.org or 'brew install tcl-tk').")
    exit(1)

from game import Game

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # hide main window
    player_name = simpledialog.askstring("Player Name", "Enter your name:")
    if not player_name:
        player_name = "Player"
    game = Game(player_name=player_name)
    game.play_game()
    root.mainloop()  # keep window open if needed