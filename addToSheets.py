import pandas as pd
import json
import gspread

gc = gspread.service_account(
    filename='/Users/maxhager/Projects2022/Keys/GoogleSheetsKey.json')
sh = gc.open("TransactionsOverview").sheet1


def getAllKeys():
    convert = json.load(
        open('/Users/maxhager/Projects2022/TransactionsOverview/transactions.json'))
    keys = []
    allKeys = []
    for i in range(len(convert["transactions"]["booked"])):
        keys = list(convert["transactions"]["booked"][i].keys())
        for j in keys:
            allKeys.append(j)
    allKeys.append('amount')
    allKeys.append('currency')
    finalKeys = set(allKeys)
    finalKeys.remove('transactionAmount')
    finalKeys.remove('remittanceInformationUnstructuredArray')
    return finalKeys


def checkIfTransactionIdIsInCsv(transactionId, allTransactionIds):
    if transactionId in allTransactionIds:
        return True
    else:
        return False


def addTransactionsToCsv():
    allTransactionIds = sh.col_values(3)
    tempVal = []
    loaded = json.load(open(
        '/Users/maxhager/Projects2022/TransactionsOverview/transactions.json'))["transactions"]["booked"]
    df = pd.read_csv(
        '/Users/maxhager/Projects2022/TransactionsOverview/transactions.csv')
    for i in range(len(loaded)):
        if checkIfTransactionIdIsInCsv(loaded[i]["transactionId"], allTransactionIds) == False:
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
                        tempVal.append(' ')
            df = pd.concat(
                [df, pd.DataFrame([tempVal], columns=getAllKeys())], ignore_index=True)
            tempVal = []
    df.to_csv(
        '/Users/maxhager/Projects2022/TransactionsOverview/transactions.csv', index=False)


def addToSheets():
    if sh.get_all_values() == []:
        header = pd.read_csv(
            '/Users/maxhager/Projects2022/TransactionsOverview/transactions.csv', nrows=0)
        l = header.columns.tolist()
        sh.append_row(l)
    else:
        df = pd.read_csv(
            '/Users/maxhager/Projects2022/TransactionsOverview/transactions.csv')
        sh.append_rows(df.values.tolist())
        sh.sort((12, 'des'))
    remove = pd.read_csv(
        '/Users/maxhager/Projects2022/TransactionsOverview/transactions.csv', nrows=0)
    remove.to_csv(
        '/Users/maxhager/Projects2022/TransactionsOverview/transactions.csv', index=False)


def createCsv():
    createCsv = pd.DataFrame(columns=getAllKeys())
    createCsv.insert(0, 'amount', createCsv.pop('amount'))
    createCsv.insert(1, 'currency', createCsv.pop('currency'))
    createCsv.insert(2, 'transactionId', createCsv.pop('transactionId'))
    createCsv.insert(3, 'debtorName', createCsv.pop('debtorName'))
    createCsv.insert(4, 'remittanceInformationUnstructured',
                     createCsv.pop('remittanceInformationUnstructured'))
    createCsv.to_csv(
        '/Users/maxhager/Projects2022/TransactionsOverview/transactions.csv', index=False)


if __name__ == "__main__":
    addTransactionsToCsv()
    addToSheets()
