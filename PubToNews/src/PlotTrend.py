# -*- coding: utf-8 -*-
"""
PlotTrend: Plot the volumen fo publication in time unit (day/week/month) as a functino of time
"""
import datetime as dt 
import string
import itertools
#from pyplot import hist
#from matplotlib.dates import date2num

DATE_TIMEFORMAT = "%Y-%m-%d"

def PlotTrend(filename, timeuit):
    f=open(filename)
    
    if timeuit is 'w':
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
            week_idx=fields[1][:5]+str(week_count)
            list_of_weeks.append(week_idx)
        f.close()
        grouped_week = [[d, len(list(g))] for d,g in itertools.groupby(list_of_weeks, lambda k: k)]
        print(grouped_week)
        #return grouped_week
    elif ind ==0:
        list_of_months=[]        
        for line in f:
            fields = line.split()
            month_idx=fields[1][:7]
            list_of_months.append(month_idx)
        f.close()
        grouped_month = [[d, len(list(g))] for d,g in itertools.groupby(list_of_months, lambda k: k)]
        print(grouped_month)
        #return grouped_month
   