from Order import Order


class InvalidPaymentStatusError(Exception):
    def __init__(self, payment_id, current_status, attempted_action):
        super().__init__(f"Cannot perform '{attempted_action}' on payment {payment_id} with status '{current_status}'.")


class PaymentNotFoundError(Exception):
    def __init__(self, payment_id):
        super().__init__(f"Payment with ID {payment_id} not found.")


class Payment:
    def __init__(self, payment_id: int, order: Order, amount: int, payment_method: str):
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")
        if not isinstance(order, Order):
            raise TypeError("Invalid order. Must be an instance of the Order class.")
        if not payment_method:
            raise ValueError("Payment method must be specified.")
        self.payment_id = payment_id
        self.order = order
        self.amount = amount
        self.payment_method = payment_method
        self.status = "Unpaid"

    def __repr__(self):
        return (f"Payment(payment_id={self.payment_id}, amount={self.amount}, "
                f"payment_method='{self.payment_method}', status='{self.status}')")

    def process_payment(self):
        if self.order.status != "Placed":
            raise InvalidPaymentStatusError(self.payment_id, self.status, "process")
        if self.status == "Paid":
            raise InvalidPaymentStatusError(self.payment_id, self.status, "process again")
        self.status = "Paid"
        return f"Payment {self.payment_id} processed successfully."

    def refund_payment(self):
        if self.status != "Paid":
            raise InvalidPaymentStatusError(self.payment_id, self.status, "refund")
        self.status = "Refunded"
        return f"Payment {self.payment_id} refunded successfully."


class PaymentManager:
    def __init__(self):
        self.payments = {}
        self.current_payment_id = 1

    def create_payment(self, order: Order, amount: int, payment_method: str):
        if order.total_amount != amount:
            raise ValueError(f"Payment amount {amount} does not match order total {order.total_amount}.")
        payment = Payment(self.current_payment_id, order, amount, payment_method)
        self.payments[self.current_payment_id] = payment
        self.current_payment_id += 1
        return payment

    def read_payment(self, payment_id: int):
        payment = self.payments.get(payment_id)
        if not payment:
            raise PaymentNotFoundError(payment_id)
        return payment

    def update_payment(self, payment_id: int, amount: int = None, payment_method: str = None):
        try:
            payment = self.read_payment(payment_id)
        except PaymentNotFoundError as e:
            return str(e)

        if amount is not None:
            if amount <= 0:
                raise ValueError("Payment amount must be greater than zero.")
            payment.amount = amount
        if payment_method is not None:
            payment.payment_method = payment_method
        return payment

    def delete_payment(self, payment_id: int):
        try:
            payment = self.read_payment(payment_id)
            del self.payments[payment_id]
            return f"Payment {payment_id} deleted successfully."
        except PaymentNotFoundError as e:
            return str(e)

    def get_all_payments(self):
        return list(self.payments.values())

    def get_payments_by_order(self, order_id: int):
        payments = [payment for payment in self.payments.values() if payment.order.order_id == order_id]
        if not payments:
            raise ValueError(f"No payments found for order ID {order_id}.")
        return payments
