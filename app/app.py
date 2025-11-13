import reflex as rx
from app.pages.login import login_page
from app.pages.register import register_page
from app.pages.dashboard import dashboard_page
from app.pages.books import books_page
from app.pages.manage_books import manage_books_page
from app.pages.users import users_page
from app.pages.code_page import code_page

app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(login_page, route="/")
app.add_page(register_page, route="/register")
app.add_page(dashboard_page, route="/dashboard")
app.add_page(books_page, route="/books")
app.add_page(manage_books_page, route="/manage-books")
app.add_page(users_page, route="/users")
app.add_page(code_page, route="/code")