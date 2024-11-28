from Order import Order


class Payment:
    def __init__(self, payment_id: int, order: Order, amount: int, payment_method: str):
        self.payment_id = payment_id
        self.order = order
        self.amount = amount
        self.payment_method = payment_method
        self.status = "Unpaid"

    def __repr__(self):
        return f"Payment(payment_id={self.payment_id}, amount={self.amount}, status='{self.status}')"

    def process_payment(self):
        if self.order.status == "Placed":
            self.status = "Paid"
            return f"Payment {self.payment_id} processed successfully!"
        return f"Order {self.order.order_id} is not placed. Cannot process payment."

    def refund_payment(self):
        if self.status == "Paid":
            self.status = "Refunded"
            return f"Payment {self.payment_id} refunded."
        return f"Payment {self.payment_id} is not completed. Cannot refund."


class PaymentManager:
    def __init__(self):
        self.payments = {}  # Словарь для хранения платежей, где ключ - payment_id, значение - объект Payment
        self.current_payment_id = 1

    def create_payment(self, order: Order, amount: int, payment_method: str):
        payment = Payment(self.current_payment_id, order, amount, payment_method)
        self.payments[self.current_payment_id] = payment
        self.current_payment_id += 1
        return payment

    def read_payment(self, payment_id: int):
        return self.payments.get(payment_id, "Payment not found.")

    def update_payment(self, payment_id: int, amount: int = None, payment_method: str = None):
        payment = self.payments.get(payment_id)
        if payment:
            if amount is not None:
                payment.amount = amount
            if payment_method is not None:
                payment.payment_method = payment_method
            return payment
        return "Payment not found."

    def delete_payment(self, payment_id: int):
        payment = self.payments.get(payment_id)
        if payment:
            del self.payments[payment_id]
            return f"Payment {payment_id} deleted."
        return "Payment not found."

    def get_all_payments(self):
        return list(self.payments.values())

    def get_payments_by_order(self, order_id: int):
        return [payment for payment in self.payments.values() if payment.order.order_id == order_id]
