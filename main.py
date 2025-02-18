"""
Main entry point for the Poker Game application.
Initializes the UI and starts the game loop.
"""

try:
    import tkinter as tk
    from tkinter import simpledialog
except ModuleNotFoundError:
    print("Error: tkinter module not found. Install Tcl/Tk support (e.g., by installing Python from python.org or 'brew install tcl-tk').")
    exit(1)

from game import Game

if __name__ == "__main__":
    # Initialize Tkinter and show a dialog for player's name.
    root = tk.Tk()
    root.withdraw()  # Hide the main window.
    player_name = simpledialog.askstring("Player Name", "Enter your name:")
    if not player_name:
        player_name = "Player"
    # Instantiate and start the game.
    game = Game(player_name=player_name)
    game.play_game()
    root.mainloop()  # Keeps the Tkinter window open