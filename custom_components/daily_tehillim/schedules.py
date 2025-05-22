# custom_components/daily_tehillim/schedules.py

import logging
from datetime import date
from hdate import HebrewDate

_LOGGER = logging.getLogger(__name__)

# Each segment is five Psalms chapters
FIVE_PER_DAY = [
    "א-ה", "ו-י", "יא-טו", "טז-כ", "כא-כה",
    "כו-ל", "לא-לה", "לו-מ", "מא-מה", "מו-נ",
    "נא-נה", "נו-ס", "סא-סה", "סו-ע", "עא-עה",
    "עו-פ", "פא-פה", "פו-צ", "צט-קג", "קד-קי",
    "קיא-קטו", "קטז-קכ", "קכא-קכה", "קכו-קל", "קלא-קלד",
    "קלה-קלט", "קמ-קמד", "קמה-קמט", "קנ-קנד", "קנה-קנ"
]

# Same list used for daily “Yom LaChodesh” readings
YOM_LACHODESH = [
    "א-ה", "ו-י", "יא-טו", "טז-כ", "כא-כה",
    "כו-ל", "לא-לה", "לו-מ", "מא-מה", "מו-נ",
    "נא-נה", "נו-ס", "סא-סה", "סו-ע", "עא-עה",
    "עו-פ", "פא-פה", "פו-צ", "צט-קג", "קד-קי",
    "קיא-קטו", "קטז-קכ", "קכא-קכה", "קכו-קל", "קלא-קלד",
    "קלה-קלט", "קמ-קמד", "קמה-קמט", "קנ-קנד", "קנה-קנ"
]

# Weekly cycle: Sunday=0 … Saturday=6
YOM_TEHILLIM_WEEKLY = {
    0: "א-כ",    # Sunday: chapters 1–20
    1: "כא-מא",  # Monday: chapters 21–41
    2: "מב-סה",  # Tuesday: chapters 42–65
    3: "סו-צ",   # Wednesday: chapters 66–90
    4: "צא-קו",  # Thursday: chapters 91–106
    5: "קז-קיט", # Friday: chapters 107–119
    6: "קכ-קנ"   # Saturday: chapters 120–150
}


def get_tehillim_portion(schedule_type: str, current_date: date | None = None) -> str:
    """
    Return today’s Tehillim portion based on schedule_type:
      - '5_per_day': slice Psalms into 30 five-chapter segments by Hebrew day
      - 'monthly':  same as Yom LaChodesh (reuse FIVE_PER_DAY)
      - 'weekly':   fixed weekly mapping
    """
    today = current_date or date.today()
    # Properly convert the Gregorian date to a Hebrew date object
    hebrew_date = HebrewDate.from_gdate(today)
    _LOGGER.debug("Today (greg): %s → Hebrew date %s", today, hebrew_date)

    # 1) 5 chapters per day: index by hebrew day-of-month (1–30 → 0–29)
    if schedule_type == "5_per_day":
        day_num = hebrew_date.day  # 1..30
        idx = day_num - 1
        if 0 <= idx < len(FIVE_PER_DAY):
            portion = FIVE_PER_DAY[idx]
            _LOGGER.debug("5_per_day day %d → index %d → %s", day_num, idx, portion)
            return portion
        _LOGGER.error("5_per_day: Hebrew day %d out of range", day_num)
        return ""

    # 2) Monthly (Yom LaChodesh) uses the same 30-entry list
    if schedule_type == "monthly":
        day_num = hebrew_date.day
        idx = day_num - 1
        if 0 <= idx < len(YOM_LACHODESH):
            portion = YOM_LACHODESH[idx]
            _LOGGER.debug("monthly day %d → index %d → %s", day_num, idx, portion)
            return portion
        _LOGGER.error("monthly: Hebrew day %d out of range", day_num)
        return ""

    # 3) Weekly cycle
    if schedule_type == "weekly":
        # Python: Monday=0 … Sunday=6; shift so Sunday→0, Monday→1, … Saturday→6
        py_wd = today.weekday()
        idx = (py_wd + 1) % 7
        portion = YOM_TEHILLIM_WEEKLY.get(idx, "")
        _LOGGER.debug("weekly python_wd %d → idx %d → %s", py_wd, idx, portion)
        return portion

    _LOGGER.error("Unknown schedule_type '%s'", schedule_type)
    return ""
