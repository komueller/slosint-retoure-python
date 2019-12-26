from enum import Enum


class ExcelColumn(Enum):
    RETURN_NUMBER = "Vorgang"
    DATE = "Dt.REingang"
    CONSIGNMENT_NUMBER = "Auftrag (E)"
    PRODUCT_NUMBER = "Artikel (E)"
    POSITION = "Pos."
    AMOUNT_VALID_RESTOCK = "RE-Menge"
    REASON = "RE-Grund"
    REPLACEMENT = "GS / Umtausch"
    STATUS = "RE-Status"
