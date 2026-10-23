def parse_command(command_line: str) -> tuple[str | None, list[str]]:
    parts = command_line.split()

    if not parts:
        return None, []

    return parts[0], parts[1:]
