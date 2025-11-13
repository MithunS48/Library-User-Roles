import reflex as rx
from app.states.auth_state import AuthState
from app.components.base_layout import base_layout


def register_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("book-marked", class_name="h-8 w-8 text-blue-600"),
                rx.el.h1("LibSys", class_name="text-2xl font-bold"),
                class_name="flex items-center justify-center gap-2 mb-8",
            ),
            rx.el.h2(
                "Create an Account", class_name="text-3xl font-bold text-gray-800"
            ),
            rx.el.p(
                "Join our community to start borrowing books.",
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
                        "Full Name", class_name="text-sm font-medium text-gray-700"
                    ),
                    rx.el.input(
                        name="name",
                        placeholder="John Doe",
                        type="text",
                        class_name="mt-1 w-full px-4 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Username", class_name="text-sm font-medium text-gray-700"
                    ),
                    rx.el.input(
                        name="username",
                        placeholder="johndoe",
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
                rx.el.div(
                    rx.el.label("Role", class_name="text-sm font-medium text-gray-700"),
                    rx.el.select(
                        rx.el.option("Student", value="Student"),
                        rx.el.option("Teacher", value="Teacher"),
                        name="role",
                        default_value="Student",
                        class_name="mt-1 w-full px-4 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50",
                    ),
                    class_name="mb-6",
                ),
                rx.el.button(
                    "Create Account",
                    type="submit",
                    class_name="w-full bg-blue-600 text-white font-semibold py-3 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-300",
                ),
                on_submit=AuthState.register,
            ),
            rx.el.p(
                "Already have an account? ",
                rx.el.a(
                    "Sign in",
                    href="/",
                    class_name="font-medium text-blue-600 hover:underline",
                ),
                class_name="mt-6 text-center text-sm text-gray-600",
            ),
            class_name="w-full max-w-md p-8 bg-white/80 backdrop-blur-lg rounded-2xl shadow-2xl border border-gray-100",
        ),
        class_name="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4",
    )


@rx.page()
def register_page() -> rx.Component:
    return base_layout(register_form())