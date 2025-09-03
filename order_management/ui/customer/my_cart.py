from decimal import Decimal, InvalidOperation
from bll import login_manager, OrderService, UserService
from bll.cart_service import CartService
from dal import SessionManager
from models.order import Order, OrderDetails
from utils.constants import ORDER_STATUS_UNPAID
from utils.tools import generate_order_no


def display_cart(session, cs, login_user):
    cart_items = cs.get_list_by_condition(session, user_id=login_user.id)
    print('-------------------------- 我的餐车 --------------------------')
    print('序号\t\t菜品名称\t\t菜品单价\t\t数量 \t\t小计')
    if cart_items and len(cart_items) > 0:
        sum_price = 0
        for cart_item in cart_items:
            sum_price += cart_item.subtotal
            food = cart_item.food
            print(f'{food.id}\t\t{food.name}\t\t{food.price}\t\t{cart_item.amount}\t\t{cart_item.subtotal}')
        print('------------------------------------------------------------')
        print(f'总金额：{sum_price}')
        return sum_price, cart_items
    else:
        print('餐车里面空空如也，快去点餐吧~')
        return 0, []


def update_cart_item_amount(session, cs, login_user):
    is_continue = True
    while is_continue:
        food_id = input('请输入需要更改数量的菜品编号（输入0结束更改）：')
        if food_id == '0':
            return
        cart_item = cs.get_single_by_condition(session, user_id=login_user.id, food_id=food_id)
        if cart_item:
            try:
                amount = Decimal(input('请输入您要更改的数量（必须大于0）：'))
                if amount < 1:
                    print('数量必须大于0！')
                    continue
                old_amount = cart_item.amount
                cart_item.amount = amount
                cart_item.subtotal = cart_item.amount * cart_item.food.price
                cs.execute_commit(session)
                print(f'数量更改成功：原先为 {old_amount} ，现在为 {cart_item.amount}')
            except InvalidOperation:
                print('数量必须是数字！')
            except Exception as e:
                cs.execute_rollback(session, e)
                print('未知异常，请查看日志！')
        else:
            print('餐车中没有该菜品！')

def delete_cart_item(session, cs, login_user):
    is_continue = True
    while is_continue:
        food_id = input('请输入需要从餐车中删除的菜品编号（输入0结束删除）：')
        if food_id == '0':
            return
        cart_item = cs.get_single_by_condition(session, user_id=login_user.id, food_id=food_id)
        if cart_item:
            try:
                session.delete(cart_item)
                cs.execute_commit(session)
                print(f'餐品记录删除成功！')
            except Exception as e:
                cs.execute_rollback(session, e)
                print('未知异常，请查看日志！')
        else:
            print('餐车中没有该菜品或已被删除！')


def generate_order(session, cs, os, login_user, sum_price, cart_items):
    try:
        order_person = input('请输入接收人姓名：')
        order_address = input('请输入接收人地址：')
        order_phone = input('请输入接收人电话：')
        # 生成唯一的订单编号（固定10位）！
        order_no = generate_order_no(10)
        new_order = Order(
            order_no=order_no,
            user_id=login_user.id,
            order_person=order_person,
            order_phone=order_phone,
            order_address=order_address,
            sum_price=sum_price,
            status=ORDER_STATUS_UNPAID
        )
        session.add(new_order)
        # 将餐车信息补充到订单详情中去
        for cart_item in cart_items:
            order_details = OrderDetails(
                order_no=order_no,
                food_id=cart_item.food.id,
                amount=cart_item.amount,
                subtotal=cart_item.subtotal
            )
            session.add(order_details)
        # 当订单生成没问题时，我们就要清空购物车信息。
        deleted_items = cs.get_list_by_condition(session, user_id=login_user.id)
        for deleted_item in deleted_items:
            session.delete(deleted_item)
        os.execute_commit(session)
        print(f'订单创建成功，编号 {order_no}，请尽快完成支付！')
        return True
    except Exception as e:
        cs.execute_rollback(session, e)
        print('订单创建失败，请查看日志！')
        return False


def my_cart():
    with SessionManager.get_session() as session:
        current_user_id = login_manager.current_user_id
        cs = CartService()
        us = UserService()
        os = OrderService()
        login_user = us.get_by_id(session, current_user_id)
        if login_user:
            is_continue = True
            while is_continue:
                sum_price, cart_items = display_cart(session, cs, login_user)
                print('------------------------------------------------------------')
                print('1.更改点餐数量\t2.删除点餐记录\t3.开始下单\t0.返回上级')
                print('------------------------------------------------------------')
                item = input('请选择：')
                if item == '1':
                    update_cart_item_amount(session, cs, login_user)
                elif item == '2':
                    delete_cart_item(session, cs, login_user)
                elif item == '3':
                    is_success = generate_order(session, cs, os, login_user, sum_price, cart_items)
                    if is_success:
                        return
                elif item == '0':
                    print('返回上级')
                    is_continue = False
                else:
                    print('没有该选项！')
        else:
            print('请先登录后操作！')
