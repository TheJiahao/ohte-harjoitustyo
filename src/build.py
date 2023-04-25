from entities import database


def build() -> None:
    database.initialize()

if __name__ == "__main__":
    build()
