from sqlalchemy import create_engine, Column, Integer, String, DateTime, \
    Boolean
from sqlalchemy.ext.declarative import declarative_base
import datetime
from config_data.config import Config, load_config

Base = declarative_base()


class Subscribe(Base):
    __tablename__ = 'subscribes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    product_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    subscribe_status = Column(Boolean, default=True)


# данные для соединения с базой данных
config: Config = load_config('./config_data/.env')

db_host = config.db.db_host  # хост базы данных
db_port = config.db.db_port  # порт базы данных
db_database = config.db.db_database  # имя базы данных
db_user = config.db.db_user  # имя пользователя базы данных
db_password = config.db.db_password  # пароль пользователя базы данных

# Создаём строку подключения к базе данных
DATABASE_URL = f'postgresql://{db_user}:{db_password}@{db_host}/{db_database}'
# Создаем объект движка для подключения к базе данных
engine = create_engine(DATABASE_URL)

# Создаем все определенные таблицы
Base.metadata.create_all(engine)
