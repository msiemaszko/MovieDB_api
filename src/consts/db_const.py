from src.main.settings import DB_HOST, DB_PORT, DB_NAME, DB_PASS, DB_USER

POSTGRESQL_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
