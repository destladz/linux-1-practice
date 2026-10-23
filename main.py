
import argparse
import getpass
import socket
import tkinter as tk

from shell import Shell
from gui import TerminalGUI


def main():
    parser = argparse.ArgumentParser(
        description="Эмулятор UNIX-подобной оболочки"
    )
    parser.add_argument("--vfs", default="./vfs_data")
    parser.add_argument("--script")
    args = parser.parse_args()

    username = getpass.getuser()
    hostname = socket.gethostname()

    title = f"Эмулятор - [{username}@{hostname}]"

    shell = Shell(username, hostname)
    shell.script_path = args.script

    try:
        shell.load_vfs(args.vfs)
    except ValueError as error:
        parser.error(str(error))

    root = tk.Tk()
    TerminalGUI(root, shell, title)
    root.mainloop()


if __name__ == "__main__":
    main()
