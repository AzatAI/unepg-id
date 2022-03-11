import xlrd
import os
from generator import Generator

path = os.getcwd()
book = xlrd.open_workbook(path+'/girls.xlsx')
worksheet = book.sheet_by_index(0)

data = []
for i in range(worksheet.nrows):
    row = []
    for j in range(worksheet.ncols):
        row.append(worksheet.cell_value(i, j))
    data.append(row)

for row in data:
    generator = Generator(name=row[0], pk=int(row[1]))
    generator.generate_images()
