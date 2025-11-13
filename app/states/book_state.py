import reflex as rx
from typing import TypedDict, Literal
import datetime
from app.states.auth_state import AuthState, User
from app.data_generator import generate_books

Category = Literal[
    "Fiction",
    "Dystopian",
    "Science Fiction",
    "Fantasy",
    "Mystery",
    "Non-Fiction",
    "Science",
    "History",
    "Biography",
    "Technology",
    "Art",
    "Philosophy",
    "Romance",
    "Thriller",
    "Self-Help",
    "Business",
    "Children",
    "Poetry",
    "Drama",
    "Travel",
]


class Book(TypedDict):
    id: int
    title: str
    author: str
    category: Category
    cover_image_url: str
    is_available: bool
    description: str
    isbn: str
    publication_year: int


class BorrowedBook(TypedDict):
    book_id: int
    user_username: str
    due_date: str


class BorrowedBookWithDetails(TypedDict):
    book: Book
    due_date: str


class Reservation(TypedDict):
    book_id: int
    user_username: str
    timestamp: str


def get_initial_books() -> list[Book]:
    all_books = generate_books(10000)
    borrowed_ids = [3, 5, 9, 12, 15, 21, 28, 34, 42, 50, 61, 75, 88, 99, 101]
    for book in all_books:
        if book["id"] in borrowed_ids:
            book["is_available"] = False
    return all_books


def get_initial_borrowed_books() -> list[BorrowedBook]:
    return [
        {
            "book_id": 3,
            "user_username": "student",
            "due_date": (datetime.date.today() + datetime.timedelta(days=10)).strftime(
                "%Y-%m-%d"
            ),
        },
        {
            "book_id": 5,
            "user_username": "teacher",
            "due_date": (datetime.date.today() + datetime.timedelta(days=25)).strftime(
                "%Y-%m-%d"
            ),
        },
        {
            "book_id": 9,
            "user_username": "student",
            "due_date": (datetime.date.today() - datetime.timedelta(days=2)).strftime(
                "%Y-%m-%d"
            ),
        },
    ]


