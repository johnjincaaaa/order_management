from ..dal.base_dal import BaseDao
from ..dal.session_manager import SessionManager
from ..models.user import User


def test_query():
    session = SessionManager.get_session()
    users = BaseDao.get_list(session, User)
    for user in users:
        print(user.username)
        print('----------- carts -----------')
        for cart in user.carts:
            print(cart.subtotal)
        print('-----------------------------\n')


if __name__ == '__main__':
    test_query()