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

# get first dictionary from transactions.json


def getAllKeys():
    convert = json.load(open('transactions.json'))
    keys = []
    allKeys = []
    for i in range(len(convert["transactions"]["booked"])):
        keys = list(convert["transactions"]["booked"][i].keys())
        for j in keys:
            allKeys.append(j)
    allKeys.append('amount')
    allKeys.append('currency')
    finalKeys = set(allKeys)
    #remove transactionAmount form finalKeys
    finalKeys.remove('transactionAmount')
    #remove remittanceInformationUnstructuredArray
    finalKeys.remove('remittanceInformationUnstructuredArray')
    return finalKeys


def checkIfTransactionIdIsInCsv(transactionId):
    #get all values from transactionId column form csv 
    ids = pd.read_csv('transactions.csv', usecols=['transactionId'])
    #print(ids.values)
    if transactionId in ids.values:
        return True
    else:
        return False


def addTransactionsToCsv():
    tempVal = []
    loaded = json.load(open('transactions.json'))["transactions"]["booked"]
    df = pd.read_csv('transactions.csv')
    for i in range(len(loaded)):
        if checkIfTransactionIdIsInCsv(loaded[i]["transactionId"]) == False:            
            for j in getAllKeys():
                if j == "amount" or j == "currency":
                    tempVal.append(loaded[i]["transactionAmount"][j])
                elif j == "debtorAccount" and "debtorAccount" in loaded[i]:
                    tempVal.append(loaded[i]["debtorAccount"]["iban"])
                elif j == "creditorAccount" and "creditorAccount" in loaded[i]:
                    tempVal.append(loaded[i]["creditorAccount"]["iban"])
                else:
                    if j in loaded[i]:
                        tempVal.append(loaded[i][j])
                    else:
                        tempVal.append('')
            df = pd.concat([df, pd.DataFrame([tempVal], columns=getAllKeys())], ignore_index=True)
            tempVal = []
    df.to_csv('transactions.csv', index=False) 



def createCsv():
    createCsv = pd.DataFrame(columns=getAllKeys())
    createCsv.insert(0, 'amount', createCsv.pop('amount'))
    createCsv.insert(1, 'currency', createCsv.pop('currency'))
    createCsv.insert(2, 'transactionId', createCsv.pop('transactionId'))
    createCsv.insert(3, 'debtorName', createCsv.pop('debtorName'))
    createCsv.insert(4, 'remittanceInformationUnstructured', createCsv.pop('remittanceInformationUnstructured'))
    createCsv.to_csv('transactions.csv', index=False)

def test():
    convert = json.load(open('transactions.json'))
    for i in range(len(convert["transactions"]["booked"])):
        print(convert["transactions"]["booked"])
        break
    



if __name__ == "__main__":
    # createCsv() only run once for init!
    # print(getFirstDict())
    createCsv()
    addTransactionsToCsv()
    