class BookState(rx.State):
    _all_books: list[Book] = get_initial_books()
    books: list[Book] = _all_books
    borrowed_books: list[BorrowedBook] = get_initial_borrowed_books()
    reservations: list[Reservation] = []
    show_book_modal: bool = False
    show_edit_book_modal: bool = False
    show_add_book_modal: bool = False
    selected_book: Book | None = None
    search_query: str = ""
    category_filter: str = "All"
    availability_filter: str = "all"
    current_page: int = 1
    books_per_page: int = 20

    @rx.var
    def total_books(self) -> int:
        return len(self.books)

    @rx.var
    def total_borrowed_books(self) -> int:
        return len([book for book in self.books if not book["is_available"]])

    @rx.var
    def available_books_count(self) -> int:
        return self.total_books - self.total_borrowed_books

    @rx.var
    def overdue_books_count(self) -> int:
        today = datetime.date.today()
        count = 0
        for book in self.borrowed_books:
            due_date = datetime.datetime.strptime(book["due_date"], "%Y-%m-%d").date()
            if due_date < today:
                count += 1
        return count

    @rx.var
    def all_categories(self) -> list[str]:
        return ["All"] + sorted(list(set((b["category"] for b in self._all_books))))

    @rx.var
    def all_book_categories(self) -> list[str]:
        return sorted(list(set((b["category"] for b in self._all_books))))

    @rx.var
    def filtered_books(self) -> list[Book]:
        books = self.books
        if self.search_query:
            query = self.search_query.lower()
            books = [
                b
                for b in books
                if query in b["title"].lower() or query in b["author"].lower()
            ]
        if self.category_filter != "All":
            books = [b for b in books if b["category"] == self.category_filter]
        if self.availability_filter != "all":
            is_available = self.availability_filter == "available"
            books = [b for b in books if b["is_available"] == is_available]
        return books

    @rx.var
    def total_pages(self) -> int:
        return -(-len(self.filtered_books) // self.books_per_page)

    @rx.var
    def paginated_books(self) -> list[Book]:
        start = (self.current_page - 1) * self.books_per_page
        end = start + self.books_per_page
        return self.filtered_books[start:end]

    @rx.event
    def go_to_page(self, page_num: int):
        self.current_page = page_num

    @rx.event
    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1

    @rx.event
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1

    @rx.var
    def books_due_soon_count(self) -> int:
        count = 0
        today = datetime.date.today()
        for b in self.borrowed_books:
            due = datetime.datetime.strptime(b["due_date"], "%Y-%m-%d").date()
            if today < due <= today + datetime.timedelta(days=3):
                count += 1
        return count

    @rx.var
    async def current_user_borrowed_books(self) -> list[BorrowedBook]:
        auth_state = await self.get_state(AuthState)
        if not auth_state or not auth_state.logged_in_user:
            return []
        username = auth_state.logged_in_user["username"]
        return [b for b in self.borrowed_books if b["user_username"] == username]

    def _get_book_by_id(self, book_id: int) -> Book | None:
        for book in self.books:
            if book["id"] == book_id:
                return book
        return None

    @rx.var
    async def current_user_borrowed_books_with_details(
        self,
    ) -> list[BorrowedBookWithDetails]:
        borrowed = await self.current_user_borrowed_books
        books_with_details = []
        for b in borrowed:
            book_details = self._get_book_by_id(b["book_id"])
            if book_details:
                books_with_details.append(
                    BorrowedBookWithDetails(book=book_details, due_date=b["due_date"])
                )
        return books_with_details

    @rx.var
    def get_book_reservations(self) -> list[Reservation]:
        if not self.selected_book:
            return []
        return [
            r for r in self.reservations if r["book_id"] == self.selected_book["id"]
        ]

    @rx.var
    def user_borrowed_counts(self) -> dict[str, int]:
        counts = {}
        for user in self.borrowed_books:
            counts[user["user_username"]] = counts.get(user["user_username"], 0) + 1
        return counts

    @rx.event
    async def on_dashboard_load(self):
        auth = await self.get_state(AuthState)
        if not auth.is_logged_in:
            yield rx.redirect("/")
            return
        for b in await self.current_user_borrowed_books:
            due = datetime.datetime.strptime(b["due_date"], "%Y-%m-%d").date()
            if due < datetime.date.today():
                book = self._get_book_by_id(b["book_id"])
                if book:
                    yield rx.toast.warning(
                        f"'{book['title']}' is overdue!", duration=5000
                    )

    @rx.event
    async def borrow_book(self, book_id: int):
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_logged_in:
            return rx.toast.error("You must be logged in to borrow a book.")
        user: User = auth_state.logged_in_user
        book_to_borrow = self._get_book_by_id(book_id)
        if book_to_borrow and book_to_borrow["is_available"]:
            book_to_borrow["is_available"] = False
            days = 30 if user["role"] == "Teacher" else 14
            due_date = datetime.date.today() + datetime.timedelta(days=days)
            new_borrowed_book: BorrowedBook = {
                "book_id": book_id,
                "user_username": user["username"],
                "due_date": due_date.strftime("%Y-%m-%d"),
            }
            self.borrowed_books.append(new_borrowed_book)
            self._update_book_in_list(book_to_borrow)
            return rx.toast.success(
                f"Successfully borrowed '{book_to_borrow['title']}'!"
            )
        return rx.toast.error("Book is not available for borrowing.")

    @rx.event
    def return_book(self, book_id: int):
        book_to_return = self._get_book_by_id(book_id)
        if book_to_return:
            book_to_return["is_available"] = True
            self._update_book_in_list(book_to_return)
        self.borrowed_books = [
            b for b in self.borrowed_books if b["book_id"] != book_id
        ]
        if book_to_return:
            yield rx.toast.info(f"You have returned '{book_to_return['title']}'.")

    def _update_book_in_list(self, updated_book: Book):
        self.books = [
            b if b["id"] != updated_book["id"] else updated_book for b in self.books
        ]
        self._all_books = [
            b if b["id"] != updated_book["id"] else updated_book
            for b in self._all_books
        ]

    @rx.event
    async def reserve_book(self, book_id: int):
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_logged_in:
            return rx.toast.error("You must be logged in to reserve a book.")
        user: User = auth_state.logged_in_user
        book = self._get_book_by_id(book_id)
        if not book or book["is_available"]:
            return rx.toast.error("Book is available and cannot be reserved.")
        if any(
            (
                r
                for r in self.reservations
                if r["book_id"] == book_id and r["user_username"] == user["username"]
            )
        ):
            return rx.toast.info("You have already reserved this book.")
        new_reservation = Reservation(
            book_id=book_id,
            user_username=user["username"],
            timestamp=datetime.datetime.now().isoformat(),
        )
        if user["role"] == "Teacher":
            insert_pos = 0
            for i, res in enumerate(self.reservations):
                res_user = await auth_state.get_user_by_username(res["user_username"])
                if (
                    res["book_id"] == book_id
                    and res_user
                    and (res_user["role"] != "Teacher")
                ):
                    insert_pos = i
                    break
                insert_pos = i + 1
            self.reservations.insert(insert_pos, new_reservation)
        else:
            self.reservations.append(new_reservation)
        return rx.toast.success(f"You have reserved '{book['title']}'.")

    @rx.event
    def open_book_modal(self, book: Book):
        self.selected_book = book
        self.show_book_modal = True

    @rx.event
    def close_book_modal(self, _=None):
        self.show_book_modal = False
        self.selected_book = None

    @rx.event
    def open_add_book_modal(self):
        self.show_add_book_modal = True

    @rx.event
    def close_add_book_modal(self, _=None):
        self.show_add_book_modal = False

    @rx.event
    def open_edit_book_modal(self, book: Book):
        self.show_book_modal = False
        self.selected_book = book
        self.show_edit_book_modal = True

    @rx.event
    def close_edit_book_modal(self, _=None):
        self.show_edit_book_modal = False
        self.selected_book = None

    @rx.event
    def add_book(self, form_data: dict):
        new_id = max((b["id"] for b in self._all_books), default=0) + 1
        new_book: Book = {
            "id": new_id,
            "title": form_data["title"],
            "author": form_data["author"],
            "category": form_data["category"],
            "cover_image_url": form_data.get("cover_image_url") or "/placeholder.svg",
            "description": form_data["description"],
            "is_available": True,
            "isbn": form_data.get("isbn", ""),
            "publication_year": int(form_data.get("publication_year", 2024)),
        }
        self._all_books.insert(0, new_book)
        self.books = self._all_books
        self.show_add_book_modal = False
        return rx.toast.success(f"Added '{new_book['title']}'.")

    @rx.event
    def update_book(self, form_data: dict):
        if not self.selected_book:
            return rx.toast.error("No book selected for update.")
        updated_book: Book = self.selected_book.copy()
        updated_book["title"] = form_data["title"]
        updated_book["author"] = form_data["author"]
        updated_book["category"] = form_data["category"]
        updated_book["cover_image_url"] = (
            form_data.get("cover_image_url") or self.selected_book["cover_image_url"]
        )
        updated_book["description"] = form_data["description"]
        updated_book["isbn"] = form_data.get("isbn") or self.selected_book["isbn"]
        updated_book["publication_year"] = (
            int(form_data.get("publication_year"))
            or self.selected_book["publication_year"]
        )
        self._update_book_in_list(updated_book)
        self.show_edit_book_modal = False
        self.selected_book = None
        return rx.toast.success(f"Updated '{updated_book['title']}'.")

    @rx.event
    def delete_book(self, book_id: int):
        if any((b for b in self.borrowed_books if b["book_id"] == book_id)):
            return rx.toast.error("Cannot delete a book that is currently borrowed.")
        book_to_delete = self._get_book_by_id(book_id)
        title = book_to_delete["title"] if book_to_delete else "Book"
        self.books = [b for b in self.books if b["id"] != book_id]
        self._all_books = [b for b in self._all_books if b["id"] != book_id]
        self.reservations = [r for r in self.reservations if r["book_id"] != book_id]
        self.show_book_modal = False
        self.selected_book = None
        return rx.toast.info(f"Deleted '{title}'.")