import json
import xml.etree.ElementTree as ET


class Book:
    def __init__(self, title: str, content: str) -> None:
        self.title = title
        self.content = content


class PrintStrategy:
    def print(self, book: Book) -> None:
        raise NotImplementedError


class ConsolePrint(PrintStrategy):
    def print(self, book: Book) -> None:
        print(book.content)


class ReversePrint(PrintStrategy):
    def print(self, book: Book) -> None:
        print(book.content[::-1])


class Serializer:
    def serialize(self, book: Book) -> str:
        raise NotImplementedError


class JsonSerializer(Serializer):
    def serialize(self, book: Book) -> str:
        return json.dumps({
            "title": book.title,
            "content": book.content
        })


class XmlSerializer(Serializer):
    def serialize(self, book: Book) -> str:
        root = ET.Element("book")

        title = ET.SubElement(root, "title")
        title.text = book.title

        content = ET.SubElement(root, "content")
        content.text = book.content

        return ET.tostring(root, encoding="unicode")


class CommandHandler:

    display_strategies = {
        "console": ConsolePrint(),
        "reverse": ReversePrint(),
    }

    print_strategies = {
        "console": ConsolePrint(),
        "reverse": ReversePrint(),
    }

    serializers = {
        "json": JsonSerializer(),
        "xml": XmlSerializer(),
    }

    def execute(self, book: Book, cmd: str, method: str) -> str | None:
        if cmd == "display":
            strategy = self.display_strategies[method]
            strategy.print(book)

        elif cmd == "print":
            strategy = self.print_strategies[method]
            print(book.title)
            strategy.print(book)

        elif cmd == "serialize":
            serializer = self.serializers[method]
            return serializer.serialize(book)

        else:
            raise ValueError(f"Unknown command: {cmd}")


def main(book: Book, commands: list[tuple[str, str]]) -> str | None:
    handler = CommandHandler()

    for cmd, method in commands:
        result = handler.execute(book, cmd, method)
        if result is not None:
            return result
