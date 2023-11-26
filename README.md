# Bank-statement-organizer
The goal of this code is to organize your bank statements.
How to use:
1. It needs a .CSV file from your bank (for now it only works with ING bank).
You can download this file from the banks website (mijn.ing.nl). It only works with a ";" separated file (which is the default).
2. Put it in the same folder as the code, and rename it to "Afschriften.csv"
3. Run main_excel.py 

That should do it.

The output is an excel file that has a tab for every month, and in that tab you can see all your transfers categorized by for example:
Groceries, taxes, rent, car costs, etc.
You can make up the categories yourself, and add or remove them as you want. For now this is done in the settings file, but a GUI is coming soon!

The transfers will be categorized based on keywords you provide. For example, you can say that all transfers that mention "albert hein" or "aldi" get put into the grocery category. Anything that mentions "toyota" gets put into the car costs category, etc.

The excel will also have a totals tab, where you can see in one overview how much you spend each month on each of the categories. 

## Explaining the code
### DISCLAIMER 
I'm teaching myself how to code. I don't know what I'm doing. The first version of this code was all in one file, just a bunch of functions in a row. Now I separated everything into classes. It seems more organized to me, but I have no idea if this is good practice, I just put parts of my code into ChatGPT sometimes and ask to improve it. 

### Right, on to the code

This code examines a .CSV file from a bank (for now it only works with ING bank).
You can download this file from the banks website (mijn.ing.nl). It only works with a ";" separated file (which is the default).

This file is basically a table, and every row in the file is one transaction or transfer on your main account. 
It has info about the amount of the transaction, if it was positive or negative, your balance after the transaction, the date, the counter bank account, and a description of the transfer.

Reding out the transactions goes as follows:
1. The code loops through the excel rows, and saves each transaction as a dictionary.
2. Transactions are grouped per month
3. Within these month groups, new groups are made based on their category

We end up with 3 dictionaries:
One with all the months, and within those months the categories and their totals. This one is used to fill an overview page in the output file called "totals"
For example:
```
{202308: 
	{"rent": -1200,
	 "groceries": -70.44,
	 "salary": 2500},
 202307:
	{"rent": -1200,
	 "car cost": -161.87,
	 "groceries": -70.44,
	 "salary": 2500}
}
```
One with all the transactions, grouped by month. This one is only used to determine what the first and last transaction of the month was, to show the beginning and end balance of the month. 
For example: 
```
{202308: 
	{"transaction 1": 
		{"date": 01-08-2023,
		 "amount": -5.35},
	 "transaction 2": 
		{"date": 02-08-2023,
		 "amount": -4},
	 "transaction 3": 
		{"date": 02-08-2023,
		 "amount": -10.54}
	},
 202307:
	{"transaction 1": 
		{"date": 02-07-2023,
		 "amount": -15.52},
	 "transaction 2": 
		{"date": 05-07-2023,
		 "amount": 41},
	 "transaction 3": 
		{"date": 06-07-2023,
		 "amount": -1.40}
	}
}
```
And one with all the transactions, grouped by month and category.
This is the main output. This dict is used to fill all the "month" pages in the output excel file

For example: 
```
{202308: 
	{"car cost":
		{"transaction 1": 
			{"date": 01-08-2023,
			 "amount": -5.35},
		 "transaction 2": 
			{"date": 02-08-2023,
			 "amount": -4},
		 "transaction 3": 
			{"date": 02-08-2023,
			 "amount": -10.54}
		},
	 "salary":
		{"transaction 1": 
			{"date": 01-08-2023,
			 "amount": 2500},
		}
	},
 202308: 
	{"car cost":
		{"transaction 1": 
			{"date": 01-08-2023,
			 "amount": -5.35},
		 "transaction 2": 
			{"date": 02-08-2023,
			 "amount": -4},
		 "transaction 3": 
			{"date": 02-08-2023,
			 "amount": -10.54}
		},
	 "salary":
		{"transaction 1": 
			{"date": 01-08-2023,
			 "amount": 2500},
		}
	}
}
```


These 3 dictionaries are used to fill the output excel file.

## GUI
I've made a GUI as well where you can edit the sorting/categorizing dictionary to add keywords and categories. 
I have not uploaded this part yet, still doing some testing. More on this later.
