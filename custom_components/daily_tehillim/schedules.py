from datetime import date
from hdate import HDate

# Each entry is a list of kapitlach or a string range label.
FIVE_PER_DAY = [
    "א-ה", "ו-י", "יא-טו", "טז-כ", "כא-כה",
    "כו-ל", "לא-לה", "לו-מ", "מא-מה", "מו-נ",
    "נא-נה", "נו-ס", "סא-סה", "סו-ע", "עא-עה",
    "עו-פ", "פא-פה", "פו-צ", "צט-קג", "קד-קי",
    "קיא-קטו", "קטז-קכ", "קכא-קכה", "קכו-קל", "קלא-קלד",
    "קלה-קלט", "קמ-קמד", "קמה-קמט", "קנ-קנד", "קנה-קנ"
]

YOM_LACHODESH = [
    "א-ה", "ו-י", "יא-טו", "טז-כ", "כא-כה",
    "כו-ל", "לא-לה", "לו-מ", "מא-מה", "מו-נ",
    "נא-נה", "נו-ס", "סא-סה", "סו-ע", "עא-עה",
    "עו-פ", "פא-פה", "פו-צ", "צט-קג", "קד-קי",
    "קיא-קטו", "קטז-קכ", "קכא-קכה", "קכו-קל", "קלא-קלד",
    "קלה-קלט", "קמ-קמד", "קמה-קמט", "קנ-קנד", "קנה-קנ"
]

YOM_TEHILLIM_WEEKLY = {
    0: "א-כ",         # Sunday: 1–20
    1: "כא-מא",       # Monday: 21–41
    2: "מב-סה",       # Tuesday: 42–65
    3: "סו-צ",        # Wednesday: 66–90
    4: "צא-קו",       # Thursday: 91–106
    5: "קז-קיט",      # Friday: 107–119:96
    6: "קכ-קנ"         # Shabbos: 120–150
}

def get_tehillim_portion(schedule_type: str, today: date = None) -> str:
    today = today or date.today()
    hdate = HDate(today)
    weekday = today.weekday()  # Monday is 0, Sunday is 6 (we shift accordingly)

    if schedule_type == "5_per_day":
        return FIVE_PER_DAY[_get_satmar_index(hdate)]

    if schedule_type == "monthly":
        return YOM_LACHODESH[hdate.hebrew_day() - 1]

    if schedule_type == "weekly":
        return YOM_TEHILLIM_WEEKLY.get((weekday + 1) % 7, "")

    return ""

def _get_satmar_index(hdate: HDate) -> int:
    """
    Returns the current index in the 5-per-day schedule, skipping issur melacha days.
    This version assumes we always start at index 0 and advance only on allowed days.
    """
    # This is a placeholder for a stateful tracker or persistent file logic,
    # which you'd use in the full sensor.py code.
    return 0