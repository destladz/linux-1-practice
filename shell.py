
from parser import parse_command
from commands import command_ls, command_cd, command_exit


class Shell:
    def __init__(self, username: str, hostname: str):
        self.username = username
        self.hostname = hostname
        self.cwd = "/"
        self.vfs_path = "./vfs_data"
        self.script_path = None

        self.commands = {
            "ls": command_ls,
            "cd": command_cd,
        }

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

        handler = self.commands.get(command)

        if handler is None:
            return f"Ошибка: неизвестная команда '{command}'", False

        try:
            result = handler(args)
            return result, False
        except ValueError as error:
            return f"Ошибка: {error}", False
