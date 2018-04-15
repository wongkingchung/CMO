import pandas  
import math
from datetime import datetime
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt


df = pandas.read_excel('C:\\coding\\ProjectProgress.xlsx', header=None)



def genchart(col):
    actual = []
    actualdate = []
    d = 0
    date_format = "%Y-%m-%d %h:%m:%s"
    scan = True
    row=0

    while (scan):
        if row == 0 :
            project = df.loc[row,col]
        if row == 1 :
            fd = df.loc[row,col]
        if row == 2 :
            td = df.loc[row,col]
            wks = (td - fd).days/7

        if row > 2 :
            fig = df.loc[row,col]
            if not math.isnan(fig):
                actual.append(fig)
                nxtday = fd + timedelta(days=7*d)
                actualdate.append(nxtday)
                d = d + 1
            else:
                scan = False

        row = row + 1
        
    #    print df.loc[row,0]
        
#    print project, fd, td
#    print actual 
#    print actualdate
#    print wks

    rate = int( (100.0/wks))
    burndown = [rate * x for x in range(wks+1)]
    estimate = pandas.DataFrame(burndown, columns=['estimated'])
    estimate['date']= pandas.date_range(fd,td,freq='7D')
    print estimate

    plt.subplot(2,2,col+1)

    plt.xticks(rotation=45)
    plt.title(project)
    plt.ylabel('Completion %')
    #plt.plot( 'date','actual',data=actdf, label='Actual')
    plt.plot( 'date', 'estimated', data=estimate, label='Estimated')
    plt.plot( actualdate, actual, label='Actual')
    plt.legend()
#    plt.show()


for x in range(len(df.columns)):
    genchart(x)

plt.subplots_adjust(hspace=0.7, wspace=0.5)
plt.show()
