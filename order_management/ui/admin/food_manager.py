from decimal import Decimal, InvalidOperation
from bll import FoodService
from dal import SessionManager
from models import Food
from utils.constants import FOOD_STATUS_UP, FOOD_STATUS_DOWN_TEXT, FOOD_STATUS_UP_TEXT, FOOD_STATUS_DOWN


def display_food(session, fs):
    food_list = fs.get_list(session)
    if food_list and len(food_list) > 0:
        print('------------------------- 菜品列表 ------------------------')
        print('编号\t\t菜品名称\t\t菜品单价\t\t规格\t\t状态')
        for food in food_list:
            status = FOOD_STATUS_UP_TEXT if food.status == FOOD_STATUS_UP else FOOD_STATUS_DOWN_TEXT
            print(f'{food.id}\t\t{food.name}\t\t{food.price}\t\t{food.specs}\t\t{status}')
        print('---------------------------------------------------------')
        print('1.添加菜品\t2.编辑菜品\t3.下架菜品\t4.上架菜品\t0.返回上级')
        print('---------------------------------------------------------')
    else:
        print('当前没有任何菜品！')
        print('---------------------------------------------------------')

def add_food(session, fs):
    try:
        name = input('请输入菜品名称：')
        price = Decimal(input('请输入菜品价格：'))
        specs = input('请输入菜品规格：')
        new_food = Food(name=name, price=price, specs=specs)
        result = fs.create(session, new_food)
        if result:
            print('菜品添加成功！')
        else:
            print('菜品添加失败，请查询日志信息！')
    except InvalidOperation:
        print('菜品价格必须是数字！')
    except Exception as e:
        print('未知异常，请查询日志信息')
        fs.execute_rollback(session, e)


def edit_food(session, fs):
    try:
        food_id = input('请输入待修改的菜品编号：')
        food = fs.get_by_id(session, food_id)
        if food:
            new_price = input('请输入新的菜品价格（留空则不修改）：')
            new_specs = input('请输入新的菜品规格（留空则不修改）：')
            if new_price:
                food.price = new_price
            if new_specs:
                food.specs = new_specs
            result = fs.update(session, food)
            if result:
                print('菜品修改成功')
            else:
                print('菜品修改失败，请查看日志！')
        else:
            print('你选择的菜品不存在！')
    except ValueError:
        print('菜品编号必须是整数！')
    except InvalidOperation:
        print('菜品价格必须是数字！')
    except Exception as e:
        print('未知异常，请查询日志信息')
        fs.execute_rollback(session, e)


def down_food(session, fs):
    try:
        food_id = input('请输入待下架的菜品编号：')
        food = fs.get_by_id(session, food_id)
        if food:
            if food.status == FOOD_STATUS_DOWN:
                print('该菜品已处于下架状态！')
                return
            food.status = FOOD_STATUS_DOWN
            result = fs.update(session, food)
            if result:
                print('菜品下架成功')
            else:
                print('菜品下架失败，请查看日志！')
        else:
            print('你选择的菜品不存在！')
    except ValueError:
        print('菜品编号必须是整数！')
    except Exception as e:
        print('未知异常，请查询日志信息')
        fs.execute_rollback(session, e)


def up_food(session, fs):
    try:
        food_id = input('请输入待上架的菜品编号：')
        food = fs.get_by_id(session, food_id)
        if food:
            if food.status == FOOD_STATUS_UP:
                print('该菜品已处于上架状态！')
                return
            food.status = FOOD_STATUS_UP
            result = fs.update(session, food)
            if result:
                print('菜品上架成功')
            else:
                print('菜品上架失败，请查看日志！')
        else:
            print('你选择的菜品不存在！')
    except ValueError:
        print('菜品编号必须是整数！')
    except Exception as e:
        print('未知异常，请查询日志信息')
        fs.execute_rollback(session, e)


def food_manager():
    fs = FoodService()
    with SessionManager.get_session() as session:
        is_continue = True
        while is_continue:
            display_food(session, fs)
            item = input('请选择：')
            if item == '1':
                add_food(session, fs)
            elif item == '2':
                edit_food(session, fs)
            elif item == '3':
                down_food(session, fs)
            elif item == '4':
                up_food(session, fs)
            elif item == '0':
                is_continue = False
            else:
                print('没有该选项！')