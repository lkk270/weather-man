import os
from dotenv import load_dotenv

load_dotenv()

NWS_BASE_URL = "https://api.weather.gov"
DATABASE_URL = os.getenv("DATABASE_URL")
