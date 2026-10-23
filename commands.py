def command_ls(args: list[str]) -> str:
    arguments = " ".join(args)
    return f"ls: аргументы: {arguments}"


def command_cd(args: list[str]) -> str:
    if len(args) > 1:
        raise ValueError(
            "cd: слишком много аргументов (ожидается не более одного)"
        )

    arguments = " ".join(args)
    return f"cd: аргументы: {arguments}"


def command_exit(args: list[str]) -> bool:
    if args:
        raise ValueError("exit: команда не принимает аргументы")

    return True
