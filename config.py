import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Base URL for the Mem API
BASE_URL = "https://api.mem.ai/v0/mems"

# Default headers for the API requests
HEADERS = {
    "Content-Type": "application/json",
}
