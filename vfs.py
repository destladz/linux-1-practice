
from pathlib import Path


class VirtualFileSystem:
    def __init__(self, source_path: str):
        self.source_path = Path(source_path).expanduser().resolve()

        if not self.source_path.exists():
            raise ValueError(f"Путь VFS не существует: {self.source_path}")

        if not self.source_path.is_dir():
            raise ValueError(f"Путь VFS не является каталогом: {self.source_path}")

        self.root = self._load_directory(self.source_path)

    def _load_directory(self, path: Path) -> dict:
        result = {}

        try:
            for entry in sorted(path.iterdir(), key=lambda item: item.name.lower()):
                if entry.is_symlink():
                    continue

                if entry.is_dir():
                    result[entry.name] = self._load_directory(entry)
                else:
                    result[entry.name] = None
        except OSError as error:
            raise ValueError(f"Не удалось прочитать каталог {path}: {error}") from error

        return result

    def resolve(self, path: str, cwd: str = "/"):
        if path.startswith("/"):
            parts = []
        else:
            parts = [part for part in cwd.split("/") if part]

        for part in path.split("/"):
            if part in ("", "."):
                continue

            if part == "..":
                if parts:
                    parts.pop()
            else:
                parts.append(part)

        node = self.root

        for part in parts:
            if not isinstance(node, dict) or part not in node:
                raise ValueError(f"Путь не существует: /{'/'.join(parts)}")

            node = node[part]

        return "/" + "/".join(parts), node

    def mkdir(self, path: str, cwd: str = "/") -> str:
        normalized = path.rstrip("/")

        if not normalized or normalized in (".", ".."):
            raise ValueError("mkdir: укажите корректное имя каталога")

        parent_path, name = normalized.rsplit("/", 1) if "/" in normalized else (".", normalized)

        if not name or name in (".", ".."):
            raise ValueError("mkdir: укажите корректное имя каталога")

        if normalized.startswith("/") and not parent_path:
            parent_path = "/"
        elif not parent_path:
            parent_path = "."

        _, parent = self.resolve(parent_path, cwd)

        if not isinstance(parent, dict):
            raise ValueError(f"mkdir: родительский путь не является каталогом: {parent_path}")

        if name in parent:
            raise ValueError(f"mkdir: каталог или файл уже существует: {path}")

        parent[name] = {}
        return f"Каталог создан: {path}"
