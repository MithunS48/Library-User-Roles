import reflex as rx
from app.states.auth_state import AuthState
from app.states.book_state import BookState, Book
from app.components.base_layout import base_layout
from app.pages.books import add_book_modal, edit_book_modal


def book_manage_row(book: Book) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.image(
                src=book["cover_image_url"], class_name="h-12 w-9 object-cover rounded"
            ),
            class_name="p-3",
        ),
        rx.el.td(book["title"], class_name="p-3 font-medium"),
        rx.el.td(book["author"], class_name="p-3 text-gray-600"),
        rx.el.td(book["category"], class_name="p-3 text-gray-600"),
        rx.el.td(
            rx.el.span(
                rx.cond(book["is_available"], "Available", "Borrowed"),
                class_name=rx.cond(
                    book["is_available"],
                    "px-2 py-1 text-xs rounded-full bg-emerald-100 text-emerald-800",
                    "px-2 py-1 text-xs rounded-full bg-amber-100 text-amber-800",
                ),
            ),
            class_name="p-3",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("copy", class_name="h-4 w-4"),
                    on_click=lambda: BookState.open_edit_book_modal(book),
                    class_name="p-2 hover:bg-gray-100 rounded-md",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4 text-red-600"),
                    on_click=lambda: BookState.delete_book(book["id"]),
                    class_name="p-2 hover:bg-red-50 rounded-md",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="p-3",
        ),
    )


def manage_books_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Manage Books", class_name="text-2xl font-bold text-gray-900"),
            rx.el.button(
                rx.icon("plus", class_name="h-4 w-4 mr-2"),
                "Add New Book",
                on_click=BookState.open_add_book_modal,
                class_name="flex items-center bg-blue-600 text-white px-4 py-2 rounded-lg font-semibold text-sm hover:bg-blue-700 transition",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Cover",
                            class_name="text-left p-3 font-semibold text-gray-600",
                        ),
                        rx.el.th(
                            "Title",
                            class_name="text-left p-3 font-semibold text-gray-600",
                        ),
                        rx.el.th(
                            "Author",
                            class_name="text-left p-3 font-semibold text-gray-600",
                        ),
                        rx.el.th(
                            "Category",
                            class_name="text-left p-3 font-semibold text-gray-600",
                        ),
                        rx.el.th(
                            "Status",
                            class_name="text-left p-3 font-semibold text-gray-600",
                        ),
                        rx.el.th(
                            "Actions",
                            class_name="text-left p-3 font-semibold text-gray-600",
                        ),
                    )
                ),
                rx.el.tbody(rx.foreach(BookState.books, book_manage_row)),
                class_name="w-full table-auto text-sm",
            ),
            class_name="w-full overflow-x-auto bg-white rounded-xl border border-gray-100 shadow-sm",
        ),
        add_book_modal(),
        edit_book_modal(),
        class_name="w-full bg-gradient-to-br from-gray-50 to-slate-100",
    )


@rx.page(on_load=[AuthState.check_login, BookState.on_dashboard_load])
def manage_books_page() -> rx.Component:
    return rx.el.div(
        rx.cond(
            AuthState.current_user_role == "Librarian",
            base_layout(manage_books_content()),
            base_layout(rx.el.div("Access Denied. Only for Librarians.")),
        )
    )