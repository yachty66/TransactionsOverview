import json

from git import refresh
import config
import requests
import sys
sys.path.append("/Users/maxhager/Projects2022/TransactionsOverview")

# convert curl to python with https://curlconverter.com/

#get a token
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

def refreshToken():
    headers = {
    'accept': 'application/json',
    }

    json_data = {
    'refresh': config.refreshToken,
    }

    response = requests.post('https://ob.nordigen.com/api/v2/token/refresh/', headers=headers, json=json_data)
    print(response.json())

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


def userAgreement():
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ACCESS_TOKEN',
    }

    data = '{"institution_id": "N26_NTSBDEB1",\n       "max_historical_days": "90",\n       "access_valid_for_days": "360",}'

    response = requests.post(
        'https://ob.nordigen.com/api/v2/agreements/enduser/', headers=headers, data=data)


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
    with open('/Users/maxhager/Projects2022/TransactionsOverview/transactions.json', 'w') as outfile:
        json.dump(response.json(), outfile)
    print(response.json())


if __name__ == '__main__':
    #print(getToken())
    #print(refreshToken())
    #print(chooseBank())
    #print(buildLink())
    #print(listAccounts())        
    #write into test.txt
    getTransactions()
    

