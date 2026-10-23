import calendar
from datetime import datetime


def command_ls(args: list[str], vfs=None, cwd: str = "/") -> str:
    if len(args) > 1:
        raise ValueError("ls: слишком много аргументов")

    if vfs is None:
        return f"ls: аргументы: {' '.join(args)}"

    path = args[0] if args else cwd
    _, node = vfs.resolve(path, cwd)

    if not isinstance(node, dict):
        raise ValueError(f"ls: не является каталогом: {path}")

    entries = [
        name + ("/" if isinstance(value, dict) else "")
        for name, value in node.items()
    ]

    return "\n".join(entries) if entries else "Каталог пуст"


def command_cd(args: list[str]) -> str:
    if len(args) > 1:
        raise ValueError(
            "cd: слишком много аргументов (ожидается не более одного)"
        )

    return args[0] if args else "/"


def command_cal(args: list[str]) -> str:
    if args:
        raise ValueError("cal: команда не принимает аргументы")

    now = datetime.now()
    return calendar.TextCalendar().formatmonth(now.year, now.month)


def command_whoami(args: list[str], username: str) -> str:
    if args:
        raise ValueError("whoami: команда не принимает аргументы")

    return username


def command_exit(args: list[str]) -> bool:
    if args:
        raise ValueError("exit: команда не принимает аргументы")

    return True


def command_mkdir(args: list[str], vfs, cwd: str = "/") -> str:
    if len(args) != 1:
        raise ValueError("mkdir: укажите имя одного каталога")

    if vfs is None:
        raise ValueError("mkdir: VFS не загружена")

    return vfs.mkdir(args[0], cwd)