# file: show_df_textual.py

import pandas as pd
from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.containers import Vertical

# Create a test DataFrame
df = pd.DataFrame({
    "clave": ["MAT101", "PHY202", "CS303"],
    "asignatura": ["Matemáticas", "Física", "Computación"],
    "credito": [4, 3, 5],
    "completo": [True, False, True],
})

class ShowDFApp(App):
    def compose(self) -> ComposeResult:
        with Vertical():
            for _, row in df.iterrows():
                text = f"{row['clave']} | {row['asignatura']} | {row['credito']} créditos"
                # Add visual cue if complete
                if row['completo']:
                    text = f"[green]{text} ✅[/green]"
                else:
                    text = f"[yellow]{text} ⏳[/yellow]"
                yield Static(text)

if __name__ == "__main__":
    ShowDFApp().run()
