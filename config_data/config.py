from dataclasses import dataclass
import os
import dotenv


@dataclass
class DatabaseConfig:
    db_database: str  # Название базы данных
    db_host: str  # URL-адрес базы данных
    db_user: str  # Username пользователя базы данных
    db_password: str  # Пароль к базе данных
    db_port: str  # Порт базы данных


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # Список id администраторов бота


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


def load_config(path: str | None = None) -> Config:
    """Функция создания экземпляра класса Config"""

    # Загуржаем данные из файла .env в Env
    dotenv.load_dotenv(path)

    # Добавляем в переменные данные, прочитанные из файла .env
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    ADMIN_IDS = os.getenv('ADMIN_IDS')
    DB_NAME = os.getenv('DB_NAME')
    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_PORT = os.getenv('DB_PORT')

    # Возвращаем экземпляр класса Config
    return Config(
        tg_bot=TgBot(
            token=BOT_TOKEN,
            admin_ids=ADMIN_IDS
        ),
        db=DatabaseConfig(
            db_database=DB_NAME,
            db_host=DB_HOST,
            db_user=DB_USER,
            db_password=DB_PASSWORD,
            db_port=DB_PORT
        )
    )
