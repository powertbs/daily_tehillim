# custom_components/daily_tehillim/schedules.py

import logging
from datetime import date, timedelta
from hdate import HDateInfo                    # <— for holiday detection
from hdate.hebrew_date import HebrewDate as HDate

_LOGGER = logging.getLogger(__name__)

# Start counting from Rosh Hashanah 5784
START_DATE = date(2023, 9, 16)

YOM_LACHODESH = [
    "א-ה", "ו-י", "יא-טו", "טז-כ", "כא-כה",
    "כו-ל", "לא-לה", "לו-מ", "מא-מה", "מו-נ",
    "נא-נה", "נו-ס", "סא-סה", "סו-ע", "עא-עה",
    "עו-פ", "פא-פה", "פו-צ", "צט-קג", "קד-קי",
    "קיא-קטו", "קטז-קכ", "קכא-קכה", "קכו-קל", "קלא-קלד",
    "קלה-קלט", "קמ-קמד", "קמה-קמט", "קנ-קנד", "קנה-קנ"
]

YOM_TEHILLIM_WEEKLY = {
    0: "א-כ",    # Sunday
    1: "כא-מא",  # Monday
    2: "מב-סה",  # Tuesday
    3: "סו-צ",   # Wednesday
    4: "צא-קו",  # Thursday
    5: "קז-קיט", # Friday
    6: "קכ-קנ"   # Shabbos
}


def is_issur_melacha(g_date: date) -> bool:
    """Return True if g_date is Shabbat or a Jewish holiday (Yom Tov/fast day)."""
    info = HDateInfo(g_date)
    if info.is_holiday:
        return True
    # Python: Monday=0 … Sunday=6; Saturday is day 5
    if g_date.weekday() == 5:
        return True
    return False


def count_valid_tehillim_days(start: date, end: date) -> int:
    """Count days between start→end, skipping issur-melacha days."""
    current = start
    count = 0
    while current <= end:
        if not is_issur_melacha(current):
            count += 1
        current += timedelta(days=1)
    return count


def num_to_hebrew(n: int) -> str:
    """Map integer to Hebrew chapter string (1→'א', …, 150→'קע')."""
    heb_map = [
        "", "א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט",
        "י", "יא", "יב", "יג", "יד", "טו", "טז", "יז", "יח", "יט",
        "כ", "כא", "כב", "כג", "כד", "כה", "כו", "כז", "כח", "כט",
        "ל", "לא", "לב", "לג", "לד", "לה", "לו", "לז", "לח", "לט",
        "מ", "מא", "מב", "מג", "מד", "מה", "מו", "מז", "מח", "מט",
        "נ", "נא", "נב", "נג", "נד", "נה", "נו", "נז", "נח", "נט",
        "ס", "סא", "סב", "סג", "סד", "סה", "סו", "סז", "סח", "סט",
        "ע", "עא", "עב", "עג", "עד", "עה", "עו", "עז", "עח", "עט",
        "פ", "פא", "פב", "פג", "פד", "פה", "פו", "פז", "פח", "פט",
        "צ", "צא", "צב", "צג", "צד", "צה", "צו", "צז", "צח", "צט",
        "ק", "קא", "קב", "קג", "קד", "קה", "קו", "קז", "קח", "קט",
        "קי", "קיא", "קיב", "קיג", "קיד", "קטו", "קטז", "קיז", "קיח", "קיט",
        "קכ", "קכא", "קכב", "קכג", "קכד", "קכה", "קכו", "קכז", "קכח", "קכט",
        "קל", "קלא", "קלב", "קלג", "קלד", "קלה", "קלו", "קלז", "קלח", "קלט",
        "קמ", "קמא", "קמב", "קמג", "קמד", "קמה", "קמו", "קמז", "קמח", "קמט",
        "קנ"
    ]
    return heb_map[n] if 0 < n < len(heb_map) else str(n)


def get_tehillim_portion(
    schedule_type: str,
    current_date: date | None = None
) -> str:
    """
    Return today’s Tehillim portion:
      • '5_per_day': skip holidays/Shabbos entirely
      • 'monthly' & 'weekly': always return something
    """
    today = current_date or date.today()
    hdate = HDate.from_gdate(today)
    _LOGGER.debug("Today %s → Hebrew %s", today, hdate)

    if schedule_type == "5_per_day":
        if is_issur_melacha(today):
            _LOGGER.debug("Issur-melacha on %s: skipping 5_per_day", today)
            return ""

        valid_days = count_valid_tehillim_days(START_DATE, today)
        # Day 1 (start date) → Psalms 1–5
        index = ((valid_days - 1) * 5) % 150
        start, end = index + 1, min(index + 5, 150)
        portion = f"{num_to_hebrew(start)}–{num_to_hebrew(end)}"
        _LOGGER.debug("5_per_day valid_days=%d → %s", valid_days, portion)
        return portion

    if schedule_type == "monthly":
        idx = hdate.day - 1
        portion = YOM_LACHODESH[idx] if 0 <= idx < len(YOM_LACHODESH) else ""
        _LOGGER.debug("monthly day %d → %s", hdate.day, portion)
        return portion

    if schedule_type == "weekly":
        idx = (today.weekday() + 1) % 7
        portion = YOM_TEHILLIM_WEEKLY.get(idx, "")
        _LOGGER.debug("weekly weekday %d → idx %d → %s", today.weekday(), idx, portion)
        return portion

    _LOGGER.error("Unknown schedule_type '%s'", schedule_type)
    return ""
