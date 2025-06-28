from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QMessageBox, QHBoxLayout
)
import sys

# ------------------------ Backend Code ------------------------

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_lent = False

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"


class Ebook(Book):
    def __init__(self, title, author, isbn, download_size):
        super().__init__(title, author, isbn)
        self.download_size = download_size

    def __str__(self):
        return f"{super().__str__()} - {self.download_size}MB"


class BookNotAvailableError(Exception):
    pass


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def lend_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn and not book.is_lent:
                book.is_lent = True
                return book
        raise BookNotAvailableError("This book is not available.")

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                book.is_lent = False


class DigitalLibrary(Library):
    def __init__(self):
        super().__init__()
        self.ebooks = []

    def add_ebook(self, title, author, isbn, download_size):
        ebook = Ebook(title, author, isbn, download_size)
        self.ebooks.append(ebook)
        self.books.append(ebook)

# ------------------------ PyQt GUI Code ------------------------

class LibraryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.library = DigitalLibrary()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Book Title")
        layout.addWidget(QLabel("Title:"))
        layout.addWidget(self.title_input)

        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Author")
        layout.addWidget(QLabel("Author:"))
        layout.addWidget(self.author_input)

        self.isbn_input = QLineEdit()
        self.isbn_input.setPlaceholderText("ISBN")
        layout.addWidget(QLabel("ISBN:"))
        layout.addWidget(self.isbn_input)

        self.ebook_checkbox = QCheckBox("Is this an eBook?")
        self.ebook_checkbox.stateChanged.connect(self.toggle_ebook_input)
        layout.addWidget(self.ebook_checkbox)

        self.download_size_input = QLineEdit()
        self.download_size_input.setPlaceholderText("Download Size in MB")
        self.download_size_input.setDisabled(True)
        layout.addWidget(QLabel("Download Size (MB):"))
        layout.addWidget(self.download_size_input)

        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("Add Book")
        self.add_btn.clicked.connect(self.add_book)
        btn_layout.addWidget(self.add_btn)

        self.quit_btn = QPushButton("Exit")
        self.quit_btn.clicked.connect(self.close)
        btn_layout.addWidget(self.quit_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def toggle_ebook_input(self):
        if self.ebook_checkbox.isChecked():
            self.download_size_input.setDisabled(False)
        else:
            self.download_size_input.setDisabled(True)
            self.download_size_input.clear()

    def add_book(self):
        title = self.title_input.text()
        author = self.author_input.text()
        isbn = self.isbn_input.text()
        is_ebook = self.ebook_checkbox.isChecked()

        if not title or not author or not isbn:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
            return

        if is_ebook:
            try:
                size = float(self.download_size_input.text())
                self.library.add_ebook(title, author, isbn, size)
                QMessageBox.information(self, "Success", "eBook added successfully!")
            except ValueError:
                QMessageBox.warning(self, "Input Error", "Download size must be a number.")
        else:
            self.library.add_book(Book(title, author, isbn))
            QMessageBox.information(self, "Success", "Book added successfully!")

        self.title_input.clear()
        self.author_input.clear()
        self.isbn_input.clear()
        self.download_size_input.clear()
        self.ebook_checkbox.setChecked(False)

# ------------------------ Run Application ------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())
