# 🕯️ Daily Tehillim

A custom Home Assistant sensor that guides you through daily Tehillim (Psalms) reading according to your preferred schedule.

## 📅 Features

- Fully automatic schedule rotation
- Aligns with the Hebrew calendar using `HDate`
- Skips Shabbos / Yom Tov when needed
- No YAML required — install via HACS

## 🔄 Supported Schedules

| Schedule Type          | Description |
|------------------------|-------------|
| **5 Chapters Per Day** | Fixed cycle, resumes after issur melacha days |
| **Yom LaChodesh**      | Based on Hebrew date (1–30), monthly reset |
| **Yom Tehillim Weekly**| Weekly cycle, repeats Sunday–Shabbos |

## 📦 Installation

1. Add this repository to HACS (as a custom repo)
2. Search for “Daily Tehillim” and install
3. Configure via the Home Assistant UI

## ✡️ Powered by HDate

Uses the `hdate` Python package for accurate Hebrew date tracking and Yom Tov awareness.

---

## Screenshots

Coming soon...

---

Pull requests welcome!

