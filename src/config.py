import os

from dotenv import load_dotenv

dirname = os.path.dirname(__file__)

try:
    load_dotenv(dotenv_path=os.path.join(dirname, "..", ".env"))
except FileNotFoundError:
    pass

DATABASE_FILENAME = os.getenv("DATABASE_FILENAME") or "database.db"
DATABASE_FILE_PATH = os.path.join(dirname, "..", "data", DATABASE_FILENAME)

try:
    PERIODS_PER_YEAR = int(os.getenv("PERIODS_PER_YEAR") or 4)
except ValueError:
    PERIODS_PER_YEAR = 4

try:
    COURSE_NAME_WIDTH = int(os.getenv("COURSE_NAME_WIDTH") or 35)
except ValueError:
    COURSE_NAME_WIDTH = 35
