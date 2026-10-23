
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


def command_exit(args: list[str]) -> bool:
    if args:
        raise ValueError("exit: команда не принимает аргументы")

    return True
