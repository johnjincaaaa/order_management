from decimal import Decimal, InvalidOperation

from bll import login_manager, FoodService, UserService
from bll.cart_service import CartService
from dal import SessionManager
from models import Cart
from utils.constants import FOOD_STATUS_UP_TEXT, FOOD_STATUS_UP, FOOD_STATUS_DOWN_TEXT


def display_food_list(session, fs):
    food_list = fs.get_list(session)
    print('------------------------- 用户列表 ------------------------')
    print('编号\t\t菜品名称\t\t菜品单价\t\t规格\t\t状态')
    for food in food_list:
        status = FOOD_STATUS_UP_TEXT if food.status == FOOD_STATUS_UP else FOOD_STATUS_DOWN_TEXT
        print(f'{food.id}\t\t{food.name}\t\t{food.price}\t\t{food.specs}\t\t{status}')
    print('---------------------------------------------------------')


def to_ordering():
    with SessionManager.get_session() as session:
        current_user_id = login_manager.current_user_id
        cart_items = {}  # 接收点好的临时菜品 {'1': 3, '2': 5....}
        fs = FoodService()
        cs = CartService()
        us = UserService()
        login_user = us.get_by_id(session, current_user_id)
        if login_user:
            display_food_list(session, fs)
            while True:
                try:
                    food_id = int(input('请选择菜品（输入0结束点餐）：'))
                    if food_id == 0:
                        break
                    food = fs.get_single_by_condition(session, id=food_id, status=FOOD_STATUS_UP)
                    if food:
                        """ 如果认为这里写整数，也没问题，根据需求来定！ """
                        amount = Decimal(input(f'请输入要购买的 {food.name} 数量：'))
                        if amount <= 0:
                            print('数量必须大于0！')
                            continue
                        if food_id in cart_items:
                            """ cart_items曾经记录过这个food_id，执行累加 """
                            cart_items[food_id] += amount
                        else:
                            """ 新建一个新的临时购物车项！"""
                            cart_items[food_id] = amount
                        print('点餐成功！')
                    else:
                        print('没有该菜品或菜品已下架！')
                except ValueError:
                    print('菜品编号只能是整数！')
                except InvalidOperation:
                    print('数量只能是数字！')

            if cart_items:
                print('\n您选择的菜品如下：')
                print('-------------------------------------------')
                total_price = 0
                for food_id, amount in cart_items.items():
                    food = fs.get_by_id(session, food_id)
                    subtotal = amount * food.price
                    total_price += subtotal
                    print(f'{food.name}：数量 {amount}，小计 {subtotal}')
                print('-------------------------------------------')
                print(f'总金额：{total_price}')
                print('-------------------------------------------')
                confirm = input('加入购物车？（输入Y确定，其它取消）：')
                if confirm.upper() == 'Y':
                    # 将数据存入购物车表！
                    for food_id, amount in cart_items.items():
                        # 判定购物车里面是否已经购买过这些菜品（user_id, food_id）
                        existing_cart_item = cs.get_single_by_condition(
                            session,
                            food_id=food_id,
                            user_id=login_user.id,
                        )
                        if existing_cart_item:
                            # 累加（UPDATE）
                            existing_cart_item.amount += amount
                            existing_cart_item.subtotal += amount * existing_cart_item.food.price
                            result = cs.update(session, existing_cart_item)
                        else:
                            # 新增（INSERT）
                            food = fs.get_by_id(session, food_id)
                            new_cart_item = Cart(
                                user_id=login_user.id,
                                food_id=food_id,
                                amount=amount,
                                subtotal=amount * food.price,
                            )
                            result = cs.create(session, new_cart_item)
                    if result:
                        print('菜品已成功加入餐车，您可以前往餐车查看或继续点餐！')
                    else:
                        print('菜品加入餐车失败，请查看日志！')
                else:
                    print('已取消加入餐车！')
        else:
            print('请先登录后操作！')