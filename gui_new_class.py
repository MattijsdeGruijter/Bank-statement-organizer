import tkinter as tk
import customtkinter as ctk
from tkinter import simpledialog, ttk, filedialog, messagebox
from main_excel import main_excel
from json_dictionary_manager import JsonDictionaryManager
from read_transactions_from_excel import ReadTransactionsFromExcel
from csv_to_xlsx_converter import CsvToExcelConverter
import os


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

#moved everything into a class and nothing broke! I think..
#Note to self: start out with a class based system next time
class BankTransfersOrganizerApp:
    
    def __init__(self, root):
        
        self.root = root
        self.root.title("Bank Transfers Organizer")
        
        # Create a frame to hold the display
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack()
        
        #these babies let you shift your entire grid down or to the right 
        #(don't bring your negative enegry (and more important, negative numbers) here!)
        #Note to self, add this every time you have any kind of grid
        #Should add padding constants as well but im lazy to change everything
        
        #So future me is looking at this code, and it looks like I just moved 
        #everything into 1 class??? Of course nothing broke! 
        self.STARTING_ROW = 1
        self.STARTING_COL = 1
        self.file_path = None
        # File path for storing the dictionary
        dictionary_file = "dictionary.json"
        self.json_dict_object = JsonDictionaryManager(dictionary_file)
        dict_data_loader = self.json_dict_object.load_dictionary_from_file()
        self.dict_data = self.json_dict_object.data
            
        self.tree_fixed_data = {}
        self.tree_returning_data = {}
        self.tree_exception_data = {}
        
        self.tree_other_data = {}

        # Create widgets, update the display initially and select the first category
        self.create_widgets()
        self.update_display()
        self.select_first_category()  


    def create_widgets(self):
        
        self.label_filename = ctk.CTkLabel(self.frame, text="Please select your\ncsv file from ING bank\n(with the ; seperator)")
        self.label_filename.grid(row=self.STARTING_ROW, column=self.STARTING_COL-1, sticky="nswe", padx=10, pady=10)

        self.select_file_button = ctk.CTkButton(self.frame, text="Select .csv File", command=self.select_file)
        self.select_file_button.grid(row=self.STARTING_ROW+1, column=self.STARTING_COL-1, columnspan=1, sticky="we", padx=10, pady=1)
        self.file_path_label = ctk.CTkLabel(self.frame, text="No .csv file selected!")
        self.file_path_label.grid(row=self.STARTING_ROW-1, column=self.STARTING_COL-1, columnspan=6, sticky="we", padx=10, pady=1)
        
        
        # Create a listbox to display keys
        self.category_listbox = tk.Listbox(self.frame)
        self.category_listbox.grid(row=self.STARTING_ROW, column=self.STARTING_COL, sticky="nswe", padx=10, pady=10)
        self.scrollbar = ctk.CTkScrollbar(self.frame, command=self.category_listbox.yview)
        self.scrollbar.grid(row=self.STARTING_ROW, column=self.STARTING_COL+1, sticky="ns")
        self.category_listbox.config(yscrollcommand=self.scrollbar.set)

        # Create a listbox to show the keywords
        self.keywords_tree = ttk.Treeview(self.frame, columns=("Keywords"), show="headings")
        self.keywords_tree.grid(row=self.STARTING_ROW, column=self.STARTING_COL+2, sticky="nswe", padx=10, pady=10)
        self.keywords_tree.heading("Keywords", text="Keywords")
        
        self.category_listbox.unbind("<<ListboxSelect>>")
        self.category_listbox.bind("<<ListboxSelect>>", self.synchronize_selection_and_show_keywords)

        #create the trees
        self.tree_fixed = ttk.Treeview(self.frame, columns=("Fixed_Costs"), show="headings")
        self.tree_fixed.grid(row=self.STARTING_ROW+3, column=self.STARTING_COL, columnspan=2, padx=10, pady=10)

        self.tree_returning = ttk.Treeview(self.frame, columns=("Returning_Costs"), show="headings")
        self.tree_returning.grid(row=self.STARTING_ROW+3, column=self.STARTING_COL+2, columnspan=2, padx=10, pady=10)

        self.tree_exception = ttk.Treeview(self.frame, columns=("Exception_Costs"), show="headings")
        self.tree_exception.grid(row=self.STARTING_ROW+3, column=self.STARTING_COL+4, columnspan=2, padx=10, pady=10)

        # Create a Combobox for selecting category types
        self.type_combobox = ttk.Combobox(self.frame, values=("fixed cost", "returning cost", "exception cost"))
        self.type_combobox.grid(row=self.STARTING_ROW, column=self.STARTING_COL+4, padx=10, pady=10)
        
        # Bind the combobox selection change event to update the category type
        self.type_combobox.unbind("<<ComboboxSelect>>")
        self.type_combobox.bind("<<ComboboxSelected>>", self.update_category_type)

        # Set up column headings
        self.tree_fixed.heading("Fixed_Costs", text="Fixed Costs")
        self.tree_returning.heading("Returning_Costs", text="Returning Costs")
        self.tree_exception.heading("Exception_Costs", text="Exception Costs")

        # Set up column colors
        self.tree_fixed.tag_configure("fixed cost", background="lightblue")
        self.tree_returning.tag_configure("returning cost", background="lightgreen")
        self.tree_exception.tag_configure("exception cost", background="lightcoral")

        self.tree_returning.bind("<Button-1>",self.disable_tree_selection)
        self.tree_exception.bind("<Button-1>",self.disable_tree_selection)
        self.tree_fixed.bind("<Button-1>",self.disable_tree_selection)
        
        # Create the tree
        self.tree_other = ttk.Treeview(self.frame, columns=("Omschrijving", "Mededeling", "Af_Bij"), show="headings")
        self.tree_other.column("Af_Bij", anchor = "center")
        self.tree_other.grid(row=self.STARTING_ROW+4, column=self.STARTING_COL, columnspan=6, padx=10, pady=10)

        # Set up column headings
        self.tree_other.heading("Omschrijving", text="Omschrijving")
        self.tree_other.heading("Mededeling", text="Mededeling")
        self.tree_other.heading("Af_Bij", text="Af/Bij", anchor="center")  # New column heading

        # Set up column colors
        self.tree_other.tag_configure("Omschrijving", background="darkblue")
        self.text_to_insert = "This field will show a list of \nall transactions that are not in \ncategories yet.\nPlease update the list"
        self.tree_other.insert("", "end", values=(self.text_to_insert,)) 
        self.tree_other.bind("<Button-1>",self.disable_tree_selection)
        
        # Create buttons to add keys and keywords
        self.add_key_button = ctk.CTkButton(self.frame, text="Add Category", command=self.add_category)
        self.add_key_button.grid(row=self.STARTING_ROW+1, column=self.STARTING_COL, columnspan=2, sticky="we", padx=10, pady=1)

        self.add_keyword_button = ctk.CTkButton(self.frame, text="Add Keyword", command=self.add_keyword)
        self.add_keyword_button.grid(row=self.STARTING_ROW+1, column=self.STARTING_COL+2, columnspan=2, sticky="we", padx=10, pady=1)

        self.delete_category_button = ctk.CTkButton(self.frame, text="Delete Category", command=self.are_you_sure_category_pop_up)
        self.delete_category_button.grid(row=self.STARTING_ROW+2, column=self.STARTING_COL, columnspan=2, sticky="we", padx=10, pady=1)

        self.delete_keyword_button = ctk.CTkButton(self.frame, text="Delete Keyword", command=self.are_you_sure_keyword_pop_up)
        self.delete_keyword_button.grid(row=self.STARTING_ROW+2, column=self.STARTING_COL+2, columnspan=2, sticky="we", padx=10, pady=1)
        
        self.calculate_button = ctk.CTkButton(self.frame, text="Update list", command=self.update_other_tree)
        self.calculate_button.grid(row=5, column=2, columnspan=2, sticky="we", padx=10, pady=1)

        self.run_button = ctk.CTkButton(self.frame, text="Create Excel file", command=self.create_excel_file)
        self.run_button.grid(row=self.STARTING_ROW+6, column=self.STARTING_COL+2, columnspan=2, sticky="we", padx=10, pady=1)    
        self.status = ctk.CTkLabel(self.frame, text="Excel file not yet created")
        self.status.grid(row=self.STARTING_ROW+7, column=self.STARTING_COL, columnspan=6, sticky="we", padx=10, pady=1)  

    def are_you_sure_keyword_pop_up(self):
        selected_keyword_index = self.keywords_tree.selection()
        if selected_keyword_index:
            selected_category = self.keywords_tree.category
            keyword_index = selected_keyword_index[0]
            keyword_to_delete = self.keywords_tree.item(keyword_index)["values"][0]
            confirmed = messagebox.askyesno("Delete Category", f"Are you sure you want to delete '{keyword_to_delete}' in the category:'{selected_category}'?")

        if confirmed:
            self.delete_keyword()
    
    def are_you_sure_category_pop_up(self):
        selected_category = self.category_listbox.get(tk.ACTIVE)
        confirmed = messagebox.askyesno("Delete Category", f"Are you sure you want to delete '{selected_category}' and all of its keywords?")

        if confirmed:
            self.delete_category()
    #dummy function so that nothing happens when you click the trees
    def disable_tree_selection(self, event):
        
        return "break"
    
    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if self.file_path:
            self.file_path_label.configure(text="Selected file: " + self.file_path)

    def update_display(self):
        
        # Clear the existing display
        self.category_listbox.delete(0, tk.END)
        self.keywords_tree.delete(*self.keywords_tree.get_children())
        for category, data in self.dict_data.items():
            self.category_listbox.insert(tk.END, category)
        self.update_category_trees()
        # update_other_tree()6

    def update_category_trees(self):
        
        self.tree_fixed.delete(*self.tree_fixed.get_children())
        self.tree_returning.delete(*self.tree_returning.get_children())
        self.tree_exception.delete(*self.tree_exception.get_children())
        
        # Clear the dictionaries before updating
        self.tree_fixed_data.clear()
        self.tree_returning_data.clear()
        self.tree_exception_data.clear()
        #populate the trees
        for category, data in self.dict_data.items():
            type_trans = data["type"]
            tags = (type_trans.lower(),)
            types = {"fixed cost": "", "returning cost": "", "exception cost": ""}
            types[type_trans] = category
            
            if types["fixed cost"]:
                item = self.tree_fixed.insert("", "end", values=(types["fixed cost"]), tags=tags)
                self.tree_fixed_data[category] = item
            elif types["returning cost"]:
                item = self.tree_returning.insert("", "end", values=(types["returning cost"]), tags=tags)
                self.tree_returning_data[category] = item
            elif types["exception cost"]:
                item = self.tree_exception.insert("", "end", values=(types["exception cost"]), tags=tags)
                self.tree_exception_data[category] = item

    def select_item_by_text(self, item_text):
        
        for index in range(self.category_listbox.size()):
            if self.category_listbox.get(index) == item_text:
                self.category_listbox.selection_set(index)
                break 
        
    def synchronize_selection(self, event):

        selected_index = self.category_listbox.curselection()
        if selected_index:
            index = int(selected_index[0])
            selected_category = self.category_listbox.get(index)
            print("select" + selected_category)
        else:
            selected_category = self.keywords_tree.category
            selected_index = self.keywords_tree.selection()
            if selected_index:
                index = int(selected_index[0])
                selected_category = self.keywords_tree.item(index)["values"][0]
            self.select_item_by_text(selected_category)
        # Set selection in the appropriate tree based on selected category, deselect the other trees
        if selected_category in self.tree_fixed_data:
                self.tree_returning.selection_remove(self.tree_returning.selection())
                self.tree_exception.selection_remove(self.tree_exception.selection())
                self.tree_fixed.selection_set(self.tree_fixed_data[selected_category])
            
        elif selected_category in self.tree_returning_data:
            self.tree_fixed.selection_remove(self.tree_fixed.selection())
            self.tree_exception.selection_remove(self.tree_exception.selection())
            self.tree_returning.selection_set(self.tree_returning_data[selected_category])
        
        elif selected_category in self.tree_exception_data:           
            self.tree_returning.selection_remove(self.tree_returning.selection())
            self.tree_fixed.selection_remove(self.tree_fixed.selection())
            self.tree_exception.selection_set(self.tree_exception_data[selected_category])
        
    def show_keywords(self, event):
        
        selected_index = self.category_listbox.curselection()
        if selected_index:
            index = int(selected_index[0])
            selected_category = self.category_listbox.get(index)
            for keyword in self.dict_data[selected_category]["key_words"]:
                if self.keywords_tree.exists(keyword)==False:
                    self.keywords_tree.insert("", "end", text=keyword)
            self.update_keywords_list(selected_category)
            self.keywords_tree.category = selected_category
            
            # Update the keywords list and maintain the category selection
            self.category_listbox.selection_set(index)
            
    def show_type(self, event):
        
        selected_index = self.category_listbox.curselection()
        if selected_index:
            index = int(selected_index[0])
            selected_category = self.category_listbox.get(index)
            if selected_category in self.dict_data:
                self.type_combobox.set(self.dict_data[selected_category]["type"])

    def synchronize_selection_and_show_keywords(self, event):  
           
        self.synchronize_selection(event)
        self.show_keywords(event)
        self.show_type(event)

    def select_first_category(self):
        
        if self.category_listbox.size() > 0:
            self.category_listbox.selection_set(0)
            self.category_listbox.event_generate("<<ListboxSelect>>")
        
    def update_keywords_list(self, selected_category):
        
        self.keywords_tree.delete(*self.keywords_tree.get_children())
        for keyword in self.dict_data[selected_category]["key_words"]:
            self.keywords_tree.insert("", "end", values=(keyword,))
        self.keywords_tree.category = selected_category
        
    def update_category_type(self, event):
        
        selected_category = self.category_listbox.get(tk.ACTIVE)
        print("update_type", selected_category)
        new_type = self.type_combobox.get()
        if selected_category in self.dict_data:
            self.dict_data[selected_category]["type"] = new_type
            self.json_dict_object.save_dictionary_to_file(self.dict_data)
            self.update_category_trees()
            self.select_item_by_text(selected_category)

    def add_category(self):
        
        new_category = simpledialog.askstring("Add category", "Enter a new category:")
        if new_category:
            self.dict_data[new_category] = {}
            self.dict_data[new_category]["total"] = 0
            self.dict_data[new_category]["key_words"] = []
            self.dict_data[new_category]["type"] = "exception cost"
            self.save_dictionary_to_file(self.dict_data, self.dictionary_file)
            self.update_display()

    def add_keyword(self):
        
        selected_category = self.category_listbox.get(tk.ACTIVE)
        if selected_category:
            new_keyword = simpledialog.askstring("Add Keyword", f"Enter a keyword for '{selected_category}':", parent=self.root)
            if new_keyword:
                self.dict_data[selected_category]["key_words"].append(new_keyword)
                self.json_dict_object.save_dictionary_to_file(self.dict_data)
                self.update_keywords_list(selected_category)  # Update the keywords list

    def delete_keyword(self):
        
        selected_keyword_index = self.keywords_tree.selection()
        if selected_keyword_index:
            selected_category = self.keywords_tree.category
            keyword_index = selected_keyword_index[0]
            keyword_to_delete = self.keywords_tree.item(keyword_index)["values"][0]
            print(keyword_to_delete)
            self.dict_data[selected_category]["key_words"].remove(keyword_to_delete)
            self.json_dict_object.save_dictionary_to_file(self.dict_data)
            self.update_keywords_list(selected_category)  # Update the keywords list
            
    def delete_category(self):
        
        selected_category = self.category_listbox.get(tk.ACTIVE)
        if selected_category:
            self.dict_data.pop(selected_category, None)
            self.json_dict_object.save_dictionary_to_file(self.dict_data)
            self.update_display()

    def update_other_tree(self):
        
        self.tree_other.delete(*self.tree_other.get_children())

        # Clear the dictionaries before updating
        self.tree_other_data.clear()
        
        #get the info from the excel file
        if self.file_path is not None:
            file_name = os.path.basename(self.file_path)
            excel_converter = CsvToExcelConverter(file_name)
            if excel_converter.input_filename.endswith('.csv'):
                file_name = excel_converter.convert_csv_to_excel()
            read_excel_object = ReadTransactionsFromExcel(self.json_dict_object, file_name)
            transactions_per_month_per_category, totals_per_month, transactions_per_month = read_excel_object.go_through_excel_file()
            #populate the tree
            iterator_months = iter(transactions_per_month_per_category)
            most_recent_month = next(iterator_months)
            if 'Other' in transactions_per_month_per_category[most_recent_month]:
                trans_to_display = transactions_per_month_per_category[most_recent_month]['Other']
                for useless, trans_dict in trans_to_display.items():
                    if useless != 'Totaal':
                        omschrijving = trans_dict['Korte naam']
                        mededeling = trans_dict['Naam']
                        af_bij_value = trans_dict['Bedrag']
                        self.tree_other.insert("", "end", values=(omschrijving, mededeling, af_bij_value))
            else:
                text_to_insert = "Done! All transactions are placed \ninto categories. \nYou are ready to create the excel file"
                self.tree_other.insert("", "end", values=(text_to_insert,))    
        else: text_to_insert = "You need to select a .CSV file first!"

    def create_excel_file(self):
        
        main_excel()
        self.status._text = "Excel file created successfully"
        print(self.status._text)

def main():
    
    app_root = ctk.CTk()
    app = BankTransfersOrganizerApp(app_root)
    # Start the main GUI loop
    app_root.mainloop()

if __name__ == "__main__":
    
    main()