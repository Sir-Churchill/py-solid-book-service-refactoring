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


class JsonSerializer:
    def serialize(self, book: Book) -> str:
        return json.dumps(book.content)


class XmlSerializer:
    def serialize(self, book: Book) -> str:
        root = ET.Element("book")
        title = ET.SubElement(root, "title")
        title.text = book.title
        content = ET.SubElement(root, "content")
        content.text = book.content
        return ET.tostring(root, encoding="unicode")


def main(book: Book, commands: list[tuple[str, str]]) -> None | str:
    for cmd, method_type in commands:
        if cmd == "display":
            if method_type == "console":
                ConsolePrint().print(book)
            elif method_type == "reverse":
                ReversePrint().print(book)
            else:
                raise ValueError("Unknown display type")

        elif cmd == "print":
            if method_type == "console":
                print(f"Printing the book: {book.title}...")
                ConsolePrint().print(book)

            elif method_type == "reverse":
                print(f"Printing the book in reverse: {book.title}...")
                ReversePrint().print(book)

            else:
                raise ValueError("Unknown print type")

        elif cmd == "serialize":
            if method_type == "json":
                return json.dumps({
                    "title": book.title,
                    "content": book.content
                })
            elif method_type == "xml":
                return XmlSerializer().serialize(book)
            else:
                raise ValueError("Unknown serialize type")


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(main(sample_book, [("display", "reverse"), ("serialize", "xml")]))
