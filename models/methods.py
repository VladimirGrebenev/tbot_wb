from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Subscribe

from config_data.config import Config, load_config
from models.models import engine
# данные для соединения с базой данных
# config: Config = load_config('./config_data/.env')
#
# db_host = config.db.db_host  # хост базы данных
# db_port = config.db.db_port  # порт базы данных
# db_database = config.db.db_database  # имя базы данных
# db_user = config.db.db_user  # имя пользователя базы данных
# db_password = config.db.db_password  # пароль пользователя базы данных
#
# # Создаём строку подключения к базе данных
# DATABASE_URL = f'postgresql://{db_user}:{db_password}@{db_host}/{db_database}'
# # Создаём engine для взаимодействия с базой данных
# engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def create_subscription(user_id, product_id):
    """
    Создает новую подписку для пользователя с заданным user_id и product_id.

    Параметры:
        user_id: Идентификатор пользователя, для которого создается подписка.
        product_id: артикул продукта, на который пользователь подписывается.

    Возвращает:
        None
    """
    # Создаём новую сессию
    session = Session()
    user_id, product_id = int(user_id), int(product_id)
    # Создаём объект подписки
    new_subscription = Subscribe(user_id=user_id, product_id=product_id)

    # Добавляем объект подписки в сессию и сохраняем изменения в базе данных
    session.add(new_subscription)
    session.commit()

    # Закрываем сессию
    session.close()


def get_last_subscriptions(user_id, limit=5):
    """
    Возвращает последние подписки пользователя с заданным user_id.

    Параметры:
        user_id: Идентификатор пользователя, подписки которого нужно получить.

    Возвращает:
        list[Subscribe]: Список последних подписок пользователя.
    """
    # Создаём новую сессию
    session = Session()

    # Выбираем последние подписки пользователя
    last_subscriptions = session.query(Subscribe).filter(Subscribe.user_id == user_id).order_by(Subscribe.created_at.desc()).limit(limit).all()

    # Закрываем сессию
    session.close()

    return last_subscriptions


def check_existing_subscription(user_id, product_id):
    """
    Проверяет наличие существующей подписки для указанного user_id и product_id.

    Параметры:
        user_id (int): Идентификатор пользователя.
        product_id (int): Идентификатор продукта.

    Возвращает:
        Subscribe or None: Существующая подписка или None, если её нет.
    """
    session = Session()
    existing_subscription = session.query(Subscribe).filter_by(user_id=user_id, product_id=product_id).first()
    session.close()
    return existing_subscription