from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, DataTable   
from textual.widgets import Input
from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from data.init_db import PensumLoaderFactory
from datetime import datetime
import os
import sys
import logging
from rich.text import Text
import pandas as pd

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
        color: #E0E6ED;
    }

    .menu-title {
    background: transparent;
    color: #E0E6ED;
    border: round #10B981;
    }

    .centered-menu {
    align: center top;
    width: 100%;
    align-horizontal: center;
    }

    
    /* Base Buttons */
    Button {
        margin: 1 2;
        width: 100%;
        padding: 1 1;
        background: transparent;
        color: white;
        border: none;
        text-style: bold;
        
    }

    Button:hover {
        background: #10B981;
        color: #FFFFFF;
        border: round none ;
    }

    /* Static Boxes */
    Static {
        color: #E0E6ED;
        background: #1E222A;
        border: round #1F2937;
        padding: 1 2;
        width: 100%;
        height: auto;
        text-style: bold;
    }

    /* Summary Panel */
    Static#summary_box {
        width: 100%;
        padding: 1 2;
        border: none;
        background: transparent;
        
    }

    /* Edit Button */
    .edit-btn {
        background: #1E293B;
        width: 85%;
        color: #E0E6ED;
        padding: 1 2;
        border: round #3B82F6;
        text-style: bold;
        margin: 1;
    }

    .edit-btn:hover {
        background: #2563EB;
        color: #FFFFFF;
        border: round #93C5FD;
    }

    /* Save Button */
    .save-btn {
        background: #1E293B;
        width: 100%;
        color: #E0E6ED;
        padding: 1 2;
        border: round #3B82F6;
        text-style: bold;
        margin: 1;
    }

    /* Scrollable Course List */
    #course_list {
        width: 4fr;
        height: 100%;
        overflow: auto;
        padding: 1;
        border: none;
        background: transparent;
    }

    .file-item {
        padding: 1 1;
        background: transparent;
        color: white;
        border: none;
    }  

    /* Course Boxes */
    .course-box {
    border: none; /* or use a subtle border if you prefer */
    padding: 0 1;
    margin: 1;
    width: 100%;
    height: auto;
    content-align: left middle;
    background: transparent;
    color: #E0E6ED;  /* Light floating text */
    text-style: bold;
}

    /* Completed Courses */
    .course-box.completed {
        border: none;
        color: #10B981; /* Mint green floating text */
        background: transparent;
    }

    /* Pending Courses */
    .course-box.pending {
        border: none;
        color: #8B5CF6; /* Lavender/purple floating text */
        background: transparent;
    }

    DataTable {
    background: transparent;
    color: yellow;
    border: none;
    scrollbar-background: transparent;
    scrollbar-color: transparent;
    }

    """




    def __init__(self):
        super().__init__()
        self.files = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(classes="centered-menu"):
            # Main menu
            yield Static("Selecciona universidad:", classes="menu-title")
            yield Button("Unicaribe", id="unicaribe", classes="start-btn")
            yield Button("🚪 Exit", id="exit")
            yield Input(placeholder="Fecha de termino aproximada (YYYY-MM-DD)", id="target_date", classes="course-input")
            yield Static("Ejemplo: 2028-03-04", classes="menu-title")
        
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "unicaribe":
        # If target_date is not set, set it to default and show a message
            if not hasattr(self, "target_date") or self.target_date is None:
                self.target_date = datetime.strptime("1995-03-04", "%Y-%m-%d")
                logging.info("No date entered, using default 1995-03-04")
                # Optionally, show a message to the user
                self.mount(Static("Fecha guardada ✅ (default)", classes="menu-title"))
            self.push_screen(FileSelectionScreen())
        elif event.button.id == "exit":
            self.exit()

    def on_input_submitted(self, event: Input.Submitted):
        if event.input.id == "target_date":
            value = event.value.strip()
            if not value:
                self.target_date = datetime.strptime("1995-03-04", "%Y-%m-%d")
                logging.info("No date entered, using default 1995-03-04")
                target_input = self.query_one("#target_date", Input)
                target_input.remove()
                self.mount(Static("Fecha guardada ✅ (default)", classes="menu-title"))
            else:
                try:
                    self.target_date = datetime.strptime(value, "%Y-%m-%d")
                    logging.info(f"Target date set to: {self.target_date}")
                    target_input = self.query_one("#target_date", Input)
                    target_input.remove()
                    self.mount(Static("Fecha guardada ✅", classes="menu-title"))
                except ValueError:
                    logging.error("Invalid date format. Please use YYYY-MM-DD.")
                    event.input.placeholder = "❌ Formato inválido. Usa YYYY-MM-DD"

class FileSelectionScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("/data:", classes="menu-title")
        self.files = [f for f in os.listdir(data_folder) if f.endswith((".pdf", ".csv"))]

        for idx, fname in enumerate(self.files):
            yield Static(f"[{idx}] {fname}", classes="file-item")

        yield Input(placeholder="numero del archivo", id="file_number", classes="course-input")
        yield Footer()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        try:
            index = int(event.value)
            selected_file = self.files[index]

            file_to_load = get_actual_file_to_load(selected_file)  # filename only

            
            loader = PensumLoaderFactory.get_loader('unicaribe', file_to_load)
            df = loader.df
            self.db = df.copy()
            summary = loader.completed_summary()

            today = datetime.today()
            target_date = self.app.target_date if hasattr(self.app, 'target_date') else datetime.strptime("2028-03-04", "%Y-%m-%d")
            if not target_date:
                target_date = datetime.strptime("1995-03-04", "%Y-%m-%d")
            delta = target_date - today
            years = delta.days // 365
            months = (delta.days % 365) // 30
            days = (delta.days % 365) % 30

            if summary['avg'] >= 90:
                 avg_grade = f"📊 Avg Grade: {summary['avg']:.2f} 🟢"
            elif 75 <= summary['avg'] < 90:
                avg_grade =f"📊 Avg Grade: {summary['avg']:.2f} 🟡"
            else:
                avg_grade = f"📊 Avg Grade: {summary['avg']:.2f} 🔴"

            summary_text = (
                f"       📘PENSUM SUMMARY        \n"
                f"────────────────────────────────\n"
                f"🟢 Total Subjects: {summary['total']}\n"
                f"✅ Completed: {summary['completed']}\n"
                f"❌ Missing: {summary['missing']}\n"
                f"{avg_grade}\n"
                f"📅 Time Left: {years} yrs, {months} mo, {days} days"
            )

            file_output = df

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
        self.file_name = file_name
        self.db = pd.DataFrame() 

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal():
            # Course list display
            with Vertical(id="course_list"):
                table = DataTable(zebra_stripes=False)
                table.add_columns(
                    "Asignatura", "Clave", "Créditos", "Pre-req", "Mes cursado", "Nota", "Estado"
                )

                for _, row in self.content.iterrows():
                    is_complete = row["completo"]

                    style = "bold green" if is_complete else "bold white"

                    # Ensure no background override
                    cells = [
                        Text(str(row["asignatura"]), style=style),
                        Text(str(row["clave"]), style=style),
                        Text(str(row["credito"]), style=style),
                        Text(str(row["pre_req"]), style=style),
                        Text(str(row["mes_cursado"])[:10], style=style),
                        Text(str(row["nota"]), style=style),
                        Text("Completado" if is_complete else "Pendiente", style=style),
                    ]

                    table.add_row(*cells)

                yield table
            
            #display the DataFrame as a Static widget
            for _, row in self.db.iterrows():
                date = str(row['mes_cursado'])
                gpa  = int(row['nota'])

            

            # Summary + Button
            with Vertical(id="summary_container"):
                    yield Static(self.summary_text, id="summary_box")
                    with Horizontal():
                        pass 

                        
                        


                    yield Button("✏️ Editar registro", id="edit_record", classes="start-btn")

        yield Button("Volver", id="back")
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
            yield Input(placeholder="Nombre de asignatura:", id="subject_name", classes="menu-title")
            yield Input(placeholder="Mes cursado (YYYY-MM):", id="subject_month", classes="menu-title")
            yield Input(placeholder="Calificación:", id="grade", classes="menu-title")
            yield Button("💾 Guardar Registro", id="save_record", classes="start-btn")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_record":
            subject_name = self.query_one("#subject_name", Input).value
            subject_month_raw = self.query_one("#subject_month", Input).value
            grade_raw = self.query_one("#grade", Input).value

            try:
                subject_month = datetime.strptime(subject_month_raw, "%Y-%m").date().replace(day=1)
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

                if summary['avg'] >= 90:
                    avg_grade = f"📊 Avg Grade: {summary['avg']:.2f} 🟢"
                elif 75 <= summary['avg'] < 90:
                    avg_grade =f"📊 Avg Grade: {summary['avg']:.2f} 🟡"
                else:
                    avg_grade = f"📊 Avg Grade: {summary['avg']:.2f} 🔴"

            summary_text = (
                f"       📘PENSUM SUMMARY        \n"
                f"────────────────────────────────\n"
                f"🟢 Total Subjects: {summary['total']}\n"
                f"✅ Completed: {summary['completed']}\n"
                f"❌ Missing: {summary['missing']}\n"
                f"{avg_grade}\n"
                f"📅 Time Left: {years} yrs, {months} mo, {days} days"
            )

            self.app.push_screen(UnicaribeScreen(df, summary_text, self.file_name))
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