from django.shortcuts import render
from django.http import HttpResponse
from yahoo_fin.stock_info import *
import yahoo_fin.stock_info as si
import time 
import pandas as pd
import queue
from threading import Thread 
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
        
    # Creating a thread list to enable multithreading
    n_threads=len(stockpicker)
    thread_list=[]  
    que=queue.Queue()
    start = time.time()

    # get_quote_table is basically web scraping yahoo finance for stock data and we are using it as an api 
    # for i in stockpicker:
        # result = get_quote_table(i)
        # data.update({i: result})
        # print(result) 
    
    # using thread reduces the time taken to fetch data from the yahoo_fin
    for i in range(n_threads):
        # creating a thread
        thread = Thread(target= lambda q, arg1: q.put({stockpicker[i]: si.get_quote_table(arg1)}), args=(que,stockpicker[i]))
        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()

    while not que.empty():
        result=que.get()
        data.update(result)

    end = time.time()
    time_taken =  end-start
    print(time_taken)

    print(data) 
    return render(request, 'mainapp/stocktracker.html', {'data': data, 'room_name': 'track'})
