import win32com.client

excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = False
wb = excel.Workbooks.Open(r"full_path_to_your_file.xlsx")
ws = wb.Worksheets("Certificado")  # Sheet you want to print

ws.ExportAsFixedFormat(0, r"full_output_path.pdf")  # 0 = PDF format
wb.Close(False)
excel.Quit()