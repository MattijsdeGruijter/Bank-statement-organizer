FILENAME = 'Afschriften.csv'
MAX_ROW = 10000
MAIN_CATEGORIE_DICT = {
        "Belasting": {
            "total": 0, 
            "key_words": ["belasting"],
            "type": "fixed cost"
        },
        "Boodschappen": {
            "total": 0, 
            "key_words": ["lidl", 
                          "aldi", 
                          "albert heijn", 
                          "hellofresh", 
                          "slijter", 
                          "toogoodtogo", 
                          "ah to go", 
                          "action", 
                          "nettorama", 
                          "jumbo", 
                          "7eleven",
                          "bb turfmarkt", 
                          ],
            "type": "returning cost"
        },
        "Car": {
            "total": 0, 
            "key_words": ["louwman", 
                          "kwikfit", 
                          "kwik fit", 
                          "park", ],
            "type": "exception cost"
        },
        "Cosmetics": {
            "total": 0,
            "key_words": ["kruidvat", 
                          "etos", 
                          "diegrenze"],
            "type": "returning cost"
        },
        "Creditcard": {
            "total": 0, 
            "key_words": ["creditcard"],
            "type": "returning cost"
        },
        "Dentist": {
            "total": 0, 
            "key_words": ["dental"],
            "type": "exception cost"
        },
        "Flights": {
            "total": 0, 
            "key_words": ["klm", 
                          "schiphol", 
                          "easyjet", 
                          "transavia"],
            "type": "exception cost"
        },
        "Furniture": {
            "total": 0, 
            "key_words": ["eijerkamp", 
                          "interior", 
                          "blossem bloem", 
                          "ikea", 
                          "intratuin"],
            "type": "exception cost"
        },
        "Gas": {
            "total": 0, 
            "key_words": ["tankstation", 
                          "tankstelle", 
                          "shell", 
                          "esso", 
                          "totalenergies", 
                          "tinq",
                          "tango"],
            "type": "returning cost"
        },
        "Health Insurance": {
            "total": 0, 
            "key_words": ["health insurance"],
            "type": "fixed cost"
        },
        "Heating": {
            "total": 0, 
            "key_words": ["eneco"],
            "type": "fixed cost"
        },
        "Holiday": {
            "total": 0, 
            "key_words": ["landal", 
                          "capfun"],
            "type": "exception cost"
        },
        "Horeca": {
            "total": 0, 
            "key_words": [
                          "ahoy", 
                          "athene",
                          "arsenaal", 
                          "backwerk",
                          "bagel", 
                          "bakker",
                          "beachclub",
                          "bier", 
                          "bills green", 
                          "bleyenberg",
                          "burrata", 
                          "cafe", 
                          "caffe",
                          "chidoz",
                          "cloos", 
                          "coffee", 
                          "de beren",
                          "dudok",
                          "eazie",
                          "el nino", 
                          "elliniko",
                          "febo", 
                          "fiddler", 
                          "five guys",
                          "food", 
                          "gyros", 
                          "haagse wereld hapj",
                          "hard rock cafe", 
                          "hudson stat", 
                          "iroion",
                          "kiosk", 
                          "kompaan",
                          "knossos", 
                          "la grappa",
                          "noodle",
                          "north sea jazz",
                          "markthal",
                          "oliebol", 
                          "osteria",
                          "pizza", 
                          "proeflokaal",
                          "reggae rotterdam",
                          "restaurant",
                          "snack",
                          "starbucks",
                          "strandexploitatie",
                          "stroopw", 
                          "subway", 
                          "supermercado",
                          "sushi", 
                          "thuisbezorgd",
                          "toilet",
                          "tonys",
                          "twins",
                          "vincenzos",
                          "wijn", 
                          ],
            "type": "returning cost"
        },
        "Investments": {
            "total": 0, 
            "key_words": ["13600072"],
            "type": "fixed cost"
        },
        "Kosten ING": {
            "total": 0, 
            "key_words": ["oranjepakket"],
            "type": "fixed cost"
        },
        "Life insurance": {
            "total": 0, 
            "key_words": ["dela natura"],
            "type": "fixed cost"
        },
        "Lunch": {
            "total": 0, 
            "key_words": ["rhdhv"],
            "type": "returning cost"
        },
        "Museum": {
            "total": 0, 
            "key_words": ["museum", 
                          "fabrique des lumieres"],
            "type": "exception cost"
        },
        "Other": {
            "total": 0, 
            "key_words": [""],
            "type": "exception cost"
        },
        "Overschrijving": {
            "total": 0, 
            "key_words": ["tikkie", ],
            "type": "exception cost"
        },
        "Pathe": {
            "total": 0, 
            "key_words": ["pathe"],
            "type": "fixed cost"
        },
        "Padel": {
            "total": 0, 
            "key_words": ["padel",
                          "syltek"],
            "type": "exception cost"
        },
        "Rent": {
            "total": 0, 
            "key_words": ["cbre dres"],
            "type": "fixed cost"
        },
        
        "Salaris": {
            "total": 0, 
            "key_words": ["haskoningdhv", 
                          "funding ci", 
                          "primat" , 
                          "convergence"],
            "type": "fixed cost"
        },
        "Shopping": {
            "total": 0, 
            "key_words": ["cotton", 
                          "pandora", 
                          "sportswear", 
                          "batavia", 
                          "nike", 
                          "adidas", 
                          "h & m", 
                          "h ? m", 
                          "amazon", 
                          "outlet", 
                          "bijenkorf", 
                          "hema", 
                          "flying tiger", 
                          "haribo", 
                          "fashion", 
                          "ravensburger", 
                          "sissyboy", 
                          "zara",
                          "uniqlo",
                          ],
            "type": "returning cost"
        },
        "Spaarrekening": {
            "total": 0, 
            "key_words": ["hr m de gruijter", 
                          "spaarrekening"],
            "type": "returning cost"
        },
        "Spotify": {
            "total": 0, 
            "key_words": ["paypal"],
            "type": "fixed cost"
        },
        "Telefoon": {
            "total": 0, 
            "key_words": ["lebara"],
            "type": "fixed cost"
        },
        "Trein": {
            "total": 0, 
            "key_words": ["ns groep", 
                          "htm ", 
                          "amsterdam gvb", 
                          "ns internation"],
            "type": "fixed cost"
        },
        "Verzekering": {
            "total": 0, 
            "key_words": ["klaverblad", 
                          "test"],
            "type": "fixed cost"
        },
        "Water": {
            "total": 0, 
            "key_words": ["dunea"],
            "type": "fixed cost"
        },
    }