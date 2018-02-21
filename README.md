# scrap all data from all tokens and coin within a timeframe and total marketcap

#Use CoinmarketCap API

This program require python2.7. &nbsp;

Run using: (Optional Param: Mininal Marketcap, Timefrom: M/D/Y). &nbsp;

python scrape.py 5000000000
***
Install:
pip install -r requirements.txt
***

This tool utilizes numpy, matplotlib, panda

#Strategies involved:
1. Buy and hold strategy - acting as the base alpha to other strategies
2. 20 day SMA Strategy
3. 8 day EMA Strategy
4. Volume analysis with 8 day EMA Strategy
5. Twitter Sentiment with Volume
