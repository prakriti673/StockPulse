# This file contains the periodic task to be carried out by celery
from celery import shared_task
from yahoo_fin.stock_info import *
import yahoo_fin.stock_info as si
from threading import Thread
from django.http import HttpResponse
import time
import queue
# we have already once sent the data retrieved from yahoo fin library
# We just want to update the data in the front-end at regular intervals
# stockpicker contains those stocks which user has selected

'''
suppose a user has selected 3 stocks, those go into celery and now celery calls the third party api in every 10 seconds
these reach the user through websockets in the frontend.
now, a second user meanwhile selects 4 stocks (2 common to the prev. users stocks and 2 different), 
now those different 2 stocks go into celery to save the number of api requests.
Now, while rendering data results to the user, a filter is applied so that user sees only those stocks for which he had applied for.
'''

@shared_task(bind=True)
def update_stocks(self, stockpicker):
    data={}
    available_stocks= tickers_nifty50()
    
    for i in stockpicker:
        if i in available_stocks:
            pass
        else:
            stockpicker.remove(i)
        
    # Creating a thread list to enable multithreading
    n_threads = len(stockpicker)
    thread_list = []  
    que = queue.Queue()
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

    
    return 'Done'
    




