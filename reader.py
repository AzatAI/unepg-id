import datetime
import threading

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

    return value


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

    time = int(len(data) * 3.5) + 10
    time = datetime.timedelta(seconds=time)
    my_thread = threading.Thread(target=timer, args=(time, ))
    my_thread.start()

    for row in data:
        generator = Generator(name=row[0], pk=row[1], category=row[2], country=row[3], country_code=row[4],
                              result_path=dir_path)
        generator.generate_images()
