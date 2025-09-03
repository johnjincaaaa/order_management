from decimal import Decimal, InvalidOperation
from bll import login_manager, OrderService, UserService
from bll.order_service import RefundService
from dal import SessionManager
from models.order import RefundApplication
from utils.constants import ORDER_STATUS_UNPAID, ORDER_STATUS_PAID, ORDER_STATUS_RECEIVED, ORDER_STATUS_REFUND_FAILED, \
    ORDER_STATUS_SHIPPED, ORDER_STATUS_PENDING_RECEIPT, ORDER_STATUS_REFUNDING, ORDER_STATUS_REFUNDED, \
    REVIEW_STATUS_UNCHECKED
from utils.tools import to_order_status_text, to_refund_status_text


def display_orders(session, os, login_user):
    orders = os.get_list_by_condition(session, user_id=login_user.id)
    if orders and len(orders) > 0:
        print('-------------------------------------- 我的订单 --------------------------------------')
        print('订单编号\t\t\t下单人\t\t订单金额\t\t订单状态\t\t下单时间')
        for order in orders:
            print(f'{order.order_no}\t\t{order.order_person} \t\t{order.sum_price}'
                  f'\t\t{to_order_status_text(order.status)}\t\t{order.create_at}')
        print('------------------------------------------------------------------------------------')
    else:
        print('当前没有任何订单信息')
        print('------------------------------------------------------------------------------------')


def refund_apply(session, rs, order, login_user):
    confirm = input('正在申请退款，请问是否继续（Y/N）：')
    if confirm.upper() == 'Y':
        try:
            amount = Decimal(input('请输入要退款的金额（大于0且小于订单总金额）：'))
            if amount > order.sum_price:
                print('退款金额不能大于订单总金额！')
                return
            reason = input('请输入退款原因：')
            new_refund = RefundApplication(
                order_no=order.order_no,
                user_id=login_user.id,
                refund_amount=amount,
                refund_reason=reason,
                status=REVIEW_STATUS_UNCHECKED
            )
            refund = rs.create(session, new_refund)
            if refund:
                print('退款申请单创建成功，请等待商家审核！')
                order.status = ORDER_STATUS_REFUNDING
                rs.execute_commit(session)
            else:
                print('退款申请单创建失败，请查看日志！')
                rs.execute_rollback(session)
        except InvalidOperation:
            print('退款金额必须是数字！')
        except Exception as e:
            print('未知错误，请查看日志！')
            rs.execute_rollback(session, e)
    else:
        print('用户取消了操作！')
        return

def sign_order(session, os, order):
    try:
        order.status = ORDER_STATUS_RECEIVED
        os.execute_commit(session)
    except Exception as e:
        print('未知错误，请查看日志！')
        os.execute_rollback(session, e)


def pay_order(session, os,  order, login_user):
    confirm = input('正在支付订单，请问是否继续（Y/N）：')
    if confirm.upper() == 'Y':
        if login_user.balance >= order.sum_price:
            try:
                login_user.balance -= order.sum_price
                order.status = ORDER_STATUS_PAID
                os.execute_commit(session)
                print('订单支付成功！')
            except Exception as e:
                os.execute_rollback(session, e)
                print('订单支付失败，请查看日志！')
        else:
            print('用户余额不足，请前往充值！')


def cancel_order(session, os, order):
    is_continue = input('正在取消订单，请问是否继续（Y/N）：')
    if is_continue.upper() == 'Y':
        try:
            # 更新订单状态
            session.delete(order)
            os.execute_commit(session)
            print('订单取消成功！')
        except Exception as e:
            os.execute_rollback(session, e)
            print('订单取消失败，请查看日志！')
    else:
        print('用户取消了操作！')


def to_order_details(session, os, rs, order, login_user):
    is_continue = True
    while is_continue:
        print('-------------------------------------------------------')
        print(f'{order.order_no}（{to_order_status_text(order.status)}）\t\t\t{order.create_at}')
        print('-------------------------------------------------------')
        print('序号\t\t菜品名称\t\t菜品单价\t\t菜品数量\t\t小计')
        for index, details in enumerate(order.order_details, 1):
            food = details.food
            print(f'{index}\t\t{food.name}\t\t{food.price}\t\t{details.amount}\t\t{details.subtotal}')
        print(f'总计\t\t\t\t\t\t\t\t\t\t\t{order.sum_price}')
        print('-------------------------------------------------------')
        print(f'下单人：{order.order_person}\t\t\t\t\t联系方式：{order.order_phone}')
        rs_list = order.refund_applications
        if rs_list and len(rs_list) > 0:
            print('-------------------------------------------------------')
            print('退款申请记录：')
            for refund in rs_list:
                print('-------------------------------------------------------')
                print(f'{refund.create_at}\t\t\t\t\t\t{to_refund_status_text(refund.status)}')
                print('-------------------------------------------------------')
                print(f'申请原因：{refund.refund_reason}\n审核意见：{refund.refund_response or '暂无'}')
                print('-------------------------------------------------------')
        else:
            print('-------------------------------------------------------')
        # 当订单处于未支付状态时（支付订单、取消订单、返回订单列表）
        if order.status == ORDER_STATUS_UNPAID:
            print('1.支付订单\t2.取消订单\t0.返回订单列表')
            print('-------------------------------------------------------')
            item = input('请选择：')
            if item == '0':
                is_continue = False
            elif item == '1':
                pay_order(session, os, order, login_user)
            elif item == '2':
                cancel_order(session, os, order)
            else:
                print('没有该选项！')
        # 当订单处于已支付、已签收、退款失败时候，可以申请退款。
        elif order.status in (ORDER_STATUS_PAID, ORDER_STATUS_RECEIVED, ORDER_STATUS_REFUND_FAILED):
            print('1.申请退款\t0.返回列表页')
            print('-------------------------------------------------------')
            item = input('请选择：')
            if item == '0':
                is_continue = False
            elif item == '1':
                refund_apply(session, rs, order, login_user)
            else:
                print('没有该选项！')
        # 当订单处于已发货、待签收
        elif order.status in (ORDER_STATUS_SHIPPED, ORDER_STATUS_PENDING_RECEIPT):
            print('1.申请退款\t2.签收订单\t0.返回列表页')
            print('-------------------------------------------------------')
            item = input('请选择：')
            if item == '0':
                is_continue = False
            elif item == '1':
                refund_apply(session, rs, order, login_user)
            elif item == '2':
                sign_order(session, os, order)
            else:
                print('没有该选项！')
        elif order.status in (ORDER_STATUS_REFUNDING, ORDER_STATUS_REFUNDED):
            if order.status == ORDER_STATUS_REFUNDING:
                msg = '当前正在审核您的退款申请，请耐心等待（输入0返回上级）'
            else:
                msg = '当前退款已完成！（输入0返回上级）'
            print(msg)
            print('-------------------------------------------------------')
            item = input('请选择：')
            if item == '0':
                is_continue = False
            else:
                print('没有该选项！')

def my_order():
    with SessionManager.get_session() as session:
        current_user_id = login_manager.current_user_id
        us = UserService()
        os = OrderService()
        rs = RefundService()
        login_user = us.get_by_id(session, current_user_id)
        if login_user:
            is_continue = True
            while is_continue:
                display_orders(session, os, login_user)
                order_no = input('请选择你要操作的订单编号（输入0返回上级）：')
                if order_no == '0':
                    is_continue = False
                    continue
                order = os.get_single_by_condition(session, order_no=order_no)
                if order:
                    to_order_details(session, os, rs, order, login_user)
                else:
                    print('你选择的订单不存在！')
        else:
            print('请先登录后操作！')