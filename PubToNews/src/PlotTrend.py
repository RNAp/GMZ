# -*- coding: utf-8 -*-
"""
PlotTrend: Plot the volumen fo publication in time unit (day/week/month) as a functino of time
"""
import datetime as dt 
import string
import itertools
import matplotlib.pyplot as plt

DATE_TIMEFORMAT = "%Y-%m-%d"

def PlotTrend(filename, timeuit):
    f=open(filename)
    
    if timeuit is 'week':
       ind = 1
    elif timeuit is 'month':
           ind = 0
    else:
        print 'Wrong time unit. Please choose week or month'
        return
   
        
    if ind == 1:
        list_of_weeks=[]
        for line in f:
            fields = line.split()
            week_count=(dt.datetime.strptime(fields[1],DATE_TIMEFORMAT).date()).isocalendar()[1]
            week_idx=fields[1][:4]+str(week_count)
            list_of_weeks.append(week_idx)
        f.close()
        grouped_week = [[d, len(list(g))] for d,g in itertools.groupby(list_of_weeks, lambda k: k)]
        count=[x[1] for x in grouped_week]
        week_lb=[x[0] for x in grouped_week]
        plt.plot(range(len(count)),count)
        plt.xticks(rotation=90)
        plt.xticks(range(len(count)),week_lb)
        plt.show()
    elif ind ==0:
        list_of_months=[]        
        for line in f:
            fields = line.split()
            month_idx=fields[1][:4]+fields[1][5:7]
            list_of_months.append(month_idx)
        f.close()
        grouped_month = [[d, len(list(g))] for d,g in itertools.groupby(list_of_months, lambda k: k)]
        count=[x[1] for x in grouped_month]
        month_lb=[x[0] for x in grouped_month]
        plt.plot(range(len(count)),count)
        plt.xticks(rotation=90)
        plt.xticks(range(len(count)),month_lb)
        plt.show()
   