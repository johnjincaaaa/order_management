import uuid

from utils.constants import *


def generate_order_no(size):
    return str(uuid.uuid4()).replace('-', '')[:size]


def to_order_status_text(order_status):
    if order_status == ORDER_STATUS_UNPAID:
        return ORDER_STATUS_UNPAID_TEXT
    elif order_status == ORDER_STATUS_PAID:
        return ORDER_STATUS_PAID_TEXT
    elif order_status == ORDER_STATUS_SHIPPED:
        return ORDER_STATUS_SHIPPED_TEXT
    elif order_status == ORDER_STATUS_PENDING_RECEIPT:
        return ORDER_STATUS_PENDING_RECEIPT_TEXT
    elif order_status == ORDER_STATUS_RECEIVED:
        return ORDER_STATUS_RECEIVED_TEXT
    elif order_status == ORDER_STATUS_REFUNDING:
        return ORDER_STATUS_REFUNDING_TEXT
    elif order_status == ORDER_STATUS_REFUNDED:
        return ORDER_STATUS_REFUNDED_TEXT
    elif order_status == ORDER_STATUS_REFUND_FAILED:
        return ORDER_STATUS_REFUND_FAILED_TEXT
    else:
        return '未知状态'


def to_refund_status_text(refund_status):
    if refund_status == REVIEW_STATUS_UNCHECKED:
        return REVIEW_STATUS_UNCHECKED_TEXT
    elif refund_status == REVIEW_STATUS_CHECKED_SUCCESS:
        return REVIEW_STATUS_CHECKED_SUCCESS_TEXT
    elif refund_status == REVIEW_STATUS_CHECKED_FAILED:
        return REVIEW_STATUS_CHECKED_FAILED_TEXT
    else:
        return '未知状态'