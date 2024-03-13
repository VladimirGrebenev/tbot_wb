from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Subscribe

from config_data.config import Config, load_config
from models.models import engine


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
    last_subscriptions = session.query(Subscribe).filter(
        Subscribe.user_id == user_id).order_by(
        Subscribe.created_at.desc()).limit(limit).all()

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
    existing_subscription = session.query(Subscribe).filter_by(user_id=user_id,
                                                               product_id=product_id).first()
    if existing_subscription:
        if existing_subscription.subscribe_status == True:
            session.close()
            return True
        else:
            session.close()
            return False
    else:
        session.close()
        return False

def get_active_subscriptions():
    """
    Получает все активные подписки из базы данных.
    Нет параметров.
    Возвращает список активных подписок.
    """
    session = Session()
    subs = (session.query(Subscribe).
            filter(Subscribe.subscribe_status == True).all())
    session.close()
    return subs


def stop_active_subscriptions(user_id):
    """
    Остановить активные подписки для указанного идентификатора пользователя.

    Аргументы:
        user_id (int): Идентификатор пользователя, для которого следует остановить подписки.

    Возвращает:
        Ничего
    """
    session = Session()
    subs = session.query(Subscribe).filter_by(user_id=user_id).all()

    for sub in subs:
        sub.subscribe_status = False

    session.commit()
    session.close()
