from csv_to_xlsx_converter import CsvToExcelConverter
from json_dictionary_manager import JsonDictionaryManager
from read_transactions_from_excel import ReadTransactionsFromExcel
from write_transactions_to_excel import WriteTransactionsToExcel
from settings import FILENAME

def main_excel(filename=FILENAME, dictionary_filename='dictionary.json') -> None:
    # Step 1: Convert CSV to Excel if necessary
    excel_converter = CsvToExcelConverter(filename)
    if excel_converter.input_filename.endswith('.csv'):
        excel_file = excel_converter.convert_csv_to_excel()
    
    # Step 2: Load the dictionary
    json_dict_object = JsonDictionaryManager(dictionary_filename)
    json_dict = json_dict_object.load_dictionary_from_file()
    
    # Step 3: Read out the excel file that was converted from csv
    read_excel_object = ReadTransactionsFromExcel(json_dict_object, excel_file)
    transactions_per_month_per_category, totals_per_month, transactions_per_month = read_excel_object.go_through_excel_file()
    

    # Step 4: write all the transactions to the excel file
    write_excel_object = WriteTransactionsToExcel(excel_file, json_dict_object, totals_per_month,transactions_per_month_per_category, transactions_per_month)
    write_excel_object.write_totals_per_category_to_total_sheet()
    write_excel_object.write_month_transactions()
    
if __name__ == '__main__':
    main_excel()