from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#%matplotlib inline

#Load Data for csv file
#Use the T-Lines
def TlinesAnalysis(df):
#     TODO LIST
#     1. Filter and cutdown data Within the past 3 months
#     Analysis the trendline Linear Regression
#     Compare the peaks and High highs and low lows
#     The total volumn between spikes
#     Swing Trading Points
#         Always enter a trade with a clear trading plan, the four key elements of which are a target, a limit, a stop loss and an add-on point.
#         Always align your trade with the overall direction of the market.
#         focus on the 6-month daily chart. Here, I can see finer details that the weekly chart obscures.
#         look for volume dries up at lows
#         Dont get caught up in the coin or company. 
#         Use a T-Line trading strategy. -8-day exponential moving average
#         the farther away from the T-line, the high the possible of it going back to the T-Line
#         Rollover - happen when the price can go over the T-line, high possibility of it will drop
#         https://www.investopedia.com/ask/answers/122314/what-exponential-moving-average-ema-formula-and-how-ema-calculated.asp
#         https://blog.quantopian.com/a-professional-quant-equity-workflow/
    threeMonth = df['time'].iloc[-1] - datetime.timedelta(days=90)
    df = df[df['time']>threeMonth]

    print(df.describe())

def volumeAnalysis(df):
	
	positivelist = []
	negativelist = []
	totaloverallsum = 0
	#set percentage is to determine if the time period of price values is spiking or drop or just a plateau
	setpercentage = .50 
	# For the sake of the testing, we will do up to 20 'datapoints'
	for x in range(0,20):
		difference = (float(df.iloc[x+1]['price_usd']) - float(df.iloc[x]['price_usd']))*float(df.iloc[x]['volume_usd'])
		

		if difference > 0:
			positivelist.append(difference)
		elif difference < 0:
			negativelist.append(difference)
	
	#cool way to calculate the sum of the positve and negative lists respectively
	sumpositive = sum(map(float,positivelist))
	sumnegative = sum(map(float,negativelist))
	

	totaloverallsum = sumpositive+sumnegative
	percentage = ((sumpositive - sumnegative) / totaloverallsum) * 100
	if abs(percentage) > setpercentage:
		if percentage > 0:
			print("A spike has occured from " + df.iloc[0]['time'] + " to " + df.iloc[20]['time'])

		elif percentage < 0:
			print("A drop has occured from " + df.iloc[0]['time'] + " to " + df.iloc[20]['time'])
	else:
		print("No drop has occured from " + df.iloc[0]['time'] + " to " + df.iloc[20]['time']) 

 


def EMA8DAY(df):
	#format the date and calculate the 8 day simple average average
	fig = plt.figure(figsize=(15,9))
	ax = fig.add_subplot(1,1,1)
	my_year_month_fmt = mdates.DateFormatter('%m/%y')
	short_rolling = df.rolling(window=8).mean()
	start = df['time'][0]
	end = df['time'][-1]
	start_date = '2015-01-01' #  #whatever we set it to be
	end_date = '2016-12-31' #whatever we set it to be
	ax.plot(short_rolling.ix[start_date:end_date, :].index, short_rolling.ix[start_date:end_date, 'MSFT'], label = '8-days SMA')
	ema_short = df.ewm(span=8, adjust=False).mean()

    #Taking the different between the prices and the EMA timeseries
	trading_positions_raw = data - ema_short

	ax.plot(data.ix[start_date:end_date, :].index, data.ix[start_date:end_date, 'MSFT'], label='Price')
	ax.plot(ema_short.ix[start_date:end_date, :].index, ema_short.ix[start_date:end_date, 'MSFT'], label = 'Span 8-days EMA')
	ax.legend(loc='best')
	ax.set_ylabel('Price in $')
	ax.grid() #set grid

	year_month_format = mdates.DateFormatter('%d/%m/%y')

	ax.xaxis.set_major_fomratter(year_month_format)
    #When the price timeseries p(t) crosses the EMA timeseries e(t) from below, we will close any existing short position and go long (buy) one unit of the asset.

	#When the price timeseries p(t) crosses the EMA timeseries e(t) from above, we will close any existing long position and go short (sell) one unit of the asset.

	#Custom trading Prediction for 8EMA
	trading_positions = trading_positions_raw.apply(np.sign) * 1
	# Lagging our trading signals by one day.
	trading_positions_final = trading_positions.shift(1)

	#Find the log of the prices is taken and the difference of the consecutive log observations
	#Predict the price 
	#Above the Tline -> Sell
	#Below the Tline -> Buy

	asset_log_returns = np.log(data).diff()
	strategy_asset_log_returns = trading_positions_final * asset_log_returns

	# Get the cumulative log-returns per asset
	cum_strategy_asset_log_returns = strategy_asset_log_returns.cumsum()
	# Transform the cumulative log returns to relative returns
	cum_strategy_asset_relative_returns = np.exp(cum_strategy_asset_log_returns) - 1
	# Taking the sum of the all of the returns
	cum_relative_return_exact = cum_strategy_asset_relative_returns.sum(axis=1)

	ax.plot(cum_relative_return_exact.index, 100*cum_relative_return_exact, label='EMA strategy')
	ax.set_ylabel('Total cumulative relative returns (%)')
	ax.legend(loc='best')
	ax.set_ylabel('Price in $')
	ax.grid() #set grid
	ax.xaxis.set_major_fomratter(year_month_format)

#Basic strategies to compare to.
def BuyAndHoldStrategy(df):
	#using delta price in time instead of price in function of time
	#1 day price different in %
	returns = data.pct_change(1)
	#log
	log_returns = np.log(data).diff()

	#calculate total return in % 
	ax = fig.add_subplot(2,1,2)

	for c in log_returns:
	    ax.plot(log_returns.index, 100*(np.exp(log_returns[c].cumsum()) - 1), label=str(c))

	ax.set_ylabel('Total relative returns (%)')
	ax.legend(loc='best')
	ax.grid()

	plt.show()
	#assuming we buy a number of token at the start

	weights_matrix = pd.DataFrame(1, index=data.index, columns=data.columns)
	temp_var = weights_matrix.dot(log_returns.transpose())
	portfolio_log_returns = pd.Series(np.diag(temp_var), index=log_returns.index)
	total_relative_returns = (np.exp(portfolio_log_returns.cumsum()) - 1)
	fig = plt.figure(figsize=[16,9])
	ax = fig.add_subplot(2, 1, 1)
	ax.plot(portfolio_log_returns.index, portfolio_log_returns.cumsum())
	ax.set_ylabel('Portfolio cumulative log returns')
	ax.grid()
	ax = fig.add_subplot(2, 1, 2)
	ax.plot(total_relative_returns.index, 100 * total_relative_returns)
	ax.set_ylabel('Portfolio total relative returns (%)')
	ax.grid()
	plt.show()

	# Calculating the time-related parameters of the simulation
	days_per_year = 52 * 5
	total_days_in_simulation = data.shape[0]
	number_of_years = total_days_in_simulation / days_per_year

	# The last data point will give us the total portfolio return
	total_portfolio_return = total_relative_returns[-1]
	# Average portfolio return assuming compunding of returns
	average_yearly_return = (1 + total_portfolio_return)**(1 / number_of_years) - 1

	print('Total portfolio return is: ' +
	      '{:5.2f}'.format(100 * total_portfolio_return) + '%')
	print('Average yearly return is: ' +
	      '{:5.2f}'.format(100 * average_yearly_return) + '%')
