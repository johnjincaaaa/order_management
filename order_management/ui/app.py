from bll import UserService, login_manager
from dal import SessionManager
from models import User
from ui.admin.food_manager import food_manager
from ui.admin.order_manager import order_manager
from ui.admin.user_manager import user_manager
from ui.customer.my_cart import my_cart
from ui.customer.my_order import my_order
from ui.customer.to_ordering import to_ordering
from utils.constants import USER_ROLE_ADMIN, USER_ROLE_CUSTOM


def start():
    loading_main_menu()


def login_frame(role):
    print('-----------------------------------------------------')
    us = UserService()
    with SessionManager.get_session() as session:
        username = input('请输入账号：')
        password = input('请输入密码：')
        res, msg = us.login_check(session, username, password, role)
        print(msg)
        if res:
            if role == USER_ROLE_ADMIN:
                admin_menu()
            else:
                custom_menu()
    print('-----------------------------------------------------')


def to_admin_login():
    is_continue = True
    while is_continue:
        print('-------------------- 后台管理系统 --------------------')
        print('-------------------- 1.管理员登录 ---------------------')
        print('-------------------- 0.返回上级 ---------------------')
        print('-----------------------------------------------------')
        item = input('请选择：')
        if item == '1':
            login_frame(USER_ROLE_ADMIN)
        elif item == '0':
            is_continue = False


def admin_menu():
    is_continue = True
    while is_continue:
        print('-------------------- 后台管理菜单 --------------------')
        print('-------------------- 1.用户管理 ---------------------')
        print('-------------------- 2.菜品管理 ---------------------')
        print('-------------------- 3.订单管理 ---------------------')
        print('-------------------- 0.注销登录 ---------------------')
        print('-----------------------------------------------------')
        item = input('请选择：')
        if item == '1':
            user_manager()
        elif item == '2':
            food_manager()
        elif item == '3':
            order_manager()
        elif item == '0':
            login_manager.get_instance().logout()
            is_continue = False


def user_center(session, us):
    current_user_id = login_manager.current_user_id
    print('---------------------------------')
    if current_user_id:
        login_user = us.get_by_id(session, current_user_id)

        print(f'账户信息：{login_user.username}')
        print(f'账户余额：{login_user.balance}')
        print(f'注册时间：{login_user.create_at}')
    else:
        print('请先登录再操作！')
    print('---------------------------------')


def custom_menu():
    is_continue = True
    while is_continue:
        print('-------------------- 前台在线点餐 --------------------')
        print('-------------------- 1.我要点餐 ---------------------')
        print('-------------------- 2.我的餐车 ---------------------')
        print('-------------------- 3.我的订单 ---------------------')
        print('-------------------- 4.用户中心 ---------------------')
        print('-------------------- 0.注销登录 ---------------------')
        print('-----------------------------------------------------')
        item = input('请选择：')
        if item == '1':
            to_ordering()
        elif item == '2':
            my_cart()
        elif item == '3':
            my_order()
        elif item == '4':
            us = UserService()
            with SessionManager.get_session() as session:
                user_center(session, us)
        elif item == '0':
            login_manager.get_instance().logout()
            is_continue = False


def custom_register():
    """用户注册"""
    us = UserService()
    with SessionManager.get_session() as session:
        while True:
            username = input('请输入账号（输入Q退出注册）：')
            if username.upper() == 'Q':
                print('已退出注册界面！')
                return
            if us.get_single_by_condition(session, username=username):
                print('该账号已被注册！')
                continue
            break

        while True:
            password1 = input('请输入密码：')
            password2 = input('请确认密码：')
            if password1 != password2:
                print('两次输入密码不一致！')
                continue
            break
        try:
            new_user = User(username=username, password=password1, role=USER_ROLE_CUSTOM)
            result = us.create(session, new_user)
            if result:
                print('注册成功！')
            else:
                print('注册失败，请查看日志！')
        except Exception as e:
            print('未知错误，请查看日志')
            us.execute_rollback(session, e)


def to_custom_login():
    is_continue = True
    while is_continue:
        print('-------------------- 前台点餐窗口 --------------------')
        print('-------------------- 1.顾客登录 ---------------------')
        print('-------------------- 2.顾客注册 ---------------------')
        print('-------------------- 3.功能预览 ---------------------')
        print('-------------------- 0.返回上级 ---------------------')
        print('-----------------------------------------------------')
        item = input('请选择：')
        if item == '1':
            login_frame(USER_ROLE_CUSTOM)
        elif item == '2':
            custom_register()
        elif item == '3':
            custom_menu()
        elif item == '0':
            is_continue = False


def loading_main_menu():
    is_continue = True
    while is_continue:
        print('-------------------- 在线订餐系统 --------------------')
        print('-------------------- 1.后台管理 ---------------------')
        print('-------------------- 2.前台点餐 ---------------------')
        print('-------------------- 0.退出系统 ---------------------')
        print('-----------------------------------------------------')
        item = input('请选择：')
        if item == '1':
            to_admin_login()
        elif item == '2':
            to_custom_login()
        elif item == '0':
            print('系统已关闭！')
            is_continue = False

