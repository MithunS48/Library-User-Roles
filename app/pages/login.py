import reflex as rx
from app.states.auth_state import AuthState
from app.components.base_layout import base_layout


def demo_account_card(role: str, username: str, icon: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name=f"h-6 w-6 {color}"),
        rx.el.div(
            rx.el.h3(role, class_name="font-semibold text-gray-800"),
            rx.el.p(
                rx.el.span("User: ", class_name="font-medium text-gray-600"),
                username,
                class_name="text-sm text-gray-800 font-mono",
            ),
            rx.el.p(
                rx.el.span("Pass: ", class_name="font-medium text-gray-600"),
                "password",
                class_name="text-sm text-gray-800 font-mono",
            ),
            class_name="flex flex-col",
        ),
        class_name="flex items-center gap-4 p-3 bg-gray-50 rounded-lg border border-gray-200 w-full",
    )


def login_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("book-marked", class_name="h-8 w-8 text-blue-600"),
                    rx.el.h1("LibSys", class_name="text-2xl font-bold"),
                    class_name="flex items-center justify-center gap-2 mb-8",
                ),
                rx.el.h2("Welcome Back", class_name="text-3xl font-bold text-gray-800"),
                rx.el.p(
                    "Enter your credentials to access your account.",
                    class_name="text-gray-500 mt-2 mb-6",
                ),
                rx.el.form(
                    rx.cond(
                        AuthState.error_message != "",
                        rx.el.div(
                            rx.el.p(AuthState.error_message),
                            class_name="mb-4 rounded-md bg-red-50 p-3 text-center text-sm text-red-600 border border-red-200",
                        ),
                        None,
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Username", class_name="text-sm font-medium text-gray-700"
                        ),
                        rx.el.input(
                            name="username",
                            placeholder="m@example.com",
                            type="text",
                            class_name="mt-1 w-full px-4 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Password", class_name="text-sm font-medium text-gray-700"
                        ),
                        rx.el.input(
                            name="password",
                            type="password",
                            class_name="mt-1 w-full px-4 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50",
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.button(
                        "Sign In",
                        type="submit",
                        class_name="w-full bg-blue-600 text-white font-semibold py-3 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-300",
                    ),
                    on_submit=AuthState.login,
                ),
                rx.el.p(
                    "Don't have an account? ",
                    rx.el.a(
                        "Sign up",
                        href="/register",
                        class_name="font-medium text-blue-600 hover:underline",
                    ),
                    class_name="mt-6 text-center text-sm text-gray-600",
                ),
                class_name="w-full max-w-md p-8 bg-white/80 backdrop-blur-lg rounded-2xl shadow-2xl border border-gray-100",
            ),
            rx.el.div(
                rx.el.h2(
                    "Demo Accounts",
                    class_name="text-xl font-bold text-gray-800 text-center mb-4",
                ),
                rx.el.div(
                    demo_account_card(
                        "Librarian", "librarian", "user-cog", "text-purple-600"
                    ),
                    demo_account_card(
                        "Teacher", "teacher", "user-check", "text-emerald-600"
                    ),
                    demo_account_card("Student", "student", "user", "text-amber-600"),
                    class_name="grid grid-cols-1 md:grid-cols-3 gap-4",
                ),
                class_name="w-full max-w-4xl p-6 mt-8 bg-white/80 backdrop-blur-lg rounded-2xl shadow-xl border border-gray-100",
            ),
            class_name="flex flex-col items-center",
        ),
        class_name="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4",
    )


@rx.page()
def login_page() -> rx.Component:
    return base_layout(login_form())