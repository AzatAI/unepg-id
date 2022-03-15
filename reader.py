import xlrd
from generator import Generator


def clean_value(value: str, column_index: int, row_index: int):
    if column_index > 4:
        raise ValueError(f"Данные не валидные. В строке {row_index}. Описание количество столбцов должно быть рано 5")

    value = value.strip()
    value = value.replace("`", "")

    if column_index == 4:
        value = value.upper()
        if len(value) != 2:
            raise ValueError(
                f"Данные не валидные. В строке {row_index}. Код страны должен состоять из 2 символов")

    new_value = ""

    if column_index == 1:
        for i in value:
            if i.isnumeric():
                new_value += i
    return value


def run_timer(timer, data, dir_path):
    timer(data, dir_path)


def open_xlsx(file_path, dir_path, timer, window):
    book = xlrd.open_workbook(file_path)
    worksheet = book.sheet_by_index(0)

    data = []
    for i in range(worksheet.nrows):
        row = []
        for j in range(worksheet.ncols):
            value = clean_value(worksheet.cell_value(i, j), j, i)
            row.append(value)
        data.append(row)

    window.destroy()

    run_timer(timer, data, dir_path)
