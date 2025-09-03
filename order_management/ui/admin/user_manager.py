import random
from decimal import Decimal, InvalidOperation
from bll import UserService
from dal.session_manager import SessionManager
from utils.constants import USER_STATUS_NORMAL_TEXT, USER_STATUS_FREEZE_TEXT, USER_ROLE_CUSTOM_TEXT, \
    USER_ROLE_ADMIN_TEXT, USER_STATUS_NORMAL, USER_ROLE_CUSTOM, USER_STATUS_FREEZE


def display_user(session, us):
    user_list = us.get_list(session)
    if user_list and len(user_list) > 0:
        print('------------------------- 用户列表 ------------------------')
        print('编号\t\t用户名\t\t用户余额\t\t用户角色\t\t状态')
        for user in user_list:
            status = USER_STATUS_NORMAL_TEXT if user.status == USER_STATUS_NORMAL else USER_STATUS_FREEZE_TEXT
            role = USER_ROLE_CUSTOM_TEXT if user.role == USER_ROLE_CUSTOM else USER_ROLE_ADMIN_TEXT
            print(f'{user.id}\t\t{user.username}\t\t{user.balance}\t\t{role}\t\t{status}')
        print('---------------------------------------------------------')
        print('1.用户充值\t2.重置密码\t3.激活用户\t4.冻结用户\t0.返回上级')
        print('---------------------------------------------------------')
    else:
        print('当前没有任何用户')
        print('---------------------------------------------------------')


def recharge_user(session, us):
    try:
        user_id = int(input('请输入待充值的用户编号：'))
        user = us.get_by_id(session, user_id)
        if user:
            recharge_amount = Decimal(input('请输入充值金额：'))
            user.balance += recharge_amount
            us.execute_commit(session)
            print('充值成功！')
        else:
            print('没有这个用户！')
    except ValueError:
        print('用户编号只能是整数！')
    except InvalidOperation:
        print('充值的金额只能是数字！')
    except Exception as e:
        print('未知异常，请查询日志信息')
        us.execute_rollback(session, e)

def reset_password(session, us):
    try:
        user_id = int(input('请输入需要重置密码的用户编号：'))
        user = us.get_by_id(session, user_id)
        if user:
            new_password = random.randint(100000, 999999)
            user.password = new_password
            us.execute_commit(session)
            print(f'密码修改成功，新的密码是{new_password}')
        else:
            print('没有这个用户！')
    except ValueError:
        print('用户编号只能是整数！')
    except Exception as e:
        print('未知异常，请查询日志信息')
        us.execute_rollback(session, e)


def active_user(session, us):
    try:
        user_id = int(input('请输入需要激活的用户编号：'))
        user = us.get_by_id(session, user_id)
        if user:
            if user.status == USER_STATUS_NORMAL:
                print('用户已经是激活状态了！')
                return
            user.status = USER_STATUS_NORMAL
            us.execute_commit(session)
            print('用户激活成功！')
        else:
            print('没有这个用户！')
    except ValueError:
        print('用户编号只能是整数！')
    except Exception as e:
        print('未知异常，请查询日志信息')
        session.rollback()
        us.execute_rollback(session, e)


def freeze_user(session, us):
    try:
        user_id = int(input('请输入需要冻结的用户编号：'))
        user = us.get_by_id(session, user_id)
        if user:
            if user.status == USER_STATUS_FREEZE:
                print('用户已经是激活状态了！')
                return
            user.status = USER_STATUS_FREEZE
            us.execute_commit(session)
            print('用户冻结成功！')
        else:
            print('没有这个用户！')
    except ValueError:
        print('用户编号只能是整数！')
    except Exception as e:
        print('未知异常，请查询日志信息')
        us.execute_rollback(session, e)

def user_manager():
    """但凡进到这里用户管理里面，我们就会多频次地操作数据，那么可以开启一个共用的session"""
    us = UserService()
    with SessionManager.get_session() as session:
        is_continue = True
        while is_continue:
            display_user(session, us)
            item = input('请选择：')
            if item == '1':
                recharge_user(session, us)
            elif item == '2':
                reset_password(session, us)
            elif item == '3':
                active_user(session, us)
            elif item == '4':
                freeze_user(session, us)
            elif item == '0':
                is_continue = False
            else:
                print('没有这个选项！')