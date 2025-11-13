import reflex as rx
from app.states.auth_state import AuthState
from app.states.book_state import BookState, BorrowedBookWithDetails
from app.components.base_layout import base_layout


def stat_card(
    icon: str, title: str, value: rx.Var[str | int], color: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-7 w-7 text-white"),
            class_name=f"p-4 rounded-full bg-{color}-500/90",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-semibold text-gray-100"),
            rx.el.p(value, class_name="text-3xl font-bold text-white"),
            class_name="flex flex-col",
        ),
        class_name=f"flex items-center gap-4 p-6 rounded-2xl shadow-lg bg-gradient-to-br from-{color}-500 to-{color}-600 hover:-translate-y-1 transition-transform duration-300",
    )


def book_row(book_info: BorrowedBookWithDetails) -> rx.Component:
    book = book_info["book"]
    due_date = book_info["due_date"]
    return rx.el.tr(
        rx.el.td(
            rx.image(
                src=book["cover_image_url"],
                class_name="h-16 w-12 object-cover rounded-md",
            ),
            class_name="p-4",
        ),
        rx.el.td(
            rx.el.p(book["title"], class_name="font-semibold"),
            rx.el.p(book["author"], class_name="text-sm text-gray-500"),
            class_name="p-4",
        ),
        rx.el.td(due_date, class_name="p-4 text-sm text-gray-600"),
        rx.el.td(
            rx.el.button(
                "Return",
                on_click=lambda: BookState.return_book(book["id"]),
                class_name="text-blue-600 font-semibold text-sm",
            ),
            class_name="p-4",
        ),
    )


def borrowed_books_table(
    books_info: rx.Var[list[BorrowedBookWithDetails]],
) -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Your Borrowed Books", class_name="text-xl font-bold text-gray-800 mb-4"
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Cover",
                            class_name="text-left font-semibold text-gray-600 p-4",
                        ),
                        rx.el.th(
                            "Title",
                            class_name="text-left font-semibold text-gray-600 p-4",
                        ),
                        rx.el.th(
                            "Due Date",
                            class_name="text-left font-semibold text-gray-600 p-4",
                        ),
                        rx.el.th(
                            "Actions",
                            class_name="text-left font-semibold text-gray-600 p-4",
                        ),
                    )
                ),
                rx.el.tbody(rx.foreach(books_info, book_row)),
                class_name="w-full table-auto",
            ),
            class_name="w-full overflow-x-auto bg-white rounded-xl border border-gray-100 shadow-sm",
        ),
    )


def librarian_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Librarian Dashboard", class_name="text-2xl font-bold text-gray-900 mb-6"
        ),
        rx.el.div(
            stat_card("book", "Total Books", BookState.total_books, "blue"),
            stat_card(
                "book-check", "Borrowed Books", BookState.total_borrowed_books, "amber"
            ),
            stat_card("users", "Active Users", AuthState.total_users, "emerald"),
            stat_card(
                "file-warning", "Overdue Items", BookState.overdue_books_count, "red"
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6",
        ),
        class_name="w-full",
    )


def student_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            f"Welcome, {AuthState.logged_in_user['name']}!",
            class_name="text-2xl font-bold text-gray-900 mb-6",
        ),
        rx.el.div(
            stat_card(
                "book-up", "Available Books", BookState.available_books_count, "emerald"
            ),
            stat_card(
                "calendar-clock",
                "Books Due Soon",
                BookState.books_due_soon_count,
                "amber",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8",
        ),
        borrowed_books_table(BookState.current_user_borrowed_books_with_details),
        class_name="w-full flex flex-col gap-6",
    )


def teacher_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            f"Welcome, {AuthState.logged_in_user['name']}!",
            class_name="text-2xl font-bold text-gray-900 mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Priority Status",
                    class_name="text-sm font-semibold text-emerald-800 bg-emerald-100 px-3 py-1 rounded-full w-fit",
                ),
                rx.el.p(
                    "You have priority borrowing privileges.",
                    class_name="text-gray-600 mt-2 text-sm",
                ),
                class_name="p-6 bg-white rounded-xl border border-gray-100 shadow-sm",
            ),
            rx.el.div(
                rx.el.p(
                    "Borrowing Limit", class_name="text-sm font-medium text-gray-500"
                ),
                rx.el.p("10 / 15 books", class_name="text-2xl font-bold text-gray-900"),
                class_name="p-6 bg-white rounded-xl border border-gray-100 shadow-sm",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8",
        ),
        borrowed_books_table(BookState.current_user_borrowed_books_with_details),
        class_name="w-full flex flex-col gap-6",
    )


def dashboard_content() -> rx.Component:
    return rx.el.div(
        rx.match(
            AuthState.current_user_role,
            ("Librarian", librarian_dashboard()),
            ("Student", student_dashboard()),
            ("Teacher", teacher_dashboard()),
            rx.el.div("Loading dashboard..."),
        ),
        class_name=rx.match(
            AuthState.current_user_role,
            (
                "Librarian",
                "min-h-full w-full bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-100",
            ),
            (
                "Student",
                "min-h-full w-full bg-gradient-to-br from-green-50 via-teal-50 to-cyan-100",
            ),
            (
                "Teacher",
                "min-h-full w-full bg-gradient-to-br from-orange-50 via-pink-50 to-rose-100",
            ),
            "bg-gray-50",
        ),
    )


@rx.page(on_load=[AuthState.check_login, BookState.on_dashboard_load])
def dashboard_page() -> rx.Component:
    return base_layout(dashboard_content())