import re
from pathlib import Path

from openpyxl import load_workbook

class ParsingItem:
    def __init__(self) -> None:
        self.product = []
        self.body = []
        
    def set_product(self, key):
        self.product = key

    def insert_nested(self, row):
        self.body.append(row)

    def to_dict(self):
        def parse_product(row: list):
            batch, manuf_date = None, None
            # >>(A001)<< от >>(02.05.2022)<<
            if match := re.search(r'([A-Z]?\d{1,3})\s*от\s*(\d{2}.\d{2}.\d{4})', row[1]):
                batch, manuf_date = match.groups()

            roszdrav_name = row[2]
            roszdrav_register = row[3]
            if roszdrav_name and roszdrav_register:
                if match := re.search(r'(\d{1,4}\/\d*)', roszdrav_register):
                    roszdrav_register = match.group()

            return {
                'nomenclature_name': row[0],
                'batch': batch,
                'manuf_date': manuf_date,
                'roszdrav_name': roszdrav_name,
                'roszdrav_register': roszdrav_register,
            }

        def parse_body(row: list):
            number, date = None, None
            # Расходная накладная >>(178)<< от >>(02.05.2023)<<
            if match := re.search(r'(\d{1,4}) от (\d{2}.\d{2}.\d{4})', row[0]):
                number, date = match.groups()

            return {
                'doc_number': number,
                'doc_date': date,
                'count': row[4],
            }
        return {
            'product': parse_product(self.product),
            'docs_list': [parse_body(row) for row in self.body]
        } if self.product else {}


class Parser:
    def __init__(self) -> None:
        self.sheet = self.load_sheet()

    def load_sheet(self):
        base_path = Path('./.data')
        file = base_path / 'example.xlsx'
        workbook = load_workbook(filename = file)
        return workbook.worksheets[0] if workbook.worksheets else None


    def parse(self):
        parsing_item = ParsingItem()
        rows = list()

        for row in self.sheet[self.sheet.dimensions]:
            if row[0].row >= 2:
                row_val = [el.value for el in row]
                if row_val[0] and row_val[1]:
                    dict_item = parsing_item.to_dict()
                    if dict_item:
                        rows.append(dict_item)

                    parsing_item = ParsingItem()
                    parsing_item.set_product(row_val)
                else:
                    parsing_item.insert_nested(row_val)
        return rows