from django.shortcuts import render
from django.http import HttpResponse
from yahoo_fin.stock_info import *
import time 
import pandas as pd
# Create your views here.
'''Yahoo_fin is a Python 3 package designed to scrape historical stock price data, as well as to provide current information on market caps, dividend yields, and which stocks comprise the major exchanges. Additional functionality includes scraping income statements, balance sheets, cash flows, holder information, and analyst data. The package includes the ability to scrape live (real-time) stock prices, capture cryptocurrency data, and get the most actively traded stocks on a current trading day. Yahoo_fin also contains a module for retrieving option prices and expiration dates.

The latest version of yahoo_fin can also scrape earnings calendar history and has an additional module for scraping financial news RSS feeds.'''

def stockPicker(request):

    # Returns a list of tickers currently listed on the NIFTY50 
    stock_picker = tickers_nifty50()
    print(stock_picker)
    
    return render(request, 'mainapp/stockpicker.html',{'stockpicker' : stock_picker})

def stockTracker(request):

    # stockpicker contains all stocks which user has selected
    stockpicker = request.GET.getlist('stockpicker')
    print(stockpicker)

    # this stores the data for all selected stocks(available_stocks)
    data={}
    available_stocks= tickers_nifty50()

    
    for i in stockpicker:
        if i in available_stocks:
            pass
        else:
            return HttpResponse("Error")
        
    # get_quote_table is basically web scraping yahoo finance for stock data and we are using it as an api 
    start = time.time()
    print(start)
    for i in stockpicker:
        details = get_quote_table(i)
        # data.update({i: details})
        print(details)
    
    end = time.time()
    time_taken=end-start
    print(time_taken)

    print(data) 
    return render(request, 'mainapp/stocktracker.html')
