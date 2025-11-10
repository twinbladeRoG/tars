from datetime import datetime, time

from langchain.tools import tool

from src.core.logger import logger
from src.utils.time import utcnow

current_time = utcnow()


def generate_today_slots():
    today = datetime.now().date()

    raw_slots = [
        (time(10, 0), time(11, 0)),  # 10-11 AM
        (time(14, 0), time(15, 0)),  # 2-3 PM
        (time(16, 30), time(17, 0)),  # 4:30-5 PM
    ]

    slots = []
    for start_t, end_t in raw_slots:
        start = datetime.combine(today, start_t)
        end = datetime.combine(today, end_t)
        slots.append({"from": start.isoformat(), "till": end.isoformat()})

    return slots


time_slots = generate_today_slots()


@tool
def check_candidate_calendar(date_time: str | None = None):
    """Check candidate availability at a given ISO datetime OR list all available slots.

    Args:
        date_time: Optional ISO datetime string (e.g., "2025-02-10T15:00:00")
    """
    logger.debug(f"Date time: {date_time}")

    available_slots_text = "\n".join(
        f"- {slot['from']} to {slot['till']}" for slot in time_slots
    )

    if not date_time:
        return (
            "📅 Available interview slots:\n"
            f"{available_slots_text}\n\n"
            "ℹ️ Provide a datetime to check availability "
            "(e.g., '2025-02-10T10:30:00')"
        )

    try:
        interview_time = datetime.fromisoformat(date_time)
    except ValueError:
        return f"❌ Invalid datetime format: {date_time}. Use ISO format: YYYY-MM-DDTHH:MM:SS"

    for slot in time_slots:
        slot_start = datetime.fromisoformat(slot["from"])
        slot_end = datetime.fromisoformat(slot["till"])

        if slot_start <= interview_time < slot_end:
            return (
                f"✅ Candidate IS available at {date_time}\n\n"
                f"📅 Other available slots:\n{available_slots_text}"
            )

    return (
        f"❌ Candidate is NOT available at {date_time}\n\n"
        f"📅 Available slots:\n{available_slots_text}"
    )
