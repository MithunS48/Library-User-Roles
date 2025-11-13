import reflex as rx
from reflex_monaco import monaco
from app.states.code_view_state import CodeViewState
from app.states.auth_state import AuthState
from app.components.base_layout import base_layout


def file_list_item(file_path: str) -> rx.Component:
    is_selected = CodeViewState.selected_file == file_path
    return rx.el.button(
        file_path,
        on_click=lambda: CodeViewState.select_file(file_path),
        class_name=rx.cond(
            is_selected,
            "w-full text-left px-3 py-2 text-sm font-medium rounded-md bg-gray-100 text-gray-900",
            "w-full text-left px-3 py-2 text-sm font-medium rounded-md hover:bg-gray-100 text-gray-600",
        ),
        width="100%",
    )


def code_view_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Application Code Viewer", class_name="text-2xl font-bold text-gray-900"
            ),
            rx.el.p(
                "Explore the source code of this application.",
                class_name="text-gray-600",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.aside(
                rx.el.h2("Files", class_name="text-lg font-semibold mb-4 px-3"),
                rx.el.div(
                    rx.foreach(CodeViewState.file_paths, file_list_item),
                    class_name="flex flex-col gap-1",
                ),
                class_name="w-full md:w-72 border-r p-4 bg-gray-50/50 flex-shrink-0 h-full overflow-y-auto",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.icon("file-code-2", class_name="h-5 w-5 text-gray-500"),
                            rx.el.span(
                                CodeViewState.selected_file,
                                class_name="font-mono text-sm",
                            ),
                            class_name="flex items-center gap-2",
                        ),
                        rx.el.button(
                            rx.icon("copy", class_name="h-4 w-4 mr-2"),
                            "Copy Code",
                            on_click=rx.set_clipboard(
                                CodeViewState.selected_file_content
                            ),
                            class_name="flex items-center text-sm font-semibold py-1 px-3 rounded-md bg-gray-200 text-gray-800 hover:bg-gray-300 transition-colors",
                        ),
                        class_name="flex justify-between items-center bg-gray-100 px-4 py-2 border-b",
                    ),
                    monaco(
                        value=CodeViewState.selected_file_content,
                        language=CodeViewState.language,
                        theme=rx.cond(rx.color_mode == "dark", "vs-dark", "light"),
                        height="calc(100vh - 200px)",
                        options={
                            "readOnly": True,
                            "fontSize": 14,
                            "minimap": {"enabled": False},
                        },
                    ),
                    class_name="w-full border rounded-lg overflow-hidden shadow-sm",
                ),
                class_name="flex-1 p-4",
            ),
            class_name="flex flex-col md:flex-row bg-white rounded-xl border shadow-sm",
        ),
        class_name="w-full bg-gradient-to-br from-slate-50 to-gray-200",
    )


@rx.page(on_load=[AuthState.check_login, CodeViewState.load_files])
def code_page() -> rx.Component:
    return base_layout(code_view_content())