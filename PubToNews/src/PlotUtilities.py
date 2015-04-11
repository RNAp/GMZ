# -*- coding: utf-8 -*-
"""
PlotTrend: Plot the volumen fo publication in time unit (day/week/month) as a functino of time
"""
import datetime as dt 
import string
import itertools
import matplotlib.pyplot as plt

DATE_TIMEFORMAT = "%Y-%m-%d"

def ExtracHist(input_filename, timeuit, output_filename):
    #Decide the time unit        
    if timeuit is 'week':
        ind = 1
    elif timeuit is 'month':
            ind = 0
    else:
        print 'Wrong time unit. Please choose week or month'
        return
   
    with open(input_filename, 'r') as f:       
        if ind == 1:#Take week as time unit
           list_of_weeks=[]
           for line in f:
               #read in the info for an article
               fields = line.split()
               #Decide the which week this day is in that year
               week_count=(dt.datetime.strptime(fields[1],DATE_TIMEFORMAT).date()).isocalendar()[1]
               #Give an unique lable for that week and assigned it to this article
               week_idx=fields[1][:4]+str(week_count)
               list_of_weeks.append(week_idx)
           f.close()
           #group articles by their week label, generate a list of pairs of  [weeklable, count]
           grouped= [[d, len(list(g))] for d,g in itertools.groupby(list_of_weeks, lambda k: k)]
        
        elif ind ==0:
            list_of_months=[]        
            for line in f:
                #read in the info for an article
                fields = line.split()
                #Give an unique lable for that month and assigned it to this article
                month_idx=fields[1][:4]+fields[1][5:7]
                list_of_months.append(month_idx)
            f.close()
            #group articles by their week label, generate a list of pairs of  [monthlable, count]
            grouped= [[d, len(list(g))] for d,g in itertools.groupby(list_of_months, lambda k: k)]
            #print grouped
    f.close()
    #Start file writing
    with open(output_filename,'w') as f:
        for cp in grouped:
            f.write(cp[0])
            f.write("\t %s " % str(cp[1]))
            f.write("\n")
    f.close
    
    
def PlotHist(input_filename):
    with open(input_filename, 'r') as f: 
         label=[]
         count=[]
         for line in f:
             fields=line.split()
             label.append(fields[0])
             count.append(fields[1])
         plt.plot(range(len(count)),count)
         plt.xticks(rotation=90)
         plt.xticks(range(len(count)),label)
         plt.show()
    return
             