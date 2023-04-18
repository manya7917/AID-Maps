import pandas as pd
# import numpy as np
data = {
    'City':["Gwalior","Delhi","Noida","Raipur","Vadodra","Indore","Bhopal"],
    'Name of Personnel' :['Manya','Tanmay','Sharma','Verma','Rana','Raju','Kotak Mahindra'],
    'Service Number':[2345,4567,4567,1234,6785,4598,3490],
    'Headquarters Address':['KAILASH HOSPITAL', 'APOLLO', 'FORTIS','abc','xyz','ert','wer']
          }
df = pd.DataFrame(data)
print(df)

