from typing import List
from xml.etree import ElementTree

from ..model.retoure_model import RetoureModel


class ModelToXmlConverter:
    def convert(self, models: List[RetoureModel]) -> List[str]:
        return [self._convert_one_model(model) for model in models]

    def _convert_one_model(self, model: RetoureModel) -> str:
        print(
            f"Start converting RetoureModel with return_number '{model.return_number}' to xml"
        )

        root = ElementTree.Element("returns")

        return_number = ElementTree.SubElement(
            root, "return", number=model.return_number
        )
        ElementTree.SubElement(
            return_number, "date", format="YYYY-MM-DD"
        ).text = model.date.strftime("%Y-%m-%d")

        ElementTree.SubElement(return_number, "channel").text = "B2C"

        consignment_number = ElementTree.SubElement(
            return_number, "consignment", number=str(model.consignment_number)
        )
        products = ElementTree.SubElement(consignment_number, "products")

        for product in model.products.values():
            product_e = ElementTree.SubElement(
                products, "product", number=product.product_number
            )
            ElementTree.SubElement(product_e, "position").text = str(product.position)

            amount = ElementTree.SubElement(product_e, "amount")
            valid = ElementTree.SubElement(amount, "valid")
            ElementTree.SubElement(valid, "restock").text = str(product.amount_valid_restock)
            ElementTree.SubElement(valid, "scrap").text = "0"
            ElementTree.SubElement(amount, "invalid").text = "0"
            ElementTree.SubElement(amount, "internal").text = "0"
            ElementTree.SubElement(product_e, "reason").text = str(product.reason)

        return ElementTree.tostring(root, encoding="utf-8", xml_declaration=True).decode()
