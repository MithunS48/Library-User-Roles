import reflex as rx
from app.states.auth_state import AuthState
from app.states.book_state import BookState, Book, Category, Reservation
from app.components.base_layout import base_layout


def availability_badge(is_available: rx.Var[bool]) -> rx.Component:
    return rx.el.span(
        rx.cond(is_available, "Available", "Borrowed"),
        class_name=rx.cond(
            is_available,
            "absolute top-3 right-3 text-xs font-bold text-white bg-gradient-to-r from-emerald-500 to-green-500 px-2.5 py-1 rounded-full shadow-lg",
            "absolute top-3 right-3 text-xs font-bold text-white bg-gradient-to-r from-amber-500 to-orange-500 px-2.5 py-1 rounded-full shadow-lg",
        ),
    )


def book_card(book: Book) -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.el.div(
                rx.image(
                    src=book["cover_image_url"],
                    alt=f"Cover of {book['title']}",
                    class_name="h-48 w-full object-cover group-hover:opacity-80 transition-opacity",
                ),
                availability_badge(book["is_available"]),
                class_name="relative",
            ),
            rx.el.div(
                rx.el.h3(book["title"], class_name="font-bold text-lg text-gray-900"),
                rx.el.p(book["author"], class_name="text-sm text-gray-600 font-medium"),
                rx.el.span(
                    book["category"],
                    class_name="mt-2 inline-block bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-1 rounded-full",
                ),
                class_name="p-4 bg-white",
            ),
            on_click=lambda: BookState.open_book_modal(book),
            class_name="w-full text-left bg-white rounded-xl shadow-sm border border-gray-200/80 overflow-hidden group hover:shadow-xl hover:-translate-y-1 transition-all duration-300",
        )
    )


def reservation_item(reservation: Reservation) -> rx.Component:
    return rx.el.div(
        rx.el.p(f"- {reservation['user_username']}", class_name="text-sm text-gray-700")
    )


def book_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.cond(
                BookState.selected_book,
                rx.el.div(
                    rx.image(
                        src=BookState.selected_book["cover_image_url"],
                        class_name="w-full h-64 object-cover rounded-t-xl",
                    ),
                    rx.el.div(
                        rx.el.h2(
                            BookState.selected_book["title"],
                            class_name="text-3xl font-bold mb-2 text-gray-900",
                        ),
                        rx.el.p(
                            f"by {BookState.selected_book['author']}",
                            class_name="text-lg text-gray-600 mb-4",
                        ),
                        rx.el.span(
                            BookState.selected_book["category"],
                            class_name="inline-block bg-blue-100 text-blue-800 text-sm font-semibold px-3 py-1 rounded-full mb-4",
                        ),
                        rx.el.p(
                            BookState.selected_book["description"],
                            class_name="text-gray-700 mb-6",
                        ),
                        rx.cond(
                            BookState.selected_book["is_available"],
                            rx.el.button(
                                rx.icon("book-up-2", class_name="mr-2"),
                                "Borrow Book",
                                on_click=lambda: BookState.borrow_book(
                                    BookState.selected_book["id"]
                                ),
                                class_name="w-full flex items-center justify-center bg-blue-600 text-white font-semibold py-3 px-4 rounded-md hover:bg-blue-700 transition",
                            ),
                            rx.el.div(
                                rx.el.button(
                                    rx.icon("bookmark", class_name="mr-2"),
                                    "Reserve Book",
                                    on_click=lambda: BookState.reserve_book(
                                        BookState.selected_book["id"]
                                    ),
                                    class_name="w-full flex items-center justify-center bg-amber-500 text-white font-semibold py-3 px-4 rounded-md hover:bg-amber-600 transition",
                                ),
                                rx.el.div(
                                    rx.el.h3(
                                        "Reservation Queue",
                                        class_name="font-semibold text-md mt-4 mb-2",
                                    ),
                                    rx.cond(
                                        BookState.get_book_reservations.length() > 0,
                                        rx.foreach(
                                            BookState.get_book_reservations,
                                            reservation_item,
                                        ),
                                        rx.el.p(
                                            "No reservations yet.",
                                            class_name="text-sm text-gray-500",
                                        ),
                                    ),
                                    class_name="mt-4 p-3 bg-gray-50 rounded-lg",
                                ),
                            ),
                        ),
                        rx.dialog.close(
                            rx.el.button(
                                rx.icon("x", class_name="h-5 w-5"),
                                class_name="absolute top-4 right-4 text-gray-500 hover:text-gray-800 p-1 rounded-full bg-white/50 hover:bg-gray-100 transition",
                            )
                        ),
                        class_name="p-6 relative",
                    ),
                ),
            ),
            class_name="bg-white rounded-xl shadow-2xl max-w-2xl w-full",
        ),
        open=BookState.show_book_modal,
        on_open_change=BookState.set_show_book_modal,
    )


