# scrap all data from all tokens and coin within a timeframe and total marketcap

#Use CoinmarketCap API
This program require python2.7
Run using: (Optional Param: Mininal Marketcap, Timefrom: M/D/Y) . 
python scrape.py 5000000000

Install:
pip install -r requirements.txt

#Strategies involved:
1. Buy and hold strategy - acting as the base alpha to other strategies
2. 20 day SMA Strategy
3. 8 day EMA Strategy
4. Volumn analysis with 8 day EMA Strategy
5. Twitter Sentiment with Volume
