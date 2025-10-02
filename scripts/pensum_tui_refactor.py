from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, DataTable, LoadingIndicator, Select, Digits, ProgressBar
from textual.widgets import Input
from textual.containers import Vertical, Horizontal, VerticalScroll
from textual.screen import Screen
from textual import on
from textual.message import Message
from textual.reactive import reactive
from textual.containers import Center, Middle
import asyncio
from data.init_db import PensumLoaderFactory
from datetime import datetime
import os
import logging
import pandas as pd
from scripts.utils.configuration import load_env
from scripts.utils.configuration import get_actual_file_to_load
from config.css_config import CSS
from scripts.tui_display import setup_summary_box
from scripts.tui_display import setup_table
from scripts.tui_display import get_skill_avg
from scripts.tui_display import grade_bar
from tui_display import get_countdown
from scripts.models.llama_model import AiCompanion
from scripts.utils.configuration import load_logging
from time import monotonic
import plotext as plt
load_logging()
import logging



# Ensure the data folder exists
ENV_PATH = '/home/oa/projects/uni/config/.env'
data_folder = load_env(ENV_PATH, "DATA_FOLDER")



class PensumApp(App):
    enable_devtools = True  
    BINDINGS = [("d", "toggle_devtools", "Toggle DevTools")]
    # Define the CSS for the app, importing from the config file
    CSS = CSS

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.files = []
        

    def compose(self) -> ComposeResult:
        
        yield Static("Selecciona universidad:", classes="menu-title")
        with Vertical(classes="centered-menu"):
            yield Button("Unicaribe", id="unicaribe", classes="start-btn")
            yield Button("UASD 🚧🚧 ", id="uasd", classes="start-btn")
            yield LoadingIndicator(classes="loading-indicator")
            
        
        yield Footer()
        yield Input(placeholder="Fecha de termino aproximada (YYYY-MM-DD)", id="target_date")
        yield Static("Ejemplo: 2028-03-04", id="ejemplo")
        yield Button("🚪 Exit", id="exit")
        

    def action_toggle_devtools(self):
        if self.devtools:
            self.devtools.toggle()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "unicaribe":
        # If target_date is not set, set it to default and show a message
            if not hasattr(self, "target_date") or self.target_date is None:
                self.target_date = datetime.strptime("1995-03-04", "%Y-%m-%d")
                logging.info("No date entered, using default 1995-03-04")
                # Optionally, show a message to the user
                self.mount(Static("Fecha guardada  (default)", classes="menu-title"))
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
                self.mount(Static("Fecha guardada  (default)", classes="menu-title"))
            else:
                try:
                    self.target_date = datetime.strptime(value, "%Y-%m-%d")
                    logging.info(f"Target date set to: {self.target_date}")
                    target_input = self.query_one("#target_date", Input)
                    target_input.remove()
                    self.mount(Static("Fecha guardada ", classes="menu-title"))
                except ValueError:
                    logging.error("Invalid date format. Please use YYYY-MM-DD.")
                    event.input.placeholder = " Formato inválido. Usa YYYY-MM-DD"

class FileSelectionScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def __init__(self):
        super().__init__()
        self.files = [f for f in os.listdir(data_folder) if f.endswith((".pdf", ".csv"))]
        
    def compose(self) -> ComposeResult:
        options = [(file, file) for file in self.files] 
        
        yield Static("Selecciona un archivo para cargar", classes="menu-title")
        
        yield Vertical(
            
            Select(options=options, prompt="Archivo:",type_to_search=True),
        classes="centered-menu",
        )
        
        years, months, days = get_countdown(self.app.target_date, alt=True)
        countdown = years * 365 + months * 30 + days
        yield Digits(str(countdown), id="countdown")

        yield Footer()

    async def on_select_changed(self, event: Select.Changed) -> None:

        try:    
            self.selected_file = event.value
            file_to_load = get_actual_file_to_load(self.selected_file, data_folder)
            loader = PensumLoaderFactory.get_loader('unicaribe', file_to_load)
            df = loader.df
            self.db = df.copy()
            summary = loader.completed_summary()

            target_date = self.app.target_date if hasattr(self.app, 'target_date') else datetime.strptime("1995-03-04", "%Y-%m-%d")
            summary_text = setup_summary_box(target_date, summary)

            file_output = df

            await self.app.push_screen(UnicaribeScreen(file_output, summary_text, file_to_load))

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
        

        with Horizontal():
            # Course list display
            with Vertical(id="course_list"):
                table = DataTable(zebra_stripes=False, id="skills-table")
                table.add_columns(
                    "Asignatura", "Clave", "Créditos", "Pre-req", "Mes cursado", "Nota", "Estado"
                )

                for cells in setup_table(self.content):
                    table.add_row(*cells)
                yield table
    
            # Summary + Button
            with VerticalScroll(id="summary_container", classes="summary-container"):
                    yield Static(self.summary_text, id="summary_box")
                    yield Button("✏️  Editar registro", id="edit_record", classes="start-btn")
                    yield Button("📈 Stats Report", id="stat_report", classes="start-btn")
                    yield Button("🛑 Record classes", id="record", classes="start-btn")

                    
                    
                    yield Static(grade_bar(self.content), id="grade_bar")

                    

        yield Button("Volver", id="back", classes="start-btn")
        yield Footer()


    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "edit_record":
            self.app.push_screen(EditRecordScreen(self.file_name))
        elif event.button.id == "back":
            self.app.pop_screen()
        elif event.button.id == "stat_report":
            self.app.push_screen(StatReportScreen(self.file_name))
        elif event.button.id == "record":
            self.app.push_screen(RecordingScreen())