def add_book_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.el.form(
                rx.el.h2(
                    "Add New Book", class_name="text-2xl font-bold text-gray-800 mb-6"
                ),
                rx.el.div(
                    rx.el.label("Title", class_name="text-sm font-medium"),
                    rx.el.input(name="title", class_name="mt-1 w-full input-field"),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Author", class_name="text-sm font-medium"),
                    rx.el.input(name="author", class_name="mt-1 w-full input-field"),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Category", class_name="text-sm font-medium"),
                    rx.el.select(
                        rx.foreach(
                            BookState.all_book_categories,
                            lambda cat: rx.el.option(cat, value=cat),
                        ),
                        name="category",
                        class_name="mt-1 w-full input-field",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Cover Image URL", class_name="text-sm font-medium"),
                    rx.el.input(
                        name="cover_image_url",
                        placeholder="/placeholder.svg",
                        class_name="mt-1 w-full input-field",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Description", class_name="text-sm font-medium"),
                    rx.el.textarea(
                        name="description", class_name="mt-1 w-full input-field"
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label("ISBN", class_name="text-sm font-medium"),
                        rx.el.input(name="isbn", class_name="mt-1 w-full input-field"),
                        class_name="w-full",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Publication Year", class_name="text-sm font-medium"
                        ),
                        rx.el.input(
                            name="publication_year",
                            type="number",
                            class_name="mt-1 w-full input-field",
                        ),
                        class_name="w-full",
                    ),
                    class_name="flex gap-4 mb-6",
                ),
                rx.el.div(
                    rx.dialog.close(
                        rx.el.button(
                            "Cancel", type="button", class_name="btn-secondary"
                        )
                    ),
                    rx.el.button("Add Book", type="submit", class_name="btn-primary"),
                    class_name="flex justify-end gap-3",
                ),
                on_submit=[BookState.add_book, BookState.close_add_book_modal],
            ),
            class_name="p-8 bg-white rounded-lg shadow-xl w-full max-w-lg",
        ),
        open=BookState.show_add_book_modal,
        on_open_change=BookState.set_show_add_book_modal,
    )


