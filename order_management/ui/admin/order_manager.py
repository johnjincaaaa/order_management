from bll import OrderService
from bll.order_service import RefundService
from dal import SessionManager
from utils.constants import ORDER_STATUS_REFUND_FAILED, ORDER_STATUS_PAID, ORDER_STATUS_SHIPPED, ORDER_STATUS_REFUNDED, \
    REVIEW_STATUS_UNCHECKED, REVIEW_STATUS_CHECKED_SUCCESS, REVIEW_STATUS_CHECKED_FAILED
from utils.tools import to_order_status_text, to_refund_status_text


def display_order(session, os):
    orders = os.get_list(session)
    if orders and len(orders) > 0:
        print('-------------------------------------- 订单列表 ------------------------------------------')
        print('订单编号\t\t\t下单人\t\t订单金额\t\t订单状态\t\t所属用户\t\t下单时间')
        for order in orders:
            print(f'{order.order_no}\t\t{order.order_person} \t\t{order.sum_price}'
                  f'\t\t{to_order_status_text(order.status)}\t\t{order.user.username}\t\t{order.create_at}')
        print('------------------------------------------------------------------------------------------')
        print('1.订单发货\t2.退款审核\t3.查看详情\t0.返回上级')
        print('------------------------------------------------------------------------------------------')
    else:
        print('当前没有任何订单！')
        print('------------------------------------------------------------------------------------------')

def order_sendout(session, os):
    try:
        order_no = input('请输入要发货的订单编号：')
        order = os.get_single_by_condition(session, order_no=order_no)
        if order:
            if order.status == ORDER_STATUS_PAID:
                order.status = ORDER_STATUS_SHIPPED
                os.execute_commit(session)
                print('订单发货成功！')
            else:
                print('该订单未支付或已发货！')
        else:
            print('没有该订单！')
    except Exception as e:
        os.execute_rollback(session, e)
        print('发货失败，请查看日志！')

def refund_examine(session, os, rs):
    try:
        order_no = input('请输入要查看的订单编号：')
        order = os.get_single_by_condition(session, order_no=order_no)
        if order:
            user = order.user
            order_details = order.order_details
            refund = rs.get_single_by_condition(session, order_no=order_no, status=REVIEW_STATUS_UNCHECKED)
            if refund:
                print('---------------------------------------------------')
                print("退款申请审核信息：")
                print(f"用户信息：用户名 - {user.username}，用户编号 - {user.id}")
                print(f"订单信息：订单编号 - {order.order_no}，订单金额 - {order.sum_price}")
                print("订单详情：")
                for detail in order_details:
                    food = detail.food
                    print(f"菜品名称：{food.name}，数量：{detail.amount}，小计：{detail.subtotal}")
                print(f"退款原因：{refund.refund_reason}")
                print(f"当前退款申请状态：{to_refund_status_text(refund.status)}")
                confirm = input("是否通过审核？（输入Y确认通过，其他则不通过）：")
                if confirm.upper() == 'Y':
                    response = input("请输入审核意见：")
                    refund.refund_response = response
                    user.balance += refund.refund_amount
                    refund.status = REVIEW_STATUS_CHECKED_SUCCESS
                    order.status = ORDER_STATUS_REFUNDED
                    rs.execute_commit(session)
                    print("审核完成，已通过！")
                else:
                    response = input("请输入审核不通过的原因：")
                    refund.refund_response = response
                    refund.status = REVIEW_STATUS_CHECKED_FAILED
                    order.status = ORDER_STATUS_REFUND_FAILED
                    rs.execute_commit(session)
                    print("审核完成，未通过！")
            else:
                print('该订单没有收到退款申请或已退款！')
        else:
            print('没有该订单！')
        print('---------------------------------------------------')
    except Exception as e:
        print('操作错误，请查看日志！')
        rs.execute_rollback(session, e)

def query_details(session, os):
    order_no = input('请输入要查看的订单编号：')
    order = os.get_single_by_condition(session, order_no=order_no)
    if order:
        print('---------------------------------------------------')
        print(f'{order.order_no}（{to_order_status_text(order.status)}）\t\t\t{order.create_at}')
        print('---------------------------------------------------')
        print('序号\t\t菜品名称\t\t菜品单价\t\t菜品数量\t\t小计')
        for index, details in enumerate(order.order_details, 1):
            food = details.food
            print(f'{index}\t\t{food.name}\t\t{food.price}\t\t{details.amount}\t\t{details.subtotal}')
        print('---------------------------------------------------')
        print(f'下单人：{order.order_person}\t\t\t\t\t联系方式：{order.order_phone}')
        print('---------------------------------------------------')
        if order.status in (ORDER_STATUS_REFUND_FAILED, ORDER_STATUS_REFUNDED):
            print('退款情况：')
            print('---------------------------------------------------')
    else:
        print('没有该订单！')
    print('---------------------------------------------------')


def order_manager():
    os = OrderService()
    rs = RefundService()
    with SessionManager.get_session() as session:
        is_continue = True
        while is_continue:
            display_order(session, os)
            item = input('请选择：')
            if item == '1':
                order_sendout(session, os)
            elif item == '2':
                refund_examine(session, os, rs)
            elif item == '3':
                query_details(session, os)
            elif item == '0':
                is_continue = False
            else:
                print('没有这个选项！')