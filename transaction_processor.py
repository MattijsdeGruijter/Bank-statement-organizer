from.settings import MAX_ROW
import re
import datetime

class TransactionProcessor:
    def __init__(self, sheet, json_dictionary_manager):
        self.sheet = sheet
        self.json_dictionary_manager = json_dictionary_manager
        self.transactions_per_month = {}
        self.totals_per_month = {}
        
    def get_transaction(self, date_row):
        date, naam_omschrijving, rekening, tegenrekening, code, af_bij, bedrag_raw, mutatiesoort, mededeling, saldo_na_mutatie = date_row
        
        
        bedrag = self.float_precision(bedrag_raw)
        if af_bij == 'Af':
                    bedrag = -bedrag
        mededeling_new, naam_omschrijving_new = self.rewrite_transaction(mededeling, naam_omschrijving)
        category = self.categorize_transaction(naam_omschrijving_new, mededeling, bedrag)
            
        transaction = {
            'Datum': date,
            'Bedrag': self.float_precision(bedrag),
            'Naam': mededeling,
            'Category': category,
            'Korte naam': naam_omschrijving_new,
            'Mededeling': mededeling_new,
            'Saldo na mutatie': saldo_na_mutatie
        }
        
        self.fill_dictionaries(date, transaction, category, bedrag)
        
        return transaction

    def categorize_transaction(self, naam_omschrijving, mededeling, bedrag):
        for cat, cat_dict in self.json_dictionary_manager.data.items():
            if cat != "Other": 
                # if 'betaalverzoek' in naam_omschrijving.lower() or naam_omschrijving.lower()[0:3] == 'hr ' or naam_omschrijving.lower()[0:3] == 'mw ':
                #     category = 'Overschrijving'
                #     pattern = r":(.*?)IBAN:"
                #     match = re.search(pattern, mededeling)
                #     if match:
                #         naam_omschrijving = match.group(1)
                keywords = cat_dict['key_words']
                for keyword in keywords:
                    if keyword in mededeling.lower() or keyword in naam_omschrijving.lower():
                        category = cat
                        self.json_dictionary_manager.data[category]["total"] += self.float_precision(bedrag)  
                        self.json_dictionary_manager.save_dictionary_to_file()
                        return category  
    
    def rewrite_transaction(self, mededeling, naam_omschrijving):
        """
        Extracts the relevant part of the mededeling/naam_omschrijving.
        """
        
    # Define a dictionary to map keywords to new values
        keyword_mappings = {
            "spaarrekening": r"spaarrekening (.*?)Valuta",
            "belasting": r"Omschrijving: (.*?)IBAN",
            "betaalverzoek": r"Omschrijving: (.*?)IBAN",
            "tikkie": r"Naam: (.*?)NL"
        }

        # Extract mededeling_only using the first pattern
        pattern1 = r"Omschrijving:(.*?)IBAN:"
        match1 = re.search(pattern1, mededeling)
        mededeling_only = match1.group(1) if match1 else ""

        # Check for keywords and update naam_omschrijving
        for keyword, pattern in keyword_mappings.items():
            if keyword in mededeling.lower():
                match2 = re.search(pattern, mededeling)
                if match2:
                    naam_omschrijving = match2.group(1)
                if keyword in ["betaalverzoek", "tikkie"]:
                    category = "Overschrijving"
                break  # Exit the loop once a match is found

        return mededeling_only, naam_omschrijving
        
    
    def go_through_excel_file(self):
        for date_row in self.sheet.iter_rows(min_row=2, min_col=1, max_col=13, max_row=MAX_ROW):
            transaction = self.get_transaction(date_row)
    
    def fill_dictionaries(self, date, transaction, category, bedrag):         
        date_in_datetime = datetime.datetime.strptime(str(date), '%Y%m%d')
        month = date_in_datetime.strftime('%Y-%m')
        if month not in self.transactions_per_month:
            self.transactions_per_month[month] = []
        self.transactions_per_month[month].append(transaction)
        
        if month not in self.totals_per_month:
            self.totals_per_month[month] = {}
            
        if category not in self.totals_per_month[month]:
            self.totals_per_month[month][category] = 0
        
        self.totals_per_month[month][category] += bedrag
        self.totals_per_month[month][category] = self.float_precision(self.totals_per_month[month][category])
        
        #sort transactions by bedrag    
        for key, value in self.transactions_per_month.items():
            if isinstance(value, dict) and 'Totaal' not in value:
                sorted_nested = dict(sorted(value.items(), key=lambda x: abs(x[1]['Bedrag']), reverse=True))
                self.transactions_per_month[key] = sorted_nested

        return self.transactions_per_month, self.totals_per_month
# Go through all the transactions in the excel sheet and return 3 values:
# 1. A dictionary of the transactions per month in this form: {month: {transaction: {date: date, etc: etc}}}
# 2. A dictionary the toals per month per category in this form: {month: {category: {total: 300}}}
# 3. An updated version of the category dictionary with the totals per category


    # Go through the transactions_per_month dictionary and return a dictionary {month: {category{{transaction: {date: date, etc: etc}}}}
    def get_transactions_per_category(self):
        self.transactions_per_month_per_category = {}
        for maand, list_of_transactions in self.transactions_per_month.items():
            if maand not in self.transactions_per_month_per_category:
                self.transactions_per_month_per_category[maand] = {}
                
                        
            for transaction in list_of_transactions:
                for category in self.json_dictionary_manager.data:
                    if transaction['Category'] == category:
                        if category not in self.transactions_per_month_per_category[maand]:
                            self.transactions_per_month_per_category[maand][category]= {}
                        self.transactions_per_month_per_category[maand][category][transaction['Naam']] = transaction
                        if 'Totaal' not in self.transactions_per_month_per_category[maand][category]:
                            self.transactions_per_month_per_category[maand][category]['Totaal'] = 0
                        bedrag = transaction['Bedrag']
                        self.transactions_per_month_per_category[maand][category]['Totaal'] += bedrag
                        
        # formatted_data = json.dumps(self.transactions_per_month_per_category, indent=4, sort_keys=True)
        # print(formatted_data)            
        return self.transactions_per_month_per_category
    
    #deals with float precision
    def float_precision(self, input):
        input_rounded = "{:.2f}".format(input)
        output = float(input_rounded)
        return output