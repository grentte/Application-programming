import json
from typing import Optional
from Payment import Payment, PaymentNotFoundError


class PaymentExistsError(Exception):
    pass


class PaymentJSONHandler:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def create(self, payment: Payment):
        payment_data = {
            "payment_id": payment.payment_id,
            "order_id": payment.order.order_id,
            "amount": payment.amount,
            "payment_method": payment.payment_method,
            "status": payment.status
        }

        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"payments": []}

        for existing_payment in data.get("payments", []):
            if existing_payment["payment_id"] == payment.payment_id:
                raise PaymentExistsError(f"Payment with ID '{payment.payment_id}' already exists.")

        data["payments"].append(payment_data)

        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

    def read(self, payment_id: int) -> Optional[Payment]:
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            for payment_data in data.get("payments", []):
                if payment_data["payment_id"] == payment_id:
                    # Assuming order object is available in another context or can be reconstructed.
                    order = None  # You need to fetch or reconstruct the order from its ID.
                    return Payment(payment_data["payment_id"], order, payment_data["amount"],
                                   payment_data["payment_method"])
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def update(self, payment_id: int, amount: Optional[int] = None, payment_method: Optional[str] = None,
               status: Optional[str] = None):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)

            for payment_data in data.get("payments", []):
                if payment_data["payment_id"] == payment_id:
                    if amount is not None:
                        payment_data["amount"] = amount
                    if payment_method is not None:
                        payment_data["payment_method"] = payment_method
                    if status is not None:
                        payment_data["status"] = status

                    with open(self.filepath, "w") as file:
                        json.dump(data, file, indent=4)
                    return True
            raise PaymentNotFoundError(payment_id)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return False
        except PaymentNotFoundError as e:
            print(e)
            return False

    def delete(self, payment_id: int):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            original_length = len(data.get("payments", []))
            data["payments"] = [payment for payment in data.get("payments", []) if payment["payment_id"] != payment_id]

            if len(data["payments"]) == original_length:
                raise PaymentNotFoundError(payment_id)

            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        except PaymentNotFoundError as e:
            print(e)
            return False

    def get_all_payments(self):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            return [Payment(payment_data["payment_id"], None, payment_data["amount"], payment_data["payment_method"])
                    for payment_data in data.get("payments", [])]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_payments_by_order(self, order_id: int):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            payments = [
                Payment(payment_data["payment_id"], None, payment_data["amount"], payment_data["payment_method"])
                for payment_data in data.get("payments", [])
                if payment_data["order_id"] == order_id
            ]
            if not payments:
                raise ValueError(f"No payments found for order ID {order_id}.")
            return payments
        except (FileNotFoundError, json.JSONDecodeError):
            return []
