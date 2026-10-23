
from parser import parse_command
from commands import command_ls, command_cd, command_exit
from vfs import VirtualFileSystem


class Shell:
    def __init__(self, username: str, hostname: str):
        self.username = username
        self.hostname = hostname
        self.cwd = "/"
        self.vfs_path = "./vfs_data"
        self.script_path = None
        self.vfs = None

        self.commands = {
            "ls": command_ls,
            "cd": command_cd,
        }

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
                should_exit = command_exit(args)
                return "Выход из эмулятора.", should_exit
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

        if command == "ls":
            try:
                return command_ls(args, self.vfs, self.cwd), False
            except ValueError as error:
                return f"Ошибка: {error}", False

        if command == "cd":
            try:
                if len(args) > 1:
                    raise ValueError(
                        "cd: слишком много аргументов (ожидается не более одного)"
                    )

                target = args[0] if args else "/"

                if self.vfs is None:
                    raise ValueError("VFS не загружена")

                new_path, node = self.vfs.resolve(target, self.cwd)

                if not isinstance(node, dict):
                    raise ValueError(f"cd: не является каталогом: {target}")

                self.cwd = new_path
                return "", False
            except ValueError as error:
                return f"Ошибка: {error}", False

        handler = self.commands.get(command)

        if handler is None:
            return f"Ошибка: неизвестная команда '{command}'", False

        try:
            result = handler(args)
            return result, False
        except ValueError as error:
            return f"Ошибка: {error}", False
