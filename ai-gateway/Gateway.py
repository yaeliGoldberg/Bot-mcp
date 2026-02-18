import os
import time
import logging
from collections import deque
from dotenv import load_dotenv
from google import genai


#File → Settings → Project: <שם הפרויקט> → Python Interpreter
# טוען משתני סביבה מהקובץ .env
load_dotenv()

# קריאת משתנים
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HARD_LIMIT_USD = float(os.getenv("HARD_LIMIT_USD", 5.0))

# הגדרת לוגים
logging.basicConfig(
    filename="gateway.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ניהול קצב בקשות (10 בדקה)
request_times = deque()
MAX_REQUESTS_PER_MINUTE = 10


# סימולציה בסיסית של עלות (לצורך בדיקת HARD_LIMIT)
current_usage_usd = 0.0
ESTIMATED_COST_PER_REQUEST = 0.01


def check_rate_limit():
    current_time = time.time()

    # הסרת בקשות שעברו יותר מדקה
    while request_times and current_time - request_times[0] > 60:
        request_times.popleft()

    if len(request_times) >= MAX_REQUESTS_PER_MINUTE:
        raise Exception("Rate limit exceeded: Max 10 requests per minute.")

    request_times.append(current_time)


def check_budget():
    global current_usage_usd

    if current_usage_usd + ESTIMATED_COST_PER_REQUEST > HARD_LIMIT_USD:
        raise Exception("Budget exceeded: HARD_LIMIT_USD reached.")

    current_usage_usd += ESTIMATED_COST_PER_REQUEST


def gateway(prompt: str) -> str:
    global GEMINI_API_KEY

    # 1️⃣ בדיקת קיום מפתח
    if not GEMINI_API_KEY:
        raise Exception("Missing GEMINI_API_KEY.")

    # 2️⃣ בדיקת תקציב
    check_budget()

    # 3️⃣ בדיקת עומס בקשות
    check_rate_limit()

    try:
        # 4️⃣ חיבור ל-Gemini


        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )


        print(response.text)

        # שמירת תשובה
        request = response.text

        logging.info("Request sent successfully to Gemini.")
        logging.info(f"Prompt: {prompt}")
        logging.info(f"Response: {request}")

        return request

    except Exception as e:
        logging.error(f"Error while sending request: {str(e)}")
        raise
