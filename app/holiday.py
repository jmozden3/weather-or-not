import json
import os
from datetime import datetime

def get_holiday_fact(date_str):
    # Convert 'YYYY-MM-DD' → 'MM-DD'
    try:
        key = datetime.strptime(date_str, "%Y-%m-%d").strftime("%m-%d")
        with open(os.path.join("data", "holidays.json"), "r") as f:
            holidays = json.load(f)
        return holidays.get(key, None)
    except:
        return None