class TimeDisplay(Static):
    """Custom time display widget"""

    start_time = monotonic()
    time_elapsed = reactive(0)
    
    

    def watch_time_elapsed(self):
        time = self.time_elapsed
        time, seconds = divmod(time, 60)
        hours, minutes = divmod(time, 60) 
        time_string = f"{hours:02.0f}:{minutes:02.0f}:{seconds:05.2f}"
        self.update(time_string)

    def on_mount(self):
        self.update_timer = self.set_interval(
            1 / 60,
            self.update_time_elapsed,
            pause=True
        )

    def update_time_elapsed(self):
        self.time_elapsed = monotonic() - self.start_time

    def start(self):
        self.start_time = monotonic()
        self.time_elapsed = 0
        self.update_timer.resume()

    def stop(self):
        self.time_elapsed = monotonic() - self.start_time
        self.update_timer.pause()

class RecordBar(Static):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._last_time = 0.0
              

    def compose(self) -> ComposeResult:
        yield ProgressBar(id="progress") 
    

    def on_mount(self):
        
        self.time_update = self.set_interval(1/10, self.make_progress, pause=True)


    def make_progress(self):
        time_display = self.screen.query_one(TimeDisplay) 
        current_time = time_display.time_elapsed
        if current_time > self._last_time:
            self._last_time = current_time  # update the stored value
            self.query_one("#progress", ProgressBar).advance(1*0.5)

    def action_start(self):
        progress_bar = self.query_one("#progress", ProgressBar)
        progress_bar.update(total=14400, progress=0)
        self._last_time = 0.0 
        self.time_update.resume()

    def action_stop(self):
        self.time_update.pause()  
        self.query_one("#progress", ProgressBar).update(progress=0)
        
class RecordingScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]
    
    
    def __init__(self):
        super().__init__()

    @on(Button.Pressed, "#start-botton")
    def start_recording(self):
        self.add_class("started")
        self.query_one(TimeDisplay).start()
        self.query_one(RecordBar).action_start()

    @on(Button.Pressed, "#stop-botton")
    def stop_recording(self):
        self.remove_class("started")
        self.query_one(TimeDisplay).stop()
        self.query_one(RecordBar).action_stop()


    def compose(self) -> ComposeResult:
       
        yield TimeDisplay("00:00:00.00", id="time-display")
        
        with Center():
            with Middle():
                yield Button("Start", variant="success", id="start-botton")
                yield Button("Stop", variant="error", id="stop-botton" )
                yield RecordBar(id="record-bar")
                yield Button("Save recording", id="save-recording-botton", classes="save-recording") 
            

        yield Footer()      

class DataReady(Message):
    def __init__(self, sender, content : str, file_name : str) -> None:
        self.content = content
        self.sender = sender
        self.file_name = file_name
        super().__init__()

class StatReportScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name
        

    def compose(self) -> ComposeResult:
        table = DataTable(zebra_stripes=False)
        table.add_columns("skills", "%")

        for cells in get_skill_avg(os.path.join(f"{data_folder}", f"{self.file_name}")):
                table.add_row(*cells)
        
        yield Vertical(
            Static("Consultando al asistente virtual...", id="status"),
            LoadingIndicator(id="load-in"),
            table
        )
        
    async def on_mount(self):
        self.query_one("#load-in").display = True
        self.query_one("#status").update("💡 El asistente está pensando...")

        asyncio.create_task(self.run_ai_query())

    async def run_ai_query(self):   

        try:
            ai = AiCompanion(self.file_name) 
            result = await asyncio.to_thread(ai.call_assistant)
            
            self.post_message(DataReady(self, result, self.file_name))
            logging.debug("Initializing AI function...")

        except Exception as e:
            logging.error(f"Error: {e}")

    async def on_data_ready(self, message:DataReady):
        self.query_one("#load-in").display = False
        self.query_one("#status").update(message.content)      

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
                full_path = get_actual_file_to_load(self.file_name, data_folder) 
                logging.debug(f"{full_path}") # Get full path
                loader = PensumLoaderFactory.get_loader('unicaribe', full_path)
                loader.edit_record(subject_name, subject_month, grade)
                loader.save()
                df = loader.df
                summary = loader.completed_summary()
                summary_text = setup_summary_box(self.app.target_date, summary)

                

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

