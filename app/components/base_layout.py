import reflex as rx
from app.states.auth_state import AuthState


def role_badge(role: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        role,
        class_name=rx.match(
            role,
            (
                "Librarian",
                "text-xs font-semibold text-white bg-gradient-to-r from-purple-500 to-indigo-500 px-2.5 py-1 rounded-full w-fit shadow-md",
            ),
            (
                "Teacher",
                "text-xs font-semibold text-white bg-gradient-to-r from-emerald-500 to-teal-500 px-2.5 py-1 rounded-full w-fit shadow-md",
            ),
            (
                "Student",
                "text-xs font-semibold text-white bg-gradient-to-r from-amber-500 to-orange-500 px-2.5 py-1 rounded-full w-fit shadow-md",
            ),
            "bg-gray-500",
        ),
    )


def nav_item(
    label: str, icon: str, href: str, is_active: rx.Var[bool] | None = None
) -> rx.Component:
    active_classes = "flex items-center gap-3 rounded-lg px-3 py-2 text-blue-700 bg-blue-100/50 font-bold transition-all shadow-sm"
    inactive_classes = "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-600 font-medium transition-all hover:text-gray-900 hover:bg-gray-100/50"
    return rx.el.a(
        rx.icon(icon, class_name="h-5 w-5"),
        rx.el.span(label, class_name="text-sm"),
        href=href,
        class_name=rx.cond(
            is_active != None,
            rx.cond(is_active, active_classes, inactive_classes),
            inactive_classes,
        ),
    )


def sidebar_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.a(
                rx.icon("book-marked", class_name="h-7 w-7 text-blue-600"),
                rx.el.span("LibSys", class_name="text-xl font-bold"),
                href="/dashboard",
                class_name="flex items-center gap-2",
            ),
            class_name="flex h-16 items-center border-b px-6",
        ),
        rx.el.div(
            rx.el.nav(
                rx.el.div(
                    nav_item(
                        "Dashboard",
                        "layout-dashboard",
                        "/dashboard",
                        is_active=AuthState.router.page.path == "/dashboard",
                    ),
                    nav_item(
                        "Books",
                        "book-open",
                        "/books",
                        is_active=AuthState.router.page.path == "/books",
                    ),
                    class_name="flex flex-col gap-1",
                ),
                rx.el.div(
                    rx.cond(
                        AuthState.current_user_role == "Librarian",
                        rx.el.div(
                            rx.el.h3(
                                "Librarian Actions",
                                class_name="px-3 text-xs font-semibold uppercase text-gray-500",
                            ),
                            nav_item(
                                "Manage Books",
                                "book-up",
                                "/manage-books",
                                is_active=AuthState.router.page.path == "/manage-books",
                            ),
                            nav_item(
                                "Users",
                                "users",
                                "/users",
                                is_active=AuthState.router.page.path == "/users",
                            ),
                            class_name="flex flex-col gap-1 mt-4",
                        ),
                        None,
                    ),
                    rx.cond(
                        AuthState.current_user_role == "Teacher",
                        rx.el.div(
                            rx.el.h3(
                                "Teacher Actions",
                                class_name="px-3 text-xs font-semibold uppercase text-gray-500",
                            ),
                            nav_item("Reserved Books", "bookmark", "#"),
                            class_name="flex flex-col gap-1 mt-4",
                        ),
                        None,
                    ),
                    nav_item(
                        "View Code",
                        "code",
                        "/code",
                        is_active=AuthState.router.page.path == "/code",
                    ),
                    class_name="mt-auto flex flex-col gap-1",
                ),
                class_name="flex flex-col gap-4 py-4",
            ),
            class_name="flex-1 overflow-auto px-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.image(
                    src=f"https://api.dicebear.com/9.x/initials/svg?seed={AuthState.logged_in_user['name']}",
                    class_name="h-10 w-10 rounded-full shadow-md",
                ),
                rx.el.div(
                    rx.el.p(
                        AuthState.logged_in_user["name"],
                        class_name="text-sm font-semibold text-gray-800",
                    ),
                    role_badge(AuthState.current_user_role),
                    class_name="flex flex-col gap-1",
                ),
                rx.el.button(
                    rx.icon("log-out", class_name="h-5 w-5 text-gray-500"),
                    on_click=AuthState.logout,
                    class_name="ml-auto rounded-lg p-2 hover:bg-gray-100/80 transition-colors",
                ),
                class_name="flex items-center gap-4 p-4",
            ),
            class_name="mt-auto border-t bg-white p-2",
        ),
        class_name="flex h-full max-h-screen flex-col bg-gradient-to-b from-white to-gray-50",
    )


def base_layout(child_component: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.cond(
            AuthState.is_logged_in,
            rx.el.div(
                rx.el.aside(
                    sidebar_content(),
                    class_name="hidden border-r bg-white lg:block w-64 shrink-0",
                ),
                rx.el.div(
                    rx.cond(
                        AuthState.sidebar_open,
                        rx.el.div(
                            rx.el.div(
                                on_click=AuthState.toggle_sidebar,
                                class_name="fixed inset-0 bg-black/60 z-30",
                            ),
                            rx.el.aside(
                                sidebar_content(),
                                class_name="fixed inset-y-0 left-0 z-40 w-64 bg-white transition-transform transform translate-x-0",
                            ),
                        ),
                        rx.el.aside(
                            sidebar_content(),
                            class_name="fixed inset-y-0 left-0 z-40 w-64 bg-white transition-transform transform -translate-x-full",
                        ),
                    ),
                    rx.el.div(
                        rx.el.header(
                            rx.el.button(
                                rx.icon("panel-left", class_name="h-5 w-5"),
                                on_click=AuthState.toggle_sidebar,
                                class_name="lg:hidden",
                            ),
                            rx.el.h1("Welcome", class_name="text-lg font-semibold"),
                            class_name="flex items-center gap-4 h-16 border-b bg-white/80 backdrop-blur-sm px-6",
                        ),
                        rx.el.main(child_component, class_name="flex-1 p-4 md:p-6"),
                        class_name="flex flex-col flex-1",
                    ),
                    class_name="flex flex-col w-full",
                ),
                class_name="flex min-h-screen w-full",
            ),
            child_component,
        ),
        class_name="font-['Lora']",
    )