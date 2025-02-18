"""
This module implements a basic UI using Tkinter for interacting with the poker game.
It creates a window for displaying game information and capturing player actions.
"""

import tkinter as tk

class GameUI:
    def __init__(self, root):
        """
        Initialize the game UI by creating a toplevel window.
        
        Args:
            root (tk.Tk): The main Tkinter root window.
        """
        self.root = root
        # Create a separate window for the game UI.
        self.top = tk.Toplevel(root)
        self.top.title("Poker Game")
        self.info_label = tk.Label(self.top, text="", font=("Helvetica", 14))
        self.info_label.pack(pady=10)
        self.action_var = tk.StringVar()
        self.action_frame = tk.Frame(self.top)
        self.action_frame.pack(pady=10)
    
    def update_info(self, info_text):
        """
        Update the displayed game information.
        
        Args:
            info_text (str): Text to be displayed.
        """
        self.info_label.config(text=info_text)
        self.top.update_idletasks()
    
    def prompt_action(self, prompt, options):
        """
        Prompt the user to choose an action.
        
        Args:
            prompt (str): The prompt message to display.
            options (List[str]): List of available action options.
        
        Returns:
            str: The action selected by the user.
        """
        # Clear any previous buttons.
        for widget in self.action_frame.winfo_children():
            widget.destroy()
        self.update_info(prompt)
        self.action_var.set("")  # Reset variable.
        for opt in options:
            btn = tk.Button(
                self.action_frame, 
                text=opt.capitalize(), 
                command=lambda o=opt: self.action_var.set(o)
            )
            btn.pack(side=tk.LEFT, padx=5)
        self.top.wait_variable(self.action_var)
        return self.action_var.get()
    
    def prompt_amount(self, prompt, min_value, max_value):
        """
        Prompt the user to enter a numeric amount.
        
        Args:
            prompt (str): The prompt message.
            min_value (int): Minimum acceptable value.
            max_value (int): Maximum acceptable value.
        
        Returns:
            int or None: The entered amount if valid, otherwise None.
        """
        popup = tk.Toplevel(self.top)
        popup.title("Enter Amount")
        tk.Label(popup, text=prompt).pack(pady=5)
        entry = tk.Entry(popup)
        entry.pack(pady=5)
        amount_var = tk.StringVar()
        def submit():
            amount_var.set(entry.get())
            popup.destroy()
        tk.Button(popup, text="OK", command=submit).pack(pady=5)
        popup.wait_window()
        try:
            amount = int(amount_var.get())
            if min_value <= amount <= max_value:
                return amount
        except ValueError:
            pass
        return None
