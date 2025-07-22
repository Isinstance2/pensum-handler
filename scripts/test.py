from rich.text import Text
from rich.console import Console

def grade_bar(value: float, max_value: float = 100, width: int = 20) -> Text:
    percent = value / max_value
    filled_length = int(width * percent)
    empty_length = width - filled_length

    filled = "█" * filled_length
    empty = "░" * empty_length

    color = "green" if value >= 75 else "yellow" if value >= 60 else "red"

    return Text(filled, style=color) + Text(empty, style="dim")

console = Console()
test_values = [95, 82, 68, 50, 30, 10]

for val in test_values:
    console.print(f"Grade {val}:", grade_bar(val))
