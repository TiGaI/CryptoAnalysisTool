#!/usr/bin/env python
import argparse
import requests
import time
from datetime import datetime
from random import random
import logging
import pandas as pd
import matplotlib.pyplot as plt
import lxml.html #Faster than Beatuiful Soup

parser = argparse.ArgumentParser(description='Scraping Tokens and Coins')
parser.add_argument('min_market_cap', metavar='min_cap', type=int, nargs='?', default=0,
                   help='minimum market cap [usd] for currency to be scraped (default: scrape all)')

args = parser.parse_args()

# Configuration
timestamp_0 = 1367174841000
timestamp_1 = int(round(time.time() * 1000))
logging.basicConfig(
    filename="logging.log", 
    level=logging.INFO, 
    format='%(asctime)s:%(name)s:%(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p')

BASE_URL = "http://coinmarketcap.com"
graphBASE_URL = "https://graphs2.coinmarketcap.com/"

countRequested = 0
interReqTime = 23
lastReqTime = None

def request(targetURL):
    global countRequested
    global lastReqTime
    if lastReqTime is not None and time.time() - lastReqTime < interReqTime:
        timeToSleep = random()*(interReqTime-time.time()+lastReqTime)*2
        logging.info("Sleeping for {0} seconds before request.".format(timeToSleep))
        time.sleep(timeToSleep)

    r = requests.get(targetURL)

    lastReqTime = time.time()
    countRequested += 1
    if r.status_code == requests.codes.ok:
        return r.text
    else:
        raise Exception("Could not process request. \
            Received status code {0}.".format(r.status_code))

def scrapeCoinList():
    URL = "{0}/{1}/views/{2}/".format(BASE_URL, 'coins', 'all')
    html = request(URL)
    data = LoopandFilterListData(html)
    return data

def scrapeTokenList():
    URL = "{0}/{1}/views/{2}/".format(BASE_URL, 'tokens', 'all')
    html = request(URL)
    data = LoopandFilterListData(html)
    return data

def LoopandFilterListData(html):
    data = []
    html = lxml.html.fromstring(html)
    rowsoftoken = html.cssselect("table > tbody > tr")
    for row in rowsoftoken:
        datum = {}
        fields = row.cssselect('td')
        datum['name'] = fields[1].cssselect("a")[0].text_content().strip()
        datum['slug'] = fields[1].cssselect("a")[0].attrib['href'].replace(
            '/currencies/', '').replace('/', '').strip()
        if fields[3].text_content().strip().replace(",", "")[1:] == '':
            break
        datum['marketcap'] = int(fields[3].text_content().strip().replace(",", "")[1:])
        supplyFieldPossible = fields[5].cssselect("a")
        if len(supplyFieldPossible) > 0:
            datum['explorer_link'] = supplyFieldPossible[0].attrib['href']
        else:
            datum['explorer_link'] = ''
        #Checking Market_cap
        if args.min_market_cap < datum['marketcap']:
            data.append(datum)
    return data

def getDetailandGraphData(token):
    URL = "{0}/currencies/{1}/".format(graphBASE_URL, token['slug'])
    rawData = pd.read_json(URL)
    rawData['time'] = rawData['market_cap_by_available_supply'].apply(lambda x: datetime.utcfromtimestamp(float(x[0])).strftime('%Y-%m-%dT%H:%M:%SZ')) #convert UNIX TIMEstamp into readable data
    rawData['market_cap_by_available_supply'] = rawData['market_cap_by_available_supply'].apply(lambda x: x[1])
    rawData['price_btc'] = rawData['price_btc'].apply(lambda x: x[1])
    rawData['price_platform'] = rawData['price_platform'].apply(lambda x: x[1])
    rawData['price_usd'] = rawData['price_usd'].apply(lambda x: x[1])
    rawData['volume_usd'] = rawData['volume_usd'].apply(lambda x: x[1])
    #rawData.to_csv("{0}.csv".format(token[slug]), sep=',',index=False)
    #print rawData
    return rawData

def technicalAnalysis(df):
    #TODO LIST
    #Filter and cutdown data Within the past 3 months
    #Analysis the trendline Linear Regression
    #Compare the peaks and High highs and low lows
    #The total volumn between spikes
    


def main():
    ##logging.info("Attempting to scrape token list.")
    tokens = scrapeTokenList()
    ##logging.info("Finished scraping token list. Starting on tokens.")

    for token in tokens:
        logging.info("> Starting scrape of token {0}...".format(token['slug']))
        df = getDetailandGraphData(token)
        TechnicalAnalysis(df)

    rawData.to_csv("testing2.csv", sep=',',index=False)
    ##logging.info("Attempting to scrape coin list...")
    #coins = scrapeCoinList()
    ##logging.info("Finished scraping coin list. Starting on coins...")

    # for coin in coins:
    #     logging.info("> Starting scrape of coin {0}...".format(coin['slug']))

    #     getDetailandGraphData(token)
    #print coins




#def main():
    # d = get_historical_data(COIN)
    # df = pd.DataFrame({"Time":list(d.keys()), "Price":list(d.values())})
    # df.index = df['Time']
    # df['Price'].plot(figsize=(20,10), color="green")
    # plt.title(COIN)
    # plt.xlabel('Date')
    # plt.ylabel('Price')
    # plt.show()

if __name__=='__main__':
    main()
