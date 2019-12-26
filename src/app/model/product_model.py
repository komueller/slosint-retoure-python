class ProductModel:
    def __init__(
        self, product_number: str, position: int, amount_valid_restock: int, reason: int
    ):
        self.product_number = product_number
        self.position = position
        self.amount_valid_restock = amount_valid_restock
        self.reason = reason

    def __repr__(self) -> str:
        return f"ProductModel(product_number='{self.product_number}', position='{self.position}', amount_valid_restock='{self.amount_valid_restock}', reason='{self.reason}')"
