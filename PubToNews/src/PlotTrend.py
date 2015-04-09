# -*- coding: utf-8 -*-
"""
PlotTrend: Plot the volumen fo publication in time unit (day/week/month) as a functino of time
"""
import datetime as dt 
import itertools
from pyplot import hist
from matplotlib.dates import date2num

DATE_TIMEFORMAT = "%Y-%m-%d"

def PlotTrend(filename):
    f=open(filename)
    list_of_dates=[]
    for line in f:
            fields = line.split()
            list_of_dates.append(dt.datetime.strptime(fields[1],DATE_TIMEFORMAT).date())
    grouped_dates = [[d, len(list(g))] for d,g in itertools.groupby(list_of_dates, lambda k: (k.year,k.month)]
    dates, counts = grouped_dates.transpose()
    counts = counts.cumsum()
    step(dates, counts)