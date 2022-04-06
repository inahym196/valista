def load_text(filepath: str) -> list[str]:
    with open(filepath, encoding='UTF-8') as f:
        return f.readlines()
