import requests, json
#https://favqs.com/api
def getQuotes(namakota):
    URL = "https://favqs.com/api/qotd" 
    getrequest = requests.get(URL)
    jsonnya = getrequest.json()
    quotenya = jsonnya['quote']['body']  
    output = quotenya +" (FPD)"  
    print(output)
getQuotes("qotd")

