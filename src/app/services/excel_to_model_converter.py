from typing import Dict, List
from datetime import datetime
import traceback

import xlrd

from app.model.product_model import ProductModel
from app.model.retoure_model import RetoureModel
from app.services.excel_column import ExcelColumn


class ExcelToModelConverter:
    def __init__(self):
        self.CONVERT_ROWS_WITH_REPLACEMENT = "1-Gutschrift"
        self.CONVERT_ROWS_WITH_STATUS = "019-Ware wurde in den Bestandgebucht"
        self.datemode = -1
        self.headers = {}

    def convert(self, file) -> List[RetoureModel]:
        print("Start converting xls file to model")
        result = []

        book = xlrd.open_workbook(file_contents=file)
        self.datemode = book.datemode
        sheet = book.sheet_by_index(0)
        self.headers = self._get_headers(sheet.row(0))

        for row in range(1, sheet.nrows):
            try:
                self._parse_row(sheet.row(row), row, result)
            except Exception:
                print(
                    f"Skipping current row {row} because it could not be parsed: '{traceback.format_exc()}'"
                )
        return result

    def _get_headers(self, row: List[xlrd.sheet.Cell]) -> Dict[str, int]:
        cell_values = [cell.value for cell in row]
        print(f"All headers: '{str(cell_values)}'")

        headers = [column.value for column in ExcelColumn]
        columns = {
            cell.value: col
            for col, cell in [
                (i, cell) for i, cell in enumerate(row) if cell.value in headers
            ]
        }

        if len(columns) != len(headers):
            raise Exception(
                f"Unable to read headers of Excel file. Expected headers '{str(headers)}', but got '{str(cell_values)}'"
            )

        print(f"Mapping of columns was successful: '{str(columns)}'")
        return columns

    def _parse_row(
        self, row: List[xlrd.sheet.Cell], row_index: int, result: List[RetoureModel]
    ):
        if not self._should_convert_row(row):
            print(f"Skipping row {row_index}")
            return

        if self._retoure_already_exists_with(self._parse_return_number(row), result):
            model = result[len(result) - 1]
            self._add_product_to_(model, row)
        else:
            result.append(self._create_new_retoure(row))

    def _add_product_to_(self, model: RetoureModel, row: List[xlrd.sheet.Cell]):
        product_number = self._cell_value(row, ExcelColumn.PRODUCT_NUMBER)

        if model.contains_product(product_number):
            return

        return_number = self._parse_return_number(row)
        position = self._get_number_from(row, ExcelColumn.POSITION)
        amount_valid_restock = self._get_number_from(
            row, ExcelColumn.AMOUNT_VALID_RESTOCK
        )
        reason = self._parse_reason(row)

        product = ProductModel(product_number, position, amount_valid_restock, reason)
        model.add_product(product)

        print(
            f"Model with return_number '{return_number}' was already added. Added Product to existing model: '{repr(product)}'"
        )

    def _create_new_retoure(self, row: List[xlrd.sheet.Cell]) -> RetoureModel:
        return_number = self._parse_return_number(row)
        date = self._get_date_from(row)
        consignment_number = self._get_number_from(row, ExcelColumn.CONSIGNMENT_NUMBER)
        product_number = self._cell_value(row, ExcelColumn.PRODUCT_NUMBER)
        position = self._get_number_from(row, ExcelColumn.POSITION)
        amount_valid_restock = self._get_number_from(
            row, ExcelColumn.AMOUNT_VALID_RESTOCK
        )
        reason = self._parse_reason(row)

        model = RetoureModel(return_number, date, consignment_number)
        product = ProductModel(product_number, position, amount_valid_restock, reason)
        model.add_product(product)

        print(f"New model added: '{repr(model)}'")
        return model

    def _should_convert_row(self, row: List[xlrd.sheet.Cell]) -> bool:
        return (
            self._cell_value(row, ExcelColumn.REPLACEMENT)
            == self.CONVERT_ROWS_WITH_REPLACEMENT
            and self._cell_value(row, ExcelColumn.STATUS)
            == self.CONVERT_ROWS_WITH_STATUS
        )

    def _retoure_already_exists_with(
        self, return_number: str, result: List[RetoureModel]
    ) -> bool:
        return any(retoure.return_number == return_number for retoure in result)

    def _parse_return_number(self, row: List[xlrd.sheet.Cell]) -> str:
        return_number = self._cell_value(row, ExcelColumn.RETURN_NUMBER).split("-")
        return f"{return_number[0]}-{return_number[1]}"

    def _parse_reason(self, row: List[xlrd.sheet.Cell]) -> int:
        return int(self._cell_value(row, ExcelColumn.REASON)[1:3])

    def _get_date_from(self, row: List[xlrd.sheet.Cell]) -> datetime:
        return datetime.strptime(self._cell_value(row, ExcelColumn.DATE), "%d.%m.%Y")

    def _get_number_from(self, row: List[xlrd.sheet.Cell], column: ExcelColumn) -> int:
        return int(self._cell_value(row, column))

    def _cell_value(self, row: List[xlrd.sheet.Cell], column: ExcelColumn):
        return row[self.headers[column.value]].value
