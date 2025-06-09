# ⛅ Weather or Not

A quirky solo or group game where you guess the weather from a **random historical day** in a **city of your choice**. Score up to 100 based on how close you are on five weather questions — and learn a fun holiday fact for that day too.

---

## 🚀 Live App

👉 [Play it here](weather-or-not-c0crfdghawf7ebah.eastus2-01.azurewebsites.net)

> **Note:** The live Azure link above may not always be available or public. If you see a 404 or error, try running the app locally using the instructions below.

---

## 🧠 How It Works

1. Enter a city name
2. Get assigned a random date from **1980–today**
3. Guess the:
   - High temperature
   - Low temperature
   - Whether it rained
   - Sunrise time
   - Sunset time
4. See your score out of 100 and compare to the actual data
5. Get a holiday fun fact from that day 📅

---

## ⚙️ Tech Stack

- **Backend**: Python + Flask
- **Frontend**: HTML, CSS, JS
- **APIs**:
  - [Open-Meteo](https://open-meteo.com/) for historical weather data
  - [Nominatim](https://nominatim.org/) for city geocoding
- **Deployment**: Azure App Service via GitHub Actions


---

## 💡 Gameplay Tips

- Best results with major cities (e.g. New York, London, Tokyo)
- Weather coverage is strongest from **1980 onward**
- Scoring is positive-based — you gain points for accuracy!
- Game data is powered by public datasets (expect occasional gaps)

---

## 🛠 Dev Instructions

1. Clone the repo
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or .\\venv\\Scripts\\activate on Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run locally:
   ```bash
   python run.py
   ```

---

## 📦 Deployment

- Deployed using **GitHub Actions** and **Azure App Service**
- Automatically deploys on every push to `main`

---

## 🙌 Contributions

PRs welcome! Submit issues or enhancements anytime.

---

## 📜 License

MIT – free to use, modify, or remix.



