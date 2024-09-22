import os

from dotenv import load_dotenv

load_dotenv()

PROJECT = os.getenv("PROJECT")
STAGE = os.getenv("STAGE")
