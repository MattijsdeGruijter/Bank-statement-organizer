import pandas as pd

class CsvToExcelConverter:
    def __init__(self, input_filename, output_filename=None, delimiter=';') -> None:
        self.input_filename = input_filename
        self.output_filename = output_filename or input_filename.replace('.csv', '.xlsx')
        self.delimiter = delimiter

    def convert_csv_to_excel(self):
        """
        Converts a CSV file to an Excel file.
        """
        try:
            df = self.read_csv_file()
            self.process_dataframe(df)
            self.save_to_excel(df)
            return self.output_filename
        except Exception as e:
            print(f"Error: {str(e)}")

    def read_csv_file(self):
        """
        Reads the CSV file and returns a DataFrame.
        """
        return pd.read_csv(self.input_filename, sep=self.delimiter)

    def process_dataframe(self, df):
        """
        Process the DataFrame, e.g., replacing commas with periods and data type conversion.
        """
        df.columns = ['datum', 'omschrijving', 'rekening', 'tegenrekening', 'code', 'afbij', 'bedrag', 'mutatiesoort', 'mededeling', 'saldo', 'tag']
        df['bedrag'] = df['bedrag'].str.replace(',', '.').astype(float)
        df['saldo'] = df['saldo'].str.replace(',', '.').astype(float)

    def save_to_excel(self, df):
        """
        Saves the DataFrame to an Excel file.
        """
        df.to_excel(self.output_filename, index=None, header=True)

# Example usage:
# converter = CsvToExcelConverter('input.csv', 'output.xlsx', delimiter=';')
# converter.convert_csv_to_excel()