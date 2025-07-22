from datetime import datetime
from scripts.pensum_tui import logging

def get_avg_grade(summary):
    """Average Color Condition"""
    if summary['avg'] >= 90:
        avg_grade = f"📊 Avg Grade: {summary['avg']:.2f} 🟢"
    elif 75 <= summary['avg'] < 90:
        avg_grade =f"📊 Avg Grade: {summary['avg']:.2f} 🟡"
    else:
        avg_grade = f"📊 Avg Grade: {summary['avg']:.2f} 🔴"
    logging.info(f"Average grade calculated: {avg_grade}")

    return avg_grade



def setup_summary_box(target_date, summary):
    """Setup the summary box."""
    today = datetime.today()
    delta = target_date - today
    years = delta.days // 365
    months = (delta.days % 365) // 30
    days = (delta.days % 365) % 30
    avg_grade = get_avg_grade(summary)

    summary_text = (
                f"       📘PENSUM SUMMARY        \n"
                f"────────────────────────────────\n"
                f"🟢 Total Subjects: {summary['total']}\n"
                f"✅ Completed: {summary['completed']}\n"
                f"❌ Missing: {summary['missing']}\n"
                f"{avg_grade}\n"
                f"📅 Time Left: {years} yrs, {months} mo, {days} days"
            )
    logging.info("Summary box setup completed.")
    return summary_text