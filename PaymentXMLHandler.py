import xml.etree.ElementTree as ET
from Order import Order
from Payment import Payment, PaymentNotFoundError, InvalidPaymentStatusError


class PaymentXMLHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def _load_payments(self):
        try:
            tree = ET.parse(self.filepath)
            return tree.getroot()
        except (FileNotFoundError, ET.ParseError):
            root = ET.Element("payments")
            tree = ET.ElementTree(root)
            tree.write(self.filepath)
            return root

    def _save_payments(self, root):
        tree = ET.ElementTree(root)
        tree.write(self.filepath)

    def create_payment(self, order: Order, amount: int, payment_method: str):
        if order.total_amount != amount:
            raise ValueError(f"Payment amount {amount} does not match order total {order.total_amount}.")

        root = self._load_payments()

        payment_id = len(root.findall("payment")) + 1
        payment = Payment(payment_id, order, amount, payment_method)

        # Create new payment XML element
        payment_element = ET.SubElement(root, "payment")
        ET.SubElement(payment_element, "payment_id").text = str(payment.payment_id)
        ET.SubElement(payment_element, "order_id").text = str(order.order_id)
        ET.SubElement(payment_element, "amount").text = str(payment.amount)
        ET.SubElement(payment_element, "payment_method").text = payment.payment_method
        ET.SubElement(payment_element, "status").text = payment.status

        self._save_payments(root)
        return payment

    def read_payment(self, payment_id: int):
        root = self._load_payments()

        for payment_element in root.findall("payment"):
            if int(payment_element.find("payment_id").text) == payment_id:
                order_id = int(payment_element.find("order_id").text)
                amount = int(payment_element.find("amount").text)
                payment_method = payment_element.find("payment_method").text
                status = payment_element.find("status").text

                # Assuming the Order class is already defined and the order exists
                order = Order(order_id, 1, None, None, "")  # You'd need to retrieve the actual Order instance
                payment = Payment(payment_id, order, amount, payment_method)
                payment.status = status
                return payment

        raise PaymentNotFoundError(payment_id)

    def update_payment(self, payment_id: int, amount: int = None, payment_method: str = None):
        root = self._load_payments()

        for payment_element in root.findall("payment"):
            if int(payment_element.find("payment_id").text) == payment_id:
                if amount is not None:
                    if amount <= 0:
                        raise ValueError("Payment amount must be greater than zero.")
                    payment_element.find("amount").text = str(amount)
                if payment_method is not None:
                    payment_element.find("payment_method").text = payment_method

                self._save_payments(root)
                return self.read_payment(payment_id)

        raise PaymentNotFoundError(payment_id)

    def delete_payment(self, payment_id: int):
        root = self._load_payments()

        for payment_element in root.findall("payment"):
            if int(payment_element.find("payment_id").text) == payment_id:
                root.remove(payment_element)
                self._save_payments(root)
                return f"Payment {payment_id} deleted successfully."

        raise PaymentNotFoundError(payment_id)

    def get_all_payments(self):
        root = self._load_payments()
        payments = []
        for payment_element in root.findall("payment"):
            payment_id = int(payment_element.find("payment_id").text)
            payments.append(self.read_payment(payment_id))
        return payments

    def get_payments_by_order(self, order_id: int):
        root = self._load_payments()
        payments = []
        for payment_element in root.findall("payment"):
            if int(payment_element.find("order_id").text) == order_id:
                payment_id = int(payment_element.find("payment_id").text)
                payments.append(self.read_payment(payment_id))
        if not payments:
            raise ValueError(f"No payments found for order ID {order_id}.")
        return payments
