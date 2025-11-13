import reflex as rx
import os
import logging


class CodeViewState(rx.State):
    file_paths: list[str] = []
    selected_file: str = ""

    @rx.var
    def selected_file_content(self) -> str:
        if not self.selected_file or not os.path.exists(self.selected_file):
            return "Select a file to view its content."
        try:
            with open(self.selected_file, "r") as f:
                return f.read()
        except Exception as e:
            logging.exception(f"Error reading file: {e}")
            return f"Error reading file: {e}"

    @rx.var
    def language(self) -> str:
        if self.selected_file.endswith(".py"):
            return "python"
        if self.selected_file.endswith(".js"):
            return "javascript"
        if self.selected_file.endswith(".css"):
            return "css"
        if self.selected_file.endswith(".html"):
            return "html"
        if self.selected_file.endswith(".json"):
            return "json"
        if self.selected_file.endswith(".md"):
            return "markdown"
        return "plaintext"

    @rx.event
    def select_file(self, file_path: str):
        self.selected_file = file_path

    @rx.event
    def load_files(self):
        base_files = ["rxconfig.py", "requirements.txt", ".gitignore"]

        @rx.event
        def get_files_in_dir(directory):
            file_list = []
            for root, _, files in os.walk(directory):
                for file in files:
                    if (
                        not file.endswith((".pyc", ".ico"))
                        and "__pycache__" not in root
                    ):
                        file_path = os.path.join(root, file)
                        if os.path.isfile(file_path):
                            file_list.append(file_path)
            return file_list

        app_dirs = ["app"]
        all_files = []
        for app_dir in app_dirs:
            all_files.extend(get_files_in_dir(app_dir))
        self.file_paths = sorted([f for f in list(set(base_files + all_files))])
        if not self.selected_file and self.file_paths:
            self.selected_file = self.file_paths[0]