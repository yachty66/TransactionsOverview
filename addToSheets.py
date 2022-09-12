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
    #get all transactions from json
    #check if transaction id is already in csv
    #if not add it to csv
    #else do nothing
    convert = json.load(open('transactions.json'))
    for i in range(len(convert["transactions"]["booked"])):
        #iter over all transactions
        #take one transaction - check if id is in csv
        getCurrentId = convert["transactions"]["booked"][i]["transactionId"]
        #check if getCurrentId is in csv
        #get column with transaction ids from csv
        getIds = pd.read_csv('transactions.csv', usecols=['transactionId'])
        #check if getCurrentId is in column
        check = getCurrentId in getIds
        #if check is true do nothing else add transaction to csv
        if check == True:
            print('transaction already in csv')
        else:
            #add following to last line of csv
            #load csv into df
            df = pd.read_csv('transactions.csv')
            df2 = df
            for j in range(len(df.head().columns)):
                for k in range(len(convert["transactions"]["booked"])):
                    #add to last line
                    #first get value with key if available  
                    val = convert["transactions"]["booked"][k][df.head().columns[j]]
                    #add to last line of df2 
                    df2 = df2.append({df.head().columns[k]: val}, ignore_index=True)
                    #write df2 to transactions.csv
    write = df2.to_csv('transactions.csv', index=False)
                
                    
                    
            #set elem at column i to value of convert["transactions"]["booked"][j][key] - but only if key exists
            #from last line 
            print(df.head().columns[i])
            #iter over indexes of df and get with index value from current record the value if it exists
            #iter over values from header 
            #get value from value of first header entry
            
            first  = df.head().columns[0]
            print(first)
    
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
    test()
    




