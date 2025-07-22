from datetime import datetime
from scripts.pensum_tui import logging
from rich.text import Text
import pandas as pd
from rich.console import Group
from rich.panel import Panel
from rich.align import Align
from rich import box
from datetime import datetime

def get_avg_grade(summary):
    """Average Color Condition"""
    try: 
 
        if summary['avg'] >= 90:
            avg_grade = f"Avg Grade: {summary['avg']:.2f} 🟢"
        elif 75 <= summary['avg'] < 90:
            avg_grade =f"Avg Grade: {summary['avg']:.2f} 🟡"
        else:
            avg_grade = f"Avg Grade: {summary['avg']:.2f} 🔴"
        logging.info(f"Average grade calculated: {avg_grade}")

        return avg_grade
    except ValueError as e:
        logging.error(f"Error calculating average grade: {e}")
        return " Avg Grade: N/A"


def setup_table(df):
    rows = []
    for _, row in df.iterrows():
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
        rows.append(cells)
    return rows


def grade_bar(df, max_value: float = 100, width: int = 10) -> Group:
    bars = []
    df_bar = df.copy()
    df_bar = df_bar.sort_values(by='mes_cursado', ascending=True)  # Sort by 'mes_cursado'
    try:
        for i, (value, date_raw) in enumerate(zip(df_bar['nota'], df_bar['mes_cursado'])):
            # Format date to something nice
            date_str = ""
            if pd.notna(date_raw):
                if isinstance(date_raw, str):
                    date_raw = pd.to_datetime(date_raw)  # handle if it's still a string
                date_str = date_raw.strftime("%b %Y") # e.g., "Jan 2024"

            # N/A case
            if pd.isna(value) or value < 0:
                bar_text = Text("🟡 N/A", style="dim")
                panel = Panel(
                    bar_text,
                    title=f"[{i+1}] Sin nota ({date_str})" if date_str else f"[{i+1}] Sin nota",
                    border_style="yellow",
                    box=box.DOUBLE
                )
                bars.append(panel)
                continue

            # Calculate bar length
            percent = value / max_value
            filled_length = int(width * percent)
            empty_length = width - filled_length

            filled = "█" * filled_length
            empty = "░" * empty_length

            # Color and emoji logic
            color = "green" if value >= 75 else "yellow" if value >= 60 else "red"
            emoji = "🟢" if value >= 75 else "🟡" if value >= 60 else "🔴"

            # Bar text
            bar_text = Text()
            bar_text.append(f"{emoji} {value:5.1f} ", style="bold")
            bar_text.append(filled, style=f"bold {color}")
            bar_text.append(empty, style="dim")
            bar_text.append("|", style="green")

            # Panel with date
            panel_title = f"[{i+1}] {date_str}" if date_str else f"[{i+1}]"
            panel = Panel(
                bar_text,
                title=panel_title,
                border_style=color,
                box=box.DOUBLE,
                style="none"
            )

            bars.append(panel)

        return Group(*bars)

    except Exception as e:
        logging.error(f"Error generating grade bar: {e}")
        return Group(Text("❗ Error al generar barras", style="bold red"))


def setup_summary_box(target_date, summary):    
    """Setup the summary box."""
    try:
        today = datetime.today()
        delta = target_date - today
        years = delta.days // 365
        months = (delta.days % 365) // 30
        days = (delta.days % 365) % 30
        avg_grade = get_avg_grade(summary)

        summary_text = (
                    f"       📘PENSUM SUMMARY        \n"
                    f"───────────────────────────────\n"
                    f"Total Subjects: {summary['total']}\n"
                    f"Completed: {summary['completed']}\n"
                    f"Missing: {summary['missing']}\n"
                    f"{avg_grade}\n"
                    f"Time Left: {years} yrs, {months} mo, {days} days"
                )
        logging.info("Summary box setup completed.")
        return summary_text
    except Exception as e:
        logging.error(f"Error setting up summary box: {e}")
        return "📘 PENSUM SUMMARY: Error"