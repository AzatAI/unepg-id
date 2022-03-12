import datetime

import xlrd
import os
from generator import Generator

path = os.getcwd()
book = xlrd.open_workbook(path+'/girl.xlsx')
worksheet = book.sheet_by_index(0)

data = []
for i in range(worksheet.nrows):
    row = []
    for j in range(worksheet.ncols):
        row.append(worksheet.cell_value(i, j))
    data.append(row)

time = len(data) * 3.4
print(f"Total count: {len(data)}")
print(f"Time: {time} sec")

for row in data:
    generator = Generator(name=row[0], pk=row[1], category=row[2], country=row[3], country_code=row[4])
    generator.generate_images()
    time -= 3.4
    print(f"Remain: {time}")


