import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    APP_NAME = os.getenv(
        "APP_NAME",
        "PrepAI"
    )

    APP_ENV = os.getenv(
        "APP_ENV",
        "development"
    )

    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY"
    )

    CHROMA_PATH = os.getenv(
        "CHROMA_PATH",
        "chroma_db"
    )

    TOP_K = int(
        os.getenv(
            "TOP_K",
            "5"
        )
    )


settings = Settings()