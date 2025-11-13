import reflex as rx
from typing import Literal, TypedDict

Role = Literal["Student", "Librarian", "Teacher"]


class User(TypedDict):
    username: str
    password: str
    name: str
    role: Role


class AuthState(rx.State):
    users: list[User] = [
        {
            "username": "librarian",
            "password": "password",
            "name": "Admin User",
            "role": "Librarian",
        },
        {
            "username": "student",
            "password": "password",
            "name": "John Doe",
            "role": "Student",
        },
        {
            "username": "teacher",
            "password": "password",
            "name": "Jane Smith",
            "role": "Teacher",
        },
    ]
    logged_in_user: User | None = None
    error_message: str = ""
    sidebar_open: bool = False

    @rx.var
    def is_logged_in(self) -> bool:
        return self.logged_in_user is not None

    @rx.var
    def is_logged_in(self) -> bool:
        return self.logged_in_user is not None

    @rx.var
    def total_users(self) -> int:
        return len(self.users)

    @rx.event
    def get_user_by_username(self, username: str) -> User | None:
        for user in self.users:
            if user["username"] == username:
                return user
        return None

    @rx.var
    def current_user_role(self) -> Role | None:
        return self.logged_in_user["role"] if self.logged_in_user else None

    @rx.event
    def register(self, form_data: dict):
        username = form_data["username"]
        password = form_data["password"]
        name = form_data["name"]
        role = form_data["role"]
        if any((u["username"] == username for u in self.users)):
            self.error_message = "Username already exists."
            return
        new_user: User = {
            "username": username,
            "password": password,
            "name": name,
            "role": role,
        }
        self.users.append(new_user)
        self.logged_in_user = new_user
        self.error_message = ""
        return rx.redirect("/dashboard")

    @rx.event
    def login(self, form_data: dict):
        username = form_data["username"]
        password = form_data["password"]
        for user in self.users:
            if user["username"] == username and user["password"] == password:
                self.logged_in_user = user
                self.error_message = ""
                return rx.redirect("/dashboard")
        self.error_message = "Invalid username or password."

    @rx.event
    def logout(self):
        self.logged_in_user = None
        self.sidebar_open = False
        return rx.redirect("/")

    @rx.event
    def check_login(self):
        if not self.is_logged_in:
            return rx.redirect("/")

    @rx.event
    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open