def edit_book_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.cond(
                BookState.selected_book,
                rx.el.form(
                    rx.el.h2(
                        "Edit Book", class_name="text-2xl font-bold text-gray-800 mb-6"
                    ),
                    rx.el.div(
                        rx.el.label("Title", class_name="text-sm font-medium"),
                        rx.el.input(
                            name="title",
                            default_value=BookState.selected_book["title"],
                            key=BookState.selected_book["id"].to_string() + "title",
                            class_name="mt-1 w-full input-field",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label("Author", class_name="text-sm font-medium"),
                        rx.el.input(
                            name="author",
                            default_value=BookState.selected_book["author"],
                            key=BookState.selected_book["id"].to_string() + "author",
                            class_name="mt-1 w-full input-field",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label("Category", class_name="text-sm font-medium"),
                        rx.el.select(
                            rx.foreach(
                                BookState.all_book_categories,
                                lambda cat: rx.el.option(cat, value=cat),
                            ),
                            name="category",
                            default_value=BookState.selected_book["category"],
                            key=BookState.selected_book["id"].to_string() + "category",
                            class_name="mt-1 w-full input-field",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Cover Image URL", class_name="text-sm font-medium"
                        ),
                        rx.el.input(
                            name="cover_image_url",
                            default_value=BookState.selected_book["cover_image_url"],
                            key=BookState.selected_book["id"].to_string() + "cover",
                            class_name="mt-1 w-full input-field",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label("Description", class_name="text-sm font-medium"),
                        rx.el.textarea(
                            name="description",
                            default_value=BookState.selected_book["description"],
                            key=BookState.selected_book["id"].to_string() + "desc",
                            class_name="mt-1 w-full input-field",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label("ISBN", class_name="text-sm font-medium"),
                            rx.el.input(
                                name="isbn",
                                default_value=BookState.selected_book["isbn"],
                                key=BookState.selected_book["id"].to_string() + "isbn",
                                class_name="mt-1 w-full input-field",
                            ),
                            class_name="w-full",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Publication Year", class_name="text-sm font-medium"
                            ),
                            rx.el.input(
                                name="publication_year",
                                type="number",
                                default_value=BookState.selected_book[
                                    "publication_year"
                                ].to_string(),
                                key=BookState.selected_book["id"].to_string()
                                + "pubyear",
                                class_name="mt-1 w-full input-field",
                            ),
                            class_name="w-full",
                        ),
                        class_name="flex gap-4 mb-6",
                    ),
                    rx.el.div(
                        rx.dialog.close(
                            rx.el.button(
                                "Cancel", type="button", class_name="btn-secondary"
                            )
                        ),
                        rx.el.button(
                            "Save Changes", type="submit", class_name="btn-primary"
                        ),
                        class_name="flex justify-end gap-3",
                    ),
                    on_submit=[BookState.update_book, BookState.close_edit_book_modal],
                ),
            ),
            class_name="p-8 bg-white rounded-lg shadow-xl w-full max-w-lg",
        ),
        open=BookState.show_edit_book_modal,
        on_open_change=BookState.set_show_edit_book_modal,
    )


def pagination_controls() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            "Previous",
            on_click=BookState.prev_page,
            disabled=BookState.current_page <= 1,
            class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed",
        ),
        rx.el.span(
            f"Page {BookState.current_page} of {BookState.total_pages}",
            class_name="text-sm text-gray-700 font-medium",
        ),
        rx.el.button(
            "Next",
            on_click=BookState.next_page,
            disabled=BookState.current_page >= BookState.total_pages,
            class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed",
        ),
        class_name="flex items-center justify-center gap-4 mt-8",
    )


def books_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Book Catalog", class_name="text-3xl font-bold text-gray-900 mb-2"
            ),
            rx.el.p(
                "Browse our collection and find your next read.",
                class_name="text-gray-600",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            rx.el.input(
                placeholder="Search by title or author...",
                on_change=BookState.set_search_query,
                class_name="w-full lg:w-1/3 px-4 py-2 bg-white border border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500",
                default_value=BookState.search_query,
            ),
            rx.el.div(
                rx.el.select(
                    rx.foreach(
                        BookState.all_categories,
                        lambda cat: rx.el.option(cat, value=cat),
                    ),
                    value=BookState.category_filter,
                    on_change=BookState.set_category_filter,
                    class_name="px-4 py-2 bg-white border border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500",
                ),
                rx.el.select(
                    rx.el.option("All Statuses", value="all"),
                    rx.el.option("Available", value="available"),
                    rx.el.option("Borrowed", value="borrowed"),
                    value=BookState.availability_filter,
                    on_change=BookState.set_availability_filter,
                    class_name="px-4 py-2 bg-white border border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500",
                ),
                class_name="flex gap-4",
            ),
            class_name="flex flex-col lg:flex-row justify-between items-center mb-8 gap-4",
        ),
        rx.el.div(
            rx.foreach(BookState.paginated_books, book_card),
            class_name="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6",
        ),
        pagination_controls(),
        book_modal(),
        class_name="w-full bg-gradient-to-b from-white to-gray-50",
    )


@rx.page(on_load=AuthState.check_login)
def books_page() -> rx.Component:
    return base_layout(books_content())