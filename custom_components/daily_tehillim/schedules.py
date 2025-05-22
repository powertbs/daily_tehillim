# custom_components/daily_tehillim/schedules.py

import logging
from datetime import date, timedelta
from hdate import HDate

_LOGGER = logging.getLogger(__name__)

START_DATE = date(2023, 9, 16)  # Rosh Hashanah 5784 or chosen start date for 5/day

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

def is_issur_melacha(hdate: HDate) -> bool:
    if hdate.holiday(only_issur=True):
        return True
    if hdate.gdate.weekday() == 5:  # Shabbos
        return True
    return False

def count_valid_tehillim_days(start: date, end: date) -> int:
    current = start
    count = 0
    while current <= end:
        hdate = HDate(current)
        if not is_issur_melacha(hdate):
            count += 1
        current += timedelta(days=1)
    return count

def num_to_hebrew(n: int) -> str:
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
        "קי", "קיא", "קיב", "קיג", "קיד", "קוה", "קיו", "קיז", "קיח", "קיט",
        "קכ", "קכא", "קכב", "קכג", "קכד", "קכה", "קכו", "קכז", "קכח", "קכט",
        "קל", "קלא", "קלב", "קלג", "קלד", "קלה", "קלו", "קלז", "קלח", "קלט",
        "קמ", "קמא", "קמב", "קמג", "קמד", "קמה", "קמו", "קמז", "קמח", "קמט",
        "קנ"
    ]
    return heb_map[n] if n < len(heb_map) else str(n)

def get_tehillim_portion(schedule_type: str, current_date: date | None = None) -> str:
    today = current_date or date.today()
    hdate = HDate(today)
    _LOGGER.debug("Today %s (Hebrew: %s)", today, hdate)

    if schedule_type == "5_per_day":
        valid_days = count_valid_tehillim_days(START_DATE, today)
        chapter_index = (valid_days * 5) % 150
        start = chapter_index + 1
        end = min(chapter_index + 5, 150)
        return f"{num_to_hebrew(start)}–{num_to_hebrew(end)}"

    if schedule_type == "monthly":
        idx = hdate.hebrew_day() - 1
        return YOM_LACHODESH[idx] if 0 <= idx < len(YOM_LACHODESH) else ""

    if schedule_type == "weekly":
        wd = (today.weekday() + 1) % 7
        return YOM_TEHILLIM_WEEKLY.get(wd, "")

    return ""
