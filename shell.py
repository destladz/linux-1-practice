
from parser import parse_command
from commands import (
    command_ls,
    command_cd,
    command_cal,
    command_whoami,
    command_exit,
)
from vfs import VirtualFileSystem


class Shell:
    def __init__(self, username: str, hostname: str):
        self.username = username
        self.hostname = hostname
        self.cwd = "/"
        self.vfs_path = "./vfs_data"
        self.script_path = None
        self.vfs = None

    def load_vfs(self, path: str):
        self.vfs = VirtualFileSystem(path)
        self.vfs_path = path
        self.cwd = "/"

    @property
    def prompt(self) -> str:
        return f"{self.username}@{self.hostname}:{self.cwd}$"

    def execute(self, command_line: str) -> tuple[str, bool]:
        command, args = parse_command(command_line)

        if command is None:
            return "", False

        if command == "exit":
            try:
                return "Выход из эмулятора.", command_exit(args)
            except ValueError as error:
                return f"Ошибка: {error}", False

        if command == "conf-dump":
            if args:
                return "Ошибка: команда conf-dump не принимает аргументы", False

            return (
                f"vfs={self.vfs_path}\n"
                f"script={self.script_path if self.script_path else ''}",
                False,
            )

        try:
            if command == "ls":
                return command_ls(args, self.vfs, self.cwd), False

            if command == "cd":
                target = command_cd(args)

                if self.vfs is None:
                    raise ValueError("VFS не загружена")

                new_path, node = self.vfs.resolve(target, self.cwd)

                if not isinstance(node, dict):
                    raise ValueError(f"cd: не является каталогом: {target}")

                self.cwd = new_path
                return "", False

            if command == "cal":
                return command_cal(args), False

            if command == "whoami":
                return command_whoami(args, self.username), False

            return f"Ошибка: неизвестная команда '{command}'", False

        except ValueError as error:
            return f"Ошибка: {error}", False
