import json
import os


class Book:
    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = "В наличии"):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def book_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @staticmethod
    def static(data):
        return Book(data["id"], data["title"], data["author"], data["year"], data["status"])


class Library:
    def __init__(self, filename="books.json"):
        self.filename = filename
        self.books = self.load_book()

    def save_book(self):  # сохранение книги
        with open(self.filename, 'w', encoding="utf-8") as f:
            json.dump([book.book_dict() for book in self.books], f, ensure_ascii=False, indent=4)

    def load_book(self):  # чтение файла
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding="utf-8") as f:
                return [Book.static(book) for book in json.load(f)]
        return []

    def add_book(self, title: str, author: str, year: int):  # добавление книги в файл
        book_id = len(self.books) + 1
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.save_book()
        print(f"Книга {title} добавлена в библиотеку")

    def delete_book(self, book_id: int):  # удаление книги
        for book in self.books:
            if book_id == book.id:
                self.books.remove(book)
                self.save_book()
                print(f"Книга с номером {book_id} удалена")
                return
        print(f"Книга с номером {book_id} не найдена")
        return

    def search_book(self, query: str):  # поиск определенной книги
        results = []
        for book in self.books:
            if (query.lower() == book.title.lower() or
                    query.lower() == book.author.lower() or
                    query == str(book.year)):
                results.append(book)
        return results

    def status_book(self, book_id: int, new_status: str):  # изменение статуса
        for book in self.books:
            if book_id == book.id:
                if new_status in ['В наличии', 'Нет в наличии']:
                    book.status == new_status
                    self.save_book()
                    print(f'Статус книги под номером {book_id} изменён на {new_status}')
                    return
                else:
                    print(f"Доступны статусы: 'В наличии', 'Нет в наличии'")
                    return
        print(f"Книга под номером {book_id} не найдена")
        return

    def all_book(self):  # показ всех харнящихся книг
        if not self.books:
            print(f"В библиотеке нет книг")
            return
        else:
            for book in self.books:
                print(f"id: {book.id}, Название: '{book.title}', "
                      f"Автор: '{book.author}', Год: {book.year}, "
                      f"Статус: {book.status}")


def console():
    print("Запуск")
    library = Library()

    while True:
        print("Меню")
        print("1: Добавить книгу")
        print("2: Удалить книгу")
        print("3: Найти книгу")
        print("4: Отобразить все книги")
        print("5: Изменить статус книги")

        choise = input("Выберите действие: ")

        if choise == '1':
            title = input("Введите название книги:")
            author = input("Введите имя автора:")
            year = int(input("Введите год издания"))
            library.add_book(title, author, year)

        elif choise == '2':
            book_id = int(input("Введите номер книги:"))
            library.delete_book(book_id)

        elif choise == '3':
            query = input("Введите название, автора или год для поиска: ")
            results = library.search_book(query)
            if results:
                for book in results:
                    print(
                        f"id: {book.id}, Название: '{book.title}', Автор: '{book.author}',"
                        f" Год: {book.year}, Статус: {book.status}")
            else:
                print("Книги не найдены.")

        elif choise == '4':
            library.all_book()

        elif choise == '5':
            id_book = int(input("Введите номер книги:"))
            status = input("Введите новый статус:")
            library.status_book(id_book, status)


if __name__ == "__main__":
    console()
