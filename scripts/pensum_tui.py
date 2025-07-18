# pensum_tui.py
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static
from textual.containers import Vertical
from pensum_handler import PensumHandler
from textual.screen import Screen
from textual.containers import Horizontal
uni = PensumHandler()


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
    """



    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        summary = uni.completed_summary()
        text = (
        f"📘 PENSUM SUMMARY\n"
        f"─────────────────────\n"
        f"🟢 Total Subjects: {summary['total']}\n"
        f"✅ Completed: {summary['completed']}\n"
        f"❌ Missing: {summary['missing']}\n"
    )
        yield Static(text, id="summary_box")
        
        with Vertical():
            yield Button("📋 View Courses", id="view")
            yield Button("✅ Mark Completed", id="complete")
            yield Button("🚪 Exit", id="exit")
        yield Footer()

    def on_button_pressed(self, event : Button.Pressed):
        match event.button.id:
            case "view":
                self.view_courses_screen()

    def view_courses_screen(self):
    
        uni = PensumHandler()

        data = uni.display_table("courses")  # This is your DB call
        output = "\n".join(str(row) for row in data)
        summary = uni.completed_summary()
        summary_text = (
        f"📘 PENSUM SUMMARY\n"
        f"─────────────────────\n"
        f"🟢 Total Subjects: {summary['total']}\n"
        f"✅ Completed: {summary['completed']}\n"
        f"❌ Missing: {summary['missing']}\n"
        f"📊 avg: {summary['avg']}\n"
        f"{summary['remaining']}\n"

    )

        self.push_screen(CourseScreen(content=output, summary_text=summary_text))

class CourseScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def __init__(self, content: str, summary_text : str) -> None:
        super().__init__()
        self.content = content
        self.summary_text = summary_text

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield Static(self.content, id="course_list")
            yield Static(self.summary_text, id="summary_box")
        yield Button("🔙 Back", id="back")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()


if __name__ == "__main__":
    PensumApp().run()
