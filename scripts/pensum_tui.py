# pensum_tui.py
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static
from textual.widgets import Input
from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from data.init_db import PensumLoaderFactory
from datetime import datetime
import os
import sys
import logging

log = logging.getLogger()
log.setLevel(logging.INFO)

file_handler = logging.FileHandler("PensumLoader.log", mode='a')
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
log.addHandler(file_handler)

console_handler = logging.StreamHandler(sys.__stdout__)
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
log.addHandler(console_handler)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

data_folder = r'/home/oa/projects/uni/data'

def get_actual_file_to_load(file_name):
    # If it's a PDF, check if corresponding CSV updated file exists
    if file_name.endswith('.pdf'):
        base_name = os.path.splitext(file_name)[0]
        updated_csv = f"{base_name}_updated.csv"
        updated_csv_path = os.path.join(data_folder, updated_csv)
        if os.path.exists(updated_csv_path):
            return updated_csv  # Return filename only
    return file_name

class PensumApp(App):
    CSS = """
    Screen {
        align: center middle;
        background: black;
    }
    Button {
        margin: 1;
        width: 30;
    }
    Static {
        color: yellow;
        background: black;
        border: round white;
        padding: 1 2;
        width: 80%;
        height: auto;
    }
    Static#summary_box {
        width: 30;
        padding: 1 2;
        border: black;
        color: yellow;
    }
    .edit-btn {
        background: $boost;
        color: $text;
        padding: 1 2;
        border: round yellow;
        text-style: bold;
    }
    .edit-btn:hover {
        background: $primary;
        color: $text;
    }
    """

    def __init__(self):
        super().__init__()
        self.files = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical():
            yield Static("Selecciona universidad:")
            yield Button("Unicaribe", id="unicaribe")
            yield Button("🚪 Exit", id="exit")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "unicaribe":
            self.push_screen(FileSelectionScreen())


class FileSelectionScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Selecciona el archivo pdf del pensum (escribe el numero):")
        self.files = [f for f in os.listdir(data_folder) if f.endswith((".pdf", ".csv"))]

        for idx, fname in enumerate(self.files):
            yield Static(f"[{idx}] {fname}")

        yield Input(placeholder="numero del archivo", id="file_number")
        yield Footer()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        try:
            index = int(event.value)
            selected_file = self.files[index]

            file_to_load = get_actual_file_to_load(selected_file)  # filename only

            
            loader = PensumLoaderFactory.get_loader('unicaribe', file_to_load)
            df = loader.df
            summary = loader.completed_summary()

            today = datetime.today()
            target_date = datetime.strptime("2028-03-04", "%Y-%m-%d")
            delta = target_date - today
            years = delta.days // 365
            months = (delta.days % 365) // 30
            days = (delta.days % 365) % 30

            summary_text = (
                f"📘 PENSUM SUMMARY\n"
                f"─────────────────────\n"
                f"🟢 Total Subjects: {summary['total']}\n"
                f"✅ Completed: {summary['completed']}\n"
                f"❌ Missing: {summary['missing']}\n"
                f"📊 Avg Grade: {summary['avg']:.2f}\n"
                f"📅 Time Left: {years} yrs, {months} mo, {days} days"
            )

            file_output = str(df)

            self.app.push_screen(UnicaribeScreen(file_output, summary_text, file_to_load))

        except (ValueError, IndexError) as e:
            self.app.bell()
            self.query_one(Input).placeholder = "❌ Entrada inválida. Intenta de nuevo."


class UnicaribeScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def __init__(self, content: str, summary_text: str, file_name: str) -> None:
        super().__init__()
        self.content = content
        self.summary_text = summary_text
        self.file_name = file_name  # Just filename

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal():
            yield Static(self.content, id="course_list")

            with Vertical(id="summary_container"):
                yield Static(self.summary_text, id="summary_box")
                yield Button("✏️ Edit Record", id="edit_record", classes="edit-btn")

        yield Button("🔙 Back", id="back")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "edit_record":
            self.app.push_screen(EditRecordScreen(self.file_name))
        elif event.button.id == "back":
            self.app.pop_screen()


class EditRecordScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name  # Just filename
        self.subject_name = None
        self.subject_month = None
        self.grade = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield Input(placeholder="Nombre de asignatura:", id="subject_name")
            yield Input(placeholder="Mes cursado (YYYY-MM):", id="subject_month")
            yield Input(placeholder="Calificación:", id="grade")
            yield Button("💾 Guardar Registro", id="save_record", classes="edit-btn")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_record":
            subject_name = self.query_one("#subject_name", Input).value
            subject_month_raw = self.query_one("#subject_month", Input).value
            grade_raw = self.query_one("#grade", Input).value

            try:
                subject_month = datetime.strptime(subject_month_raw, "%Y-%m")
                grade = float(grade_raw)
            except ValueError:
                self.app.bell()
                return

            if subject_name:
                full_path = get_actual_file_to_load(self.file_name) 
                logging.debug(f"{full_path}") # Get full path
                loader = PensumLoaderFactory.get_loader('unicaribe', full_path)
                loader.edit_record(subject_name, subject_month, grade)
                loader.save()
                df = loader.df
                summary = loader.completed_summary()

                today = datetime.today()
                target_date = datetime.strptime("2028-03-04", "%Y-%m-%d")
                delta = target_date - today
                years = delta.days // 365
                months = (delta.days % 365) // 30
                days = (delta.days % 365) % 30

                summary_text = (
                    f"📘 PENSUM SUMMARY\n"
                    f"─────────────────────\n"
                    f"🟢 Total Subjects: {summary['total']}\n"
                    f"✅ Completed: {summary['completed']}\n"
                    f"❌ Missing: {summary['missing']}\n"
                    f"📊 Avg Grade: {summary['avg']:.2f}\n"
                    f"📅 Time Left: {years} yrs, {months} mo, {days} days"
                )

                self.app.push_screen(UnicaribeScreen(str(df), summary_text, self.file_name))
            else:
                self.app.bell()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        input_id = event.input.id
        value = event.value

        if input_id == "subject_name":
            self.subject_name = value
        elif input_id == "subject_month":
            try:
                self.subject_month = datetime.strptime(value, "%Y-%m")
            except ValueError:
                self.subject_month = None
        elif input_id == "grade":
            try:
                self.grade = float(value)
            except ValueError:
                self.grade = None

if __name__ == "__main__":
    PensumApp().run()
