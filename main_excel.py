from csv_to_xlsx_converter import CsvToExcelConverter
from json_dictionary_manager import JsonDictionaryManager
from read_transactions_from_excel import ReadTransactionsFromExcel
from write_transactions_to_excel import WriteTransactionsToExcel
from settings import FILENAME

def main_excel() -> None:
    main_class = MainClass()
    main_class.execute()
    
class MainClass():
    def execute(self):
        self.csv_to_xlsx_converter()
        self.load_json_dictionary()
        self.read_excel_file()
        self.write_excel_file()
        
    def csv_to_xlsx_converter(self, filename=FILENAME):
        # Step 1: Convert CSV to Excel if necessary
        excel_converter = CsvToExcelConverter(filename)
        if excel_converter.input_filename.endswith('.csv'):
            self.excel_file = excel_converter.convert_csv_to_excel()
            return self.excel_file

    def load_json_dictionary(self, dictionary_filename='dictionary.json'):
        # Step 2: Load the dictionary
        self.json_dict_object = JsonDictionaryManager(dictionary_filename)
        json_dict = self.json_dict_object.load_dictionary_from_file()
        return json_dict

    def read_excel_file(self):
        # Step 3: Read out the excel file that was converted from csv
        read_excel_object = ReadTransactionsFromExcel(self.json_dict_object, self.excel_file)
        self.transactions_per_month_per_category, self.totals_per_month, self.transactions_per_month = read_excel_object.go_through_excel_file()
        
    def write_excel_file(self):
        # Step 4: write all the transactions to the excel file
        write_excel_object = WriteTransactionsToExcel(self.excel_file, self.json_dict_object, self.totals_per_month, self.transactions_per_month_per_category, self.transactions_per_month)
        write_excel_object.write_totals_per_category_to_total_sheet()
        write_excel_object.write_month_transactions()
    
if __name__ == '__main__':
    main_excel()