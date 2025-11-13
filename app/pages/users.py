import reflex as rx
from app.states.auth_state import AuthState, User
from app.states.book_state import BookState
from app.components.base_layout import base_layout, role_badge


def user_row(user: User) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.image(
                    src=f"https://api.dicebear.com/9.x/initials/svg?seed={user['name']}",
                    class_name="h-10 w-10 rounded-full",
                ),
                rx.el.div(
                    rx.el.p(user["name"], class_name="font-semibold"),
                    rx.el.p(user["username"], class_name="text-sm text-gray-500"),
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="p-4",
        ),
        rx.el.td(role_badge(user["role"]), class_name="p-4"),
        rx.el.td(
            BookState.user_borrowed_counts.get(user["username"], 0).to_string(),
            class_name="p-4 font-medium",
        ),
        rx.el.td(
            rx.el.button(
                "View Activity", class_name="text-blue-600 font-semibold text-sm"
            ),
            class_name="p-4",
        ),
    )


def users_content() -> rx.Component:
    return rx.el.div(
        rx.el.h1("User Management", class_name="text-2xl font-bold text-gray-900 mb-6"),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "User",
                            class_name="text-left p-4 font-semibold text-gray-600",
                        ),
                        rx.el.th(
                            "Role",
                            class_name="text-left p-4 font-semibold text-gray-600",
                        ),
                        rx.el.th(
                            "Borrowed Books",
                            class_name="text-left p-4 font-semibold text-gray-600",
                        ),
                        rx.el.th(
                            "Actions",
                            class_name="text-left p-4 font-semibold text-gray-600",
                        ),
                    )
                ),
                rx.el.tbody(rx.foreach(AuthState.users, user_row)),
                class_name="w-full table-auto text-sm",
            ),
            class_name="w-full overflow-x-auto bg-white rounded-xl border border-gray-100 shadow-sm",
        ),
        class_name="w-full bg-gradient-to-br from-sky-50 to-blue-100",
    )


@rx.page(on_load=[AuthState.check_login])
def users_page() -> rx.Component:
    return rx.el.div(
        rx.cond(
            AuthState.current_user_role == "Librarian",
            base_layout(users_content()),
            base_layout(rx.el.div("Access Denied. Only for Librarians.")),
        )
    )