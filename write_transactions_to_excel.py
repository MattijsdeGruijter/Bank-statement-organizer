import openpyxl
import tkinter as tk
import sys
from openpyxl.styles import PatternFill, Font

class ExcelFileProcessor:
    def __init__(self, filename, save_load, totals_month) -> None:
        self.filename = filename
        self.data_only = False
        self.save_load = save_load
        self.totals_month = totals_month
        self.fill = PatternFill(start_color='BFBFBF', end_color='BFBFBF', fill_type="solid")

    def open_workbook(self):
        '''
        Tries to open the workbook, gives an error if it
        fails to open the file
        '''
        try:
            self.workbook = openpyxl.load_workbook(self.filename, data_only=self.data_only)
            return self.workbook
        except PermissionError:
            # Display pop-up message box
            root = tk.Tk()
            root.withdraw()
            tk.messagebox.showinfo("Permission Denied", "Please close the workbook '{}' and try again.".format(self.filename))
            return sys.exit()
    # Create the "total" sheet and write the totals for each month
    
    def write_totals_per_category_to_total_sheet(self) -> None:
        '''
        Creates a new sheet in the workbook called 'Total'
        if there is already a 'Total' sheet, it will be
        removed and recreated.
        
        Every category will have his own row, where the 
        totals of each month will be written in columns.
        '''
        self.open_workbook()
        self.total_sheet__create_total_sheet()
        self.total_sheet__put_categories_in_first_column_and_format()
        self.total_sheet__write_totals_per_month_in_the_next_columns()
        self.save_workbook()
    
    def total_sheet__create_total_sheet(self) -> None:
        if 'Total' in self.workbook.sheetnames:
            total_sheet = self.workbook['Total']
            self.workbook.remove(total_sheet)
        self.sheet_total = self.workbook.create_sheet('Total')
        self.sheet_total.column_dimensions['A'].width = 20
        
    def total_sheet__put_categories_in_first_column_and_format(self) -> None:       
        '''
        sort the dict so that the overall sum of 
        the most expencive category is on top
        write the categories to the first column
        also format the even rows with a grey color
        '''
        row_num = 2
        self.totals = self.save_load.data
        totals_sorted = dict(sorted(self.totals.items(), key=lambda x: abs(x[1]['total']), reverse=True))
        for cat in totals_sorted:
            self.sheet_total.cell(row=row_num, column=1).value = cat
            if row_num % 2 == 0:
                self.sheet_total.cell(row=row_num, column=1).fill = self.fill
            row_num += 1
        
    def total_sheet__write_totals_per_month_in_the_next_columns(self):
        for month, category_dict in self.totals_month.items():
            
            # Find the first empty column for the date and amounts
            col_num = 2
            while self.sheet_total.cell(row=1, column=col_num).value:
                col_num += 1
            # Write the date to cell 
            self.sheet_total.cell(row=1, column=col_num).value = month
            self.sheet_total.cell(row=1, column=col_num).font = Font(bold=True)
                    
            #Go through all the categories and check against the category in the dict. If it matches, write the value
            for cat_cell in self.sheet_total.iter_rows(min_row=2, max_row=len(self.totals)+2, min_col=1):  
                if cat_cell[0].row % 2 == 0:
                    self.sheet_total.cell(row=cat_cell[0].row, column=col_num).fill = self.fill
                for category, bedrag in category_dict.items():
                    if cat_cell[0].value == category:
                        self.sheet_total.cell(row=cat_cell[0].row, column=col_num).value = bedrag
                        if cat_cell[0].row % 2 == 0:
                            self.sheet_total.cell(row=cat_cell[0].row, column=col_num).fill = self.fill
                
    def save_workbook(self) -> None:
        self.workbook.save(self.filename)
