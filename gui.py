import tkinter as tk
from tkinter import scrolledtext

from shell import Shell


class TerminalGUI:
    def __init__(self, root: tk.Tk, shell: Shell, title: str):
        self.root = root
        self.shell = shell

        self.root.title(title)
        self.root.geometry("850x520")
        self.root.minsize(600, 350)
        self.root.configure(bg="#1e1e1e")

        self.output = scrolledtext.ScrolledText(
            root,
            bg="#1e1e1e",
            fg="#eeeeee",
            insertbackground="#ffffff",
            font=("Consolas", 12),
            wrap=tk.WORD,
            state=tk.DISABLED,
            padx=10,
            pady=10,
        )
        self.output.pack(fill=tk.BOTH, expand=True)

        self.input = tk.Entry(
            root,
            bg="#292929",
            fg="#ffffff",
            insertbackground="#ffffff",
            font=("Consolas", 12),
            relief=tk.FLAT,
        )
        self.input.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.input.bind("<Return>", self.on_enter)
        self.input.focus_set()

        self.write("Эмулятор UNIX-подобной оболочки\n")
        self.write("Введите команду. Для выхода используйте exit.\n\n")
        self.show_prompt()

    def write(self, text: str):
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)

    def show_prompt(self):
        self.write(f"{self.shell.prompt} ")

    def on_enter(self, event=None):
        command_line = self.input.get()
        self.input.delete(0, tk.END)

        self.write(command_line + "\n")

        result, should_exit = self.shell.execute(command_line)

        if result:
            self.write(result + "\n")

        if should_exit:
            self.root.after(300, self.root.destroy)
            self.input.configure(state=tk.DISABLED)
            return "break"

        self.show_prompt()
        return "break"
