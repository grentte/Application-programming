class Payment:
    def __init__(self, payment_id, order, amount, payment_method):
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
    pass

