import pandas as pd
from io import BytesIO

def generate_report(data: list, sheet_name: str = 'Hoja1', excluded_columns: list=[], excluded_rows: list=[], 
                    colors: dict={'header': '#dae366', 'even': '#edf1b3', 'odd': '#ffffff'}) -> BytesIO:
    """Generate a report from the provided data.

    Args:
        data: List of dictionaries containing the data.
        sheet_name: Name of the sheet in the excel report.
        excluded_columns: List of column names to exclude from the report.
        excluded_rows: List of row numbers to exclude from the report.
        colors: Dictionary containing the colors for the "header"/"odd"/"even" keys.

    Returns:
        A file like object containing the excel report.

    TODO: add more features, support other file formats instead of excel such as PDF/HTML, other data structures
    """
    # first row bold titles, colors for the header and odd/even rows different
    df = pd.DataFrame(data)
    df.drop(excluded_rows, inplace=True)
    df.drop(columns=excluded_columns, inplace=True)
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheet_name, index=False)


    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    # Add a header format.
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': colors['header'],
        'border': 1
    })

    # Write the column headers with the defined format.
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)

    # Write the alternating rows with different colors and borders for specific columns.
    for row_num in range(1, len(df) + 1):
        for col_num in range(len(df.columns)):
            if row_num % 2 == 0:
                cell_format = workbook.add_format({'fg_color': colors['even'], 'border': 1})
            else:
                cell_format = workbook.add_format({'fg_color': colors['odd'], 'border': 1})

            worksheet.write(row_num, col_num, df.iloc[row_num-1, col_num], cell_format)

    writer.close()

    # Rewind the buffer.   
    output.seek(0)
    return output

# Manually test the function formatting by generating a report with the provided data
if __name__ == '__main__':
    data = [
        {'interface': 'GigabitEthernet1/0/1', 'config': 'config1', 'status': 'TEST', 'ip_address': '192.0.0.1:8000'},
        {'interface': 'GigabitEthernet1/0/2', 'config': 'config2', 'status': 'TEST', 'ip_address': '192.0.0.2:8000'},
        {'interface': 'GigabitEthernet1/0/3', 'config': 'config3', 'status': 'TEST', 'ip_address': '192.0.0.3:8000'},
        {'interface': 'GigabitEthernet1/0/1', 'config': 'config1', 'status': 'TEST', 'ip_address': '192.0.0.4:8000'},
        {'interface': 'GigabitEthernet1/0/2', 'config': 'config2', 'status': 'TEST', 'ip_address': '192.0.0.5:8000'},
        {'interface': 'GigabitEthernet1/0/3', 'config': 'config3', 'status': 'TEST', 'ip_address': '192.0.0.6:8000'},
        {'interface': 'GigabitEthernet1/0/1', 'config': 'config1', 'status': 'TEST', 'ip_address': '192.0.0.7:8000'},
        {'interface': 'GigabitEthernet1/0/2', 'config': 'config2', 'status': 'TEST', 'ip_address': '192.0.0.8:8000'},
        {'interface': 'GigabitEthernet1/0/3', 'config': 'config3', 'status': 'TEST', 'ip_address': '192.0.0.9:8000'},
    ]
    output = generate_report(data=data, sheet_name='TEST', excluded_columns=['status'], excluded_rows=[0,1])
    
    # save file to generate_report.xlsx in the current directory
    file = open('generate_report_test.xlsx', 'wb')
    file.write(output.getvalue())
    file.close()
