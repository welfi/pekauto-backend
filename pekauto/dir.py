from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Construct SQLite URL
sqlite_url = f'sqlite:///{BASE_DIR}/db.sqlite3'
print(sqlite_url)