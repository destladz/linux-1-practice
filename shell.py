from parser import parse_command
from commands import command_ls, command_cd, command_exit


class Shell:
    def __init__(self, username: str, hostname: str):
        self.username = username
        self.hostname = hostname
        self.cwd = "/"

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

        handler = self.commands.get(command)

        if handler is None:
            return f"Ошибка: неизвестная команда '{command}'", False

        try:
            result = handler(args)
            return result, False
        except ValueError as error:
            return f"Ошибка: {error}", False
