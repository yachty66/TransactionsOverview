'''
- [x] keys into config
- [x] clean code
- [x] create file for adding to sheets
- [ ] get transactions and add them to csv as pandas df
- [ ] from json response take last entry and check if it is already in csv if not add it 
- [ ] repeat as long as there are new entries
- [ ] create google sheets
- [ ] add all new entries to google sheet
- [ ] create cronjob for every day 00:00
- [ ] clean code
'''

import pandas as pd
import json 

#get first dictionary from transactions.json
def getAllKeys():
    #convert json to dict
    convert = json.load(open('transactions.json'))
    keys = []
    allKeys = []
    for i in range(len(convert["transactions"]["booked"])):
        keys = list(convert["transactions"]["booked"][i].keys())
        for j in keys:
            allKeys.append(j)
    #transactionAmount': {'amount': '-18.99', 'currency': 'EUR'}
    #still need to add the keys from the nested dict later

    #add amount and currency manually
    allKeys.append('amount')
    allKeys.append('currency')
    finalKeys = set(allKeys)
    print(finalKeys)
    return finalKeys
    # now i have keys and i need to create a df with them as header and also add amount and currency to header 
    # than i need to go through transaction data and add every row to respective column
    #I only add this row if it is not already in the csv (check with transaction id)
    
def addTransactionsToCsv():
    #load json with transactions
    convert = json.load(open('transactions.json'))
    #loop over all transactions
    for i in range(len(convert["transactions"]["booked"])):
        #get transaction id 
        getCurrentId = convert["transactions"]["booked"][i]["transactionId"]
        #get all id's
        getIds = pd.read_csv('transactions.csv', usecols=['transactionId'])
        #boolean which checks if id is already in csv
        check = getCurrentId in getIds
        #check if bool is true if yes nothing happpens because id is already in csv
        if check == True:
            print('transaction already in csv')
        else:
            #read transactions as df
            df = pd.read_csv('transactions.csv')
            #create a second object of the df
            df2 = df
            #iter over number of columns 
            counter = 0
            for j in range(len(df.head().columns)):
                counter += 1
                print(counter)
                #list with all value from current iter
                lWithValues = []
                lWithValuesAll = []
                #iter over every transaction
                #print(len(convert["transactions"]["booked"]))
                #for k in range(len(convert["transactions"]["booked"])):
                    #get value with key from current column from current transaction
                try:
                    val = convert["transactions"]["booked"][i][df.head().columns[j]]
                    lWithValues.append(val)
                    #df2.append({df.head().columns[0]: val}, ignore_index=True)
                    #add value to position k column in dataframe
                    #write new df to csv
                    #add this value to exact this position of k - column
                except KeyError:
                    lWithValues.append('0')
            #print(lWithValues)
            #break
            counter = 0
            #lWithValuesAll.append(lWithValues)
            #lWithValues = []
    #print(len(lWithValuesAll))
                    #add on current column current value
                    #df2 = df2.append({df.head().columns[k]: val}, ignore_index=True)
    #write to csv
    df2.to_csv('transactions.csv', index=False)
            
    
def test():
    df = pd.read_csv('transactions.csv')
    #get size of head df
    #get number of columns
    for i in range(len(df.head().columns)):
        for j in range(len(convert["transactions"]["booked"])):
            #set elem at column i to value of convert["transactions"]["booked"][j][key] - but only if key exists
            #from last line 
            print(df.head().columns[i])


    #iter over indexes of df and get with index value from current record the value if it exists
    #iter over values from header 
    #get value from value of first header entry
    #first = df.head().columns[0]
   #print(first)

    #transactions = json.load(open('transactions.json'))
    
def createCsv():
    #create df with all keys + amount and currency
    createCsv = pd.DataFrame(columns = getAllKeys())
    #add amount and currency to header columns

    #addHeader = createCsv.append({'amount', 'currency'}, ignore_index=True)
    #write to csv 
    createCsv.to_csv('transactions.csv', index=False)
    


    
if __name__ == "__main__":
    #createCsv() only run once for init!
    #print(getFirstDict())
    addTransactionsToCsv()    




