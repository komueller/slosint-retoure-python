from app.model.product_model import ProductModel


class RetoureModel:
    def __init__(self, return_number: str, date, consignment_number: int):
        self.return_number = return_number
        self.date = date
        self.consignment_number = consignment_number
        self.products = {}

    def add_product(self, product: ProductModel):
        self.products[product.product_number] = product

    def contains_product(self, product_number: str) -> bool:
        return product_number in self.products.keys()

    def __repr__(self) -> str:
        return f"RetoureModel(return_number='{self.return_number}', date='{str(self.date)}', consignment_number='{self.consignment_number}', products='{repr(self.products)}')"
