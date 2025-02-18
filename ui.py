import tkinter as tk

class GameUI:
    def __init__(self, root):
        self.root = root
        # Create a main window panel for game info and actions
        self.top = tk.Toplevel(root)
        self.top.title("Poker Game")
        self.info_label = tk.Label(self.top, text="", font=("Helvetica", 14))
        self.info_label.pack(pady=10)
        self.action_var = tk.StringVar()
        self.action_frame = tk.Frame(self.top)
        self.action_frame.pack(pady=10)
    
    def update_info(self, info_text):
        self.info_label.config(text=info_text)
        self.top.update_idletasks()
    
    def prompt_action(self, prompt, options):
        # Clear previous buttons
        for widget in self.action_frame.winfo_children():
            widget.destroy()
        self.update_info(prompt)
        self.action_var.set("")
        for opt in options:
            btn = tk.Button(self.action_frame, text=opt.capitalize(), command=lambda o=opt: self.action_var.set(o))
            btn.pack(side=tk.LEFT, padx=5)
        self.top.wait_variable(self.action_var)
        return self.action_var.get()
    
    def prompt_amount(self, prompt, min_value, max_value):
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
