import pandas  
import math
from datetime import datetime
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt


df = pandas.read_excel('C:\\coding\\ProjectProgress.xlsx', header=None)

actual = []
actualdate = []
d = 0
date_format = "%Y-%m-%d %h:%m:%s"

for row in range(0, 15):
    if row == 0 :
        project = df.loc[row,0]
    if row == 1 :
        fd = df.loc[row,0]
    if row == 2 :
        td = df.loc[row,0]
        wks = (td - fd).days/7

    if row > 2 :
        fig = df.loc[row,0]
        if not math.isnan(fig):
            actual.append(fig)
            nxtday = fd + timedelta(days=7*d)
            actualdate.append(nxtday)
            d = d + 1

    print df.loc[row,0]
    
print project, fd, td
print actual 
print actualdate

actdict = {'actual':actual, 'date':actualdate}
actdf = pandas.DataFrame(actdict)
#actdf = pandas.DataFrame(actualdate, columns=['date'])

print actdf

plt.xticks(rotation=30)
plt.title('Project 1')
plt.ylabel('Completion %')
#plt.plot( 'date','actual',data=actdf, label='Actual')
plt.plot( actualdate, actual, label='Actual')
plt.legend()
plt.show()

