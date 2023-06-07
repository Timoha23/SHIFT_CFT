import os

from dotenv import load_dotenv


load_dotenv()

DB_PORT = os.getenv("DB_PORT")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")

DATABASE_URL = (f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}"
                f"/{DB_NAME}")

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # время жизни токена
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")


TEST_DB_PORT = os.getenv("TEST_DB_PORT")
TEST_DB_HOST = os.getenv("TEST_DB_HOST")
TEST_DB_NAME = os.getenv("TEST_DB_NAME")
TEST_DB_USER = os.getenv("TEST_DB_USER")
TEST_DB_PASS = os.getenv("TEST_DB_PASS")

TEST_DATABASE_URL = (f"postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASS}@"
                     f"{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}")
