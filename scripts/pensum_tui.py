# pensum_tui.py
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static
from textual.widgets import Input, Label
from textual.containers import Vertical
from textual.screen import Screen
from textual.containers import Horizontal
from data.init_db import PensumLoaderFactory
from datetime import datetime
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


data_folder = r'/home/oa/projects/uni/data'


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
    width: 30;  /* narrower box */
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

    def on_button_pressed(self, event : Button.Pressed):
        if event.button.id == "unicaribe":
            self.push_screen(FileSelectionScreen())


class FileSelectionScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def compose(self) -> ComposeResult:
        yield  Header()
        yield Static("Selecciona el archivo pdf del pensum (escribe el numero):")
        self.files = [f for f in os.listdir(data_folder) if f.endswith(".pdf")]

        for idx, fname in enumerate(self.files):
            yield Static(f"[{idx}] {fname}")
        
        yield Input(placeholder="numero del archivo", id="file_number")
        yield Footer()
    
    

    def on_input_submitted(self, event: Input.Submitted) -> None:
        try:
            index = int(event.value)
            file_name = self.files[index]
            
            loader = PensumLoaderFactory.get_loader('unicaribe', os.path.join(data_folder, file_name))
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

            self.app.push_screen(UnicaribeScreen(file_output, summary_text))

        except (ValueError, IndexError) as e:
            self.app.bell()
            self.query_one(Input).placeholder = "❌ Entrada inválida. Intenta de nuevo."


class UnicaribeScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def __init__(self, content: str, summary_text : str) -> None:
        super().__init__()
        self.content = content
        self.summary_text = summary_text

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
        if event.button.id == "back":
            self.app.pop_screen()


if __name__ == "__main__":
    PensumApp().run()
