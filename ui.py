"""
This module implements a basic UI using Tkinter for interacting with the poker game.
It creates a window for displaying game information and capturing player actions.
"""

import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

class GameUI:
    def __init__(self, root):
        """
        Initialize the game UI by creating a toplevel window.
        
        Args:
            root (tk.Tk): The main Tkinter root window.
        """
        self.root = root
        self.top = tk.Toplevel(root)
        self.top.title("Texas Hold'em Poker")
        self.style = ttk.Style(self.top)
        self.style.theme_use("clam")
        
        # Main container using grid for layout.
        self.main_frame = ttk.Frame(self.top, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="NSEW")
        self.top.columnconfigure(0, weight=1)
        self.top.rowconfigure(0, weight=1)
        
        # Info frame for game status and chip counts.
        self.info_frame = ttk.Frame(self.main_frame, padding="5", relief="ridge")
        self.info_frame.grid(row=0, column=0, columnspan=2, sticky="EW", pady=5)
        self.info_label = ttk.Label(self.info_frame, text="", font=("Helvetica", 14))
        self.info_label.grid(row=0, column=0, sticky="W")
        
        # Add a Help button for AI action explanations.
        help_btn = ttk.Button(self.info_frame, text="Help",
                              command=lambda: self.show_tooltip())
        help_btn.grid(row=0, column=1, padx=10, sticky="e")
        
        # Table frame for community cards.
        self.table_frame = ttk.Frame(self.main_frame, padding="5", relief="groove")
        self.table_frame.grid(row=1, column=0, columnspan=2, sticky="NSEW", pady=5)
        ttk.Label(self.table_frame, text="Community Cards:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky="W")
        self.community_canvas = tk.Canvas(self.table_frame, width=500, height=150, bg="#35654d")
        self.community_canvas.grid(row=1, column=0, padx=5, pady=5)
        
        # AI frame for AI hands.
        self.ai_frame = ttk.Frame(self.main_frame, padding="5", relief="groove")
        self.ai_frame.grid(row=2, column=0, sticky="NSEW", pady=5)
        ttk.Label(self.ai_frame, text="AI Hands:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky="W")
        self.ai_canvas = tk.Canvas(self.ai_frame, width=500, height=150, bg="#2e2e2e")
        self.ai_canvas.grid(row=1, column=0, padx=5, pady=5)
        
        # Player frame for human player's cards.
        self.player_frame = ttk.Frame(self.main_frame, padding="5", relief="groove")
        self.player_frame.grid(row=3, column=0, sticky="NSEW", pady=5)
        ttk.Label(self.player_frame, text="Your Hand:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky="W")
        self.player_canvas = tk.Canvas(self.player_frame, width=500, height=120, bg="#1b1b1b")
        self.player_canvas.grid(row=1, column=0, padx=5, pady=5)
        
        # Action frame for buttons and betting input.
        self.action_frame = ttk.Frame(self.main_frame, padding="5")
        self.action_frame.grid(row=4, column=0, sticky="EW", pady=5)
        self.action_var = tk.StringVar()
        
        self.input_frame = ttk.Frame(self.main_frame, padding="5")
        self.input_frame.grid(row=5, column=0, sticky="EW", pady=5)
        
        # Remove duplicate info/status: keep only one status_frame.
        # Add a log frame to display AI actions and game activity.
        self.log_frame = ttk.Frame(self.main_frame, padding="5", relief="groove")
        self.log_frame.grid(row=6, column=0, sticky="NSEW", pady=5)
        ttk.Label(self.log_frame, text="Game Log:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky="W")
        self.log_text = tk.Text(self.log_frame, height=8, state="disabled", wrap="word", font=("Helvetica", 10))
        self.log_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        # Add a vertical scrollbar for the log.
        self.log_scrollbar = ttk.Scrollbar(self.log_frame, orient="vertical", command=self.log_text.yview)
        self.log_scrollbar.grid(row=1, column=1, sticky="ns")
        self.log_text.configure(yscrollcommand=self.log_scrollbar.set)
        # Remove the status_frame that was duplicating info.
        # Adjust grid rows: now total rows=7.
        for i in range(7):
            self.main_frame.rowconfigure(i, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

    # Constants for high‐resolution images.
    IMAGE_SIZE = (120, 180)  # Use higher-res images (width, height)

    def load_card_image(self, card):
        base_path = "/Users/ahmedikram/GitHub Repos/Texas-Holdem-Poker-Game/assets/cards"
        filename = f"{card.rank.name.lower()}_of_{card.suit.name.lower()}.png"
        full_path = os.path.join(base_path, filename)
        try:
            image = Image.open(full_path).resize(self.IMAGE_SIZE)  # Use high-res images
            return ImageTk.PhotoImage(image)
        except Exception:
            return None

    def load_card_back(self):
        # Attempt to load a generic card back image.
        base_path = "/Users/ahmedikram/GitHub Repos/Texas-Holdem-Poker-Game/assets/cards"
        full_path = os.path.join(base_path, "card_back.png")
        try:
            image = Image.open(full_path).resize(self.IMAGE_SIZE)  # Use high-res card back
            return ImageTk.PhotoImage(image)
        except Exception:
            return None

    def _display_cards(self, canvas, cards, x_offset=10, y_offset=None):
        canvas.delete("all")
        canvas.images = []  # Clear previous images.
        width, height = self.IMAGE_SIZE
        if y_offset is None:
            y_offset = (int(canvas["height"]) - height) // 2
        x = x_offset
        for card in cards:
            img = self.load_card_image(card)
            if img:
                canvas.create_image(x, y_offset, anchor="nw", image=img)
                canvas.images.append(img)
            else:
                # Draw a white rectangle card with black border and show card text.
                canvas.create_rectangle(x, y_offset, x + width, y_offset + height, fill="white", outline="black")
                canvas.create_text(x + width/2, y_offset + height/2, text=str(card), font=("Helvetica", 14), fill="black")
            x += 70
        canvas.update_idletasks()

    def display_community_cards(self, cards):
        # Use a fixed y_offset (e.g., 30) for community cards.
        self._display_cards(self.community_canvas, cards, x_offset=10, y_offset=30)

    def display_player_hand(self, cards):
        self._display_cards(self.player_canvas, cards)

    def display_ai_hands(self, ai_cards, reveal_all=False):
        """
        ai_cards: list of tuples (player_name, [Card], folded:bool)
        Arranges AI hands horizontally.
        If reveal_all is False:
          - Active AI (folded==False): show card back images.
          - Folded AI (folded==True): reveal actual cards.
        If reveal_all is True, reveal actual cards for all AI.
        """
        self.ai_canvas.delete("all")
        self.ai_canvas.images = []
        num_ai = len(ai_cards)
        canvas_width = int(self.ai_canvas["width"])
        spacing = canvas_width // num_ai
        for idx, (name, cards, folded) in enumerate(ai_cards):
            base_x = idx * spacing + 10
            # Display AI name.
            self.ai_canvas.create_text(base_x, 10, anchor="nw", text=name, font=("Helvetica", 10, "bold"), fill="white")
            x = base_x
            y = 30
            for card in cards:
                if reveal_all or folded:
                    # Reveal card face.
                    img = self.load_card_image(card)
                    if img:
                        self.ai_canvas.create_image(x, y, anchor="nw", image=img)
                        self.ai_canvas.images.append(img)
                    else:
                        self.ai_canvas.create_text(x+30, y+45, text=str(card), font=("Helvetica", 12), fill="white")
                else:
                    # Active AI: show card back.
                    back_img = self.load_card_back()
                    if back_img:
                        self.ai_canvas.create_image(x, y, anchor="nw", image=back_img)
                        self.ai_canvas.images.append(back_img)
                    else:
                        self.ai_canvas.create_text(x+30, y+45, text="Back", font=("Helvetica", 12), fill="white")
                x += 70
        self.ai_canvas.update_idletasks()

    def update_info(self, info_text):
        """
        Update the status shown at the top of the UI. This panel is now used solely 
        for brief instructions. Detailed AI/game events should be appended to the log.
        """
        self.info_label.config(text=info_text, foreground="black")
        self.info_label.update_idletasks()

    def append_log(self, message):
        """
        Append a new message with timestamp to the game log.
        """
        from datetime import datetime
        timestamp = datetime.now().strftime("[%H:%M:%S] ")
        self.log_text.config(state="normal")
        self.log_text.insert("end", timestamp + message + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")
    
    def prompt_action(self, prompt, options):
        # Clear previous action widgets.
        for widget in self.action_frame.winfo_children():
            widget.destroy()
        # Update the status label with the prompt.
        self.update_info(prompt)
        self.action_var.set("")
        col = 0
        for opt in options:
            # Create buttons with more descriptive text.
            btn = ttk.Button(self.action_frame, text=opt.capitalize(), command=lambda o=opt: self.action_var.set(o))
            btn.grid(row=0, column=col, padx=10, pady=10)
            self.blink_widget(btn)
            col += 1
        self.top.wait_variable(self.action_var)
        return self.action_var.get()
    
    def prompt_amount(self, prompt, min_value, max_value):
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        prompt_label = ttk.Label(self.input_frame, text=prompt)
        prompt_label.grid(row=0, column=0, padx=5, pady=5)
        entry = ttk.Entry(self.input_frame)
        entry.grid(row=0, column=1, padx=5, pady=5)
        amount_var = tk.StringVar()
        def submit():
            amount_var.set(entry.get())
        ok_btn = ttk.Button(self.input_frame, text="OK", command=submit)
        ok_btn.grid(row=0, column=2, padx=5, pady=5)
        self.top.wait_variable(amount_var)
        try:
            amount = int(amount_var.get())
            if min_value <= amount <= max_value:
                return amount
        except ValueError:
            pass
        return None

    def blink_widget(self, widget, count=3):
        def _blink(count):
            if count <= 0:
                widget.config(style="")
                return
            current = widget.cget("style")
            widget.config(style="Blink.TButton" if current == "" else "")
            widget.after(300, lambda: _blink(count-1))
        _blink(count)

    def animate_deal(self, canvas, image_obj, start_x, start_y, end_x, end_y, steps=20, delay=50):
        """
        Animate a card image moving on the given canvas.
        Moves the image from (start_x, start_y) to (end_x, end_y) in a number of steps.
        """
        dx = (end_x - start_x) / steps
        dy = (end_y - start_y) / steps
        # Create the image at the starting position.
        item = canvas.create_image(start_x, start_y, anchor="nw", image=image_obj)
        def step(step_count):
            if step_count < steps:
                canvas.move(item, dx, dy)
                canvas.after(delay, lambda: step(step_count + 1))
            else:
                # Ensure final position is exactly at (end_x, end_y)
                canvas.coords(item, end_x, end_y)
        step(0)
        return item

    def show_notification(self, message, duration=2000):
        """
        Display a temporary overlay notification in the GUI.
        """
        notif = tk.Label(self.top, text=message, font=("Helvetica", 16, "bold"),
                         bg="yellow", fg="black")
        notif.place(relx=0.5, rely=0.1, anchor="n")
        self.top.after(duration, notif.destroy)

    def show_tooltip(self):
        """
        Show a help dialog explaining AI actions.
        """
        help_text = (
            "AI Actions Help:\n\n"
            "- 'Calls': The AI matches the current bet.\n"
            "- 'Raises': The AI increases the bet if its hand is strong (combined rank above threshold).\n"
            "- 'Folds': The AI opts out of the hand if the call is too high relative to its strength.\n\n"
            "These decisions are based on a simple rule-based evaluation of the AI's hole cards."
        )
        tk.messagebox.showinfo("AI Actions Explanation", help_text)
