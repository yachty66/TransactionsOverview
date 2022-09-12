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
import requests
import config
import json

# convert curl to python with https://curlconverter.com/


def getToken():
    headers = {
        'accept': 'application/json',
    }

    json_data = {
        'secret_id': config.secretId,
        'secret_key': config.secretKey
    }

    response = requests.post(
        'https://ob.nordigen.com/api/v2/token/new/', headers=headers, json=json_data)

    return response.json()


def chooseBank():
    headers = {
        'accept': 'application/json',
        'Authorization': config.accessToken
    }
    params = {
        'country': 'de',
    }
    response = requests.get(
        'https://ob.nordigen.com/api/v2/institutions/', params=params, headers=headers)
    id = ""
    for bank in response.json():
        if bank['name'] == 'N26 Bank':
            id = bank['id']
    return id


def buildLink():
    headers = {
        'accept': 'application/json',
        'Authorization': config.accessToken
    }

    json_data = {
        'redirect': 'http://localhost:8000/',
        'institution_id': 'N26_NTSBDEB1'
    }

    response = requests.post(
        'https://ob.nordigen.com/api/v2/requisitions/', headers=headers, json=json_data)
    return response.json()


def listAccounts():
    headers = {
        'accept': 'application/json',
        'Authorization': config.accessToken
    }

    response = requests.get(
        "https://ob.nordigen.com/api/v2/requisitions/" + config.linkId + "/", headers=headers)
    return response.json()


def getTransactions():
    # data from last 90 day altough it is possible to get transactions from the last 24 months
    # access needs to be manually refreshed every 90 days
    headers = {
        'accept': 'application/json',
        'Authorization': config.accessToken
    }

    response = requests.get("https://ob.nordigen.com/api/v2/accounts/" +
                            config.account + "/transactions/", headers=headers)
    with open('transactions.json', 'w') as outfile:
        json.dump(response.json(), outfile)


if __name__ == '__main__':
    # print(getToken())
    # print(chooseBank())
    # print(buildLink())
    # print(listAccounts())
    getTransactions()
