import openpyxl

#
class ReadExcel():
  def __init__(self, file_path):
    self.workbook = openpyxl.workbook(file_path)
    self.worksheet = self.workbook.active()

  def get_data(self):
    data = []
    for row in self.worksheet.iter_rows():
      row_value = []
      for cell in row:
        row_value.append(cell.value)
      data.append(row_value)
    return data
  
if __name__ == '__main__':
  read_excel_obj = ReadExcel('')
  result = read_excel_obj.get_data()
  print(result)

