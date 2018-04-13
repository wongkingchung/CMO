# libraries and data
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd

date_format = "%Y-%m-%d"
fd = "2018-04-11"
td = "2018-08-08"
delta = datetime.strptime(td,date_format) - datetime.strptime(fd,date_format)

#rate= delta/7
perioddays = int((delta.total_seconds()/3600/24)/7 ) + 1

rate = int( (100.0/perioddays) + 0.5 )

burndown = [rate * x for x in range(perioddays)]
df = pd.DataFrame(burndown, columns=['estimated'])
df['date']=pd.date_range(fd,td,freq='7D')

 

actual=pd.DataFrame({'actual':[0,0,5,7,10,15,20,24,27,30,35,40,45,48,60,62,64,75]}) 
actual['date']=pd.date_range('2018-04-11','2018-08-08',freq='7D')

# plot
plt.xticks(rotation=30)
plt.title('Project 1')
plt.ylabel('Completion %')
plt.plot( 'date', 'estimated', data=df, label='Estimated')
plt.plot( 'date','actual',data=actual, label='Actual')
#plt.gca().legend('Actual','Estimated')
plt.savefig('c:\\coding\\burn.png')
plt.legend()
plt.show()


