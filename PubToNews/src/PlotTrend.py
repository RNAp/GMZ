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

def PlotTrend(filename, timeunit):
    f=open(filename)
    list_of_dates=[]
    
    if timeunit is 'week'
       ind = 1
       else if timeunit is 'month'
            ind = 0
            else:
                print 'Wrong time unit. Please choose week or month'
                return
    for line in f:
            fields = line.split()
            if ind == 1:
                list_of_weeks=[]
                week_count=(dt.datetime.strptime(fields[1],DATE_TIMEFORMAT).date()).isocalendar()[1]
                week_idx=fields[1](:4)+str(week_count)
                list_of_weeks.append(week_idx)
                grouped_week = [[d, len(list(g))] for d,g in itertools.groupby(list_of_weeks, lambda k: k)]
                print(grouped_week)
            else:
                list_of_months=[]
                month_idx=fields[1](:6)
                list_of_months.append(month_idx)
                grouped_month = [[d, len(list(g))] for d,g in itertools.groupby(list_of_months, lambda k: k)]
                print(grouped_month)
   