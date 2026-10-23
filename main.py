import getpass
import socket
import tkinter as tk

from shell import Shell
from gui import TerminalGUI


def main():
    username = getpass.getuser()
    hostname = socket.gethostname()

    title = f"Эмулятор - [{username}@{hostname}]"

    shell = Shell(username, hostname)

    root = tk.Tk()
    TerminalGUI(root, shell, title)

    root.mainloop()


if __name__ == "__main__":
    main()
