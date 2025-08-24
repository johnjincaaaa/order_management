def start():
    loading_main_menu()


def admin_login_frame():
    print('管理员登录')


def to_admin_login():
    is_continue = True
    while is_continue:
        print('-------------------- 后台管理系统 --------------------')
        print('-------------------- 1.管理员登录 ---------------------')
        print('-------------------- 0.返回上级 ---------------------')
        print('-----------------------------------------------------')
        item = input('请选择：')
        if item == '1':
            admin_login_frame()
        elif item == '0':
            is_continue = False


def to_customer_login():
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
            print('顾客登录')
        elif item == '2':
            print('顾客注册')
        elif item == '3':
            print('功能预览')
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
            to_customer_login()
        elif item == '0':
            print('系统已关闭！')
            is_continue = False